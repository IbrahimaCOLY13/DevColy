from qgis.core import (
    QgsGeometry, 
    QgsFeatureRequest, 
    QgsSpatialIndex, 
    QgsPointXY,
    QgsProject,
    QgsWkbTypes
)
from PyQt5.QtCore import Qt
from qgis.core import QgsRectangle
import os
import csv

from .Extract_Point_Geom import extraire_dernier_point_geom

class TopologyChecker:
    def __init__(self, layers: dict, connection_tolerance: float = 0.01, mo: str = 'EDV', log_callback=None):
        """
        layers : dict de couches QGIS par clé (ex: 'network_eu', 'manhole_eu', 'branch_eu', ...)
        connection_tolerance : tolérance en unité de la couche (ex. mètres)
        mo : Maître d'ouvrage pour charger la configuration des champs d'altitude
        log_callback : fonction pour envoyer les messages de log (ex: lambda msg: self.add_log(msg))
        """
        self.layers = layers
        self.connection_tolerance = connection_tolerance
        self.mo = mo
        self.spatial_indexes = {}      # cache de QgsSpatialIndex par layer.id() ou layer.name()
        self.error_id = 0
        self.multipart_feature_ids = {}  # {layer_name: set(feature_id, ...)} pour ignorer ensuite
        self.log_callback = log_callback  # Callback pour les logs
        
        # Charger la configuration des champs d'altitude
        self.altitude_config = self.load_altitude_config(mo)
    
    def log(self, message):
        """Envoie un message de log via le callback si disponible"""
        if self.log_callback:
            self.log_callback(message)

    def load_altitude_config(self, mo):
        """Charge la configuration des champs d'altitude depuis le fichier CSV."""
        config = {
            'champ_amont': 'ALTDEB',
            'champ_aval': 'ALTFIN',
            'champs_point': ['COORLAMZ', 'Z(MSL)', 'ALT_POINT', 'ALTITUDE']
        }
        
        # Chemin vers le fichier CSV
        plugin_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(plugin_dir, 'table', 'Champs_altitudes.csv')
        
        if not os.path.exists(csv_path):
            return config  # Retourner config par défaut
        
        try:
            with open(csv_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f, delimiter=';')
                for row in reader:
                    if row['MO'].strip() == mo:
                        config['champ_amont'] = row['Champ_altitude_amont_cana'].strip()
                        config['champ_aval'] = row['Champ_altitude_aval_cana'].strip()
                        # Champs point séparés par |
                        champs_str = row['Champs_altitude_point'].strip()
                        config['champs_point'] = [c.strip() for c in champs_str.split('|')]
                        break
        except Exception as e:
            print(f"Erreur lors du chargement de la config altitude: {e}")
        
        return config

    # Helpers
    def add_error(self, etype, description, layer_name, feature_id=None, geometry=None):
        """Créé et retourne un dict d'erreur standard."""
        self.error_id += 1
        return {
            'id': self.error_id,
            'type': etype,
            'description': description,
            'layer': layer_name,
            'feature_id': feature_id,
            'geometry': geometry
        }
    
    def consolidate_errors(self, errors):
        """
        Fusionne les erreurs concernant la même entité (layer + feature_id).
        Regroupe les descriptions pour éviter les doublons.
        
        Args:
            errors: Liste d'erreurs
            
        Returns:
            Liste d'erreurs consolidées (sans doublons)
        """
        # Regrouper par (layer, feature_id)
        error_groups = {}
        
        for error in errors:
            layer = error.get('layer')
            feature_id = error.get('feature_id')
            
            # Clé unique pour regrouper
            if feature_id is not None:
                key = (layer, feature_id)
            else:
                # Si pas de feature_id, garder l'erreur telle quelle (pas de fusion)
                key = None
            
            if key is None:
                # Ajouter directement sans fusion
                if None not in error_groups:
                    error_groups[None] = []
                error_groups[None].append(error)
            else:
                if key not in error_groups:
                    error_groups[key] = []
                error_groups[key].append(error)
        
        # Fusionner les erreurs par groupe
        consolidated = []
        
        # Erreurs sans feature_id (pas de fusion)
        if None in error_groups:
            consolidated.extend(error_groups[None])
        
        # Erreurs avec feature_id (fusion)
        for key, group in error_groups.items():
            if key is None:
                continue
            
            if len(group) == 1:
                # Une seule erreur, pas de fusion
                consolidated.append(group[0])
            else:
                # Multiple erreurs pour la même entité -> fusionner
                first_error = group[0]
                
                # Collecter tous les types et descriptions
                types = []
                descriptions = []
                for err in group:
                    if err['type'] not in types:
                        types.append(err['type'])
                    if err['description'] not in descriptions:
                        descriptions.append(err['description'])
                
                # Créer une erreur fusionnée
                merged_error = {
                    'id': first_error['id'],  # Garder le premier ID
                    'type': ' + '.join(types) if len(types) > 1 else types[0],
                    'description': ' | '.join(descriptions),
                    'layer': first_error['layer'],
                    'feature_id': first_error['feature_id'],
                    'geometry': first_error['geometry']
                }
                consolidated.append(merged_error)
        
        return consolidated

    def ensure_index(self, layer):
        """Crée et retourne un index spatial pour la couche donnée."""
        if layer is None:
            return None

        layer_id = layer.id()

        # Déjà existant : renvoyer lindex
        if layer_id in self.spatial_indexes:
            return self.spatial_indexes[layer_id]

        # Construire lindex correctement
        index = QgsSpatialIndex()
        for feat in layer.getFeatures():
            index.addFeature(feat)

        self.spatial_indexes[layer_id] = index
        return index


    def bbox_around_point(self, pt, tol=None):
        """Rectangle autour d'un point pour filterRect."""
        t = tol if tol is not None else self.connection_tolerance
        return QgsRectangle(pt.x() - t, pt.y() - t, pt.x() + t, pt.y() + t)

    def get_line_endpoints(self, geom):
        """
        Retourne (start_point: QgsPointXY, end_point: QgsPointXY) pour une ligne.
        Gère singlepart/multipart.
        """
        if geom is None or geom.isEmpty():
            return None, None

        # Gérer multipart
        if geom.isMultipart():
            multi = geom.asMultiPolyline()
            if not multi or not multi[0]:
                return None, None
            poly = multi[0]
        else:
            poly = geom.asPolyline()

        if not poly or len(poly) < 2:
            return None, None

        return poly[0], poly[-1]

    def geometry_is_valid(self, geom):
        """Test simple de validité (non nulle et non vide)."""
        return (geom is not None) and (not geom.isEmpty())

    def is_multipart_line(self, feature):
        """Retourne True si la géométrie ligne est multipart."""
        geom = feature.geometry()
        if not geom:
            return False
        return geom.isMultipart() and QgsWkbTypes.geometryType(feature.geometry().wkbType()) == QgsWkbTypes.LineGeometry

    # Contrôles
    def run_all_checks(self):
        """Exécute toutes les vérifications et retourne une liste des erreurs."""
        all_errors = []

        # 1) multipart lines
        all_errors.extend(self.check_multipart_lines())

        # 2) boxes-branches
        all_errors.extend(self.check_connections_boxes_branches())

        # 3) branches-network
        all_errors.extend(self.check_connections_branches_network())

        # 4) manholes-pipes
        all_errors.extend(self.check_connections_manholes_pipes())

        # 5) do-pipes (overflow)
        all_errors.extend(self.check_connections_do_pipes())

        # 6) pr-pipes (pumps/refoulement)
        all_errors.extend(self.check_connections_pr_pipes())

        # 7) overlaps
        all_errors.extend(self.check_entity_overlaps())

        # 8) flow direction
        all_errors.extend(self.check_flow_direction())

        return all_errors

    # 1) multipart (interdit)
    def check_multipart_lines(self):
        """
        Signale chaque entité ligne multipart comme erreur.
        Les entités multipart sont enregistrées dans self.multipart_feature_ids et seront ignorées par les autres contrôles.
        """
        errors = []
        for key, layer in self.layers.items():
            try:
                if not layer or layer.geometryType() != QgsWkbTypes.LineGeometry:
                    continue
            except Exception:
                # certains objets layer peuvent lancer
                continue

            multipart_ids = set()
            for feat in layer.getFeatures():
                geom = feat.geometry()
                if geom is None or geom.isEmpty():
                    # géométrie nulle -> on peut signaler aussi
                    errors.append(self.add_error(
                        'Géométrie invalide',
                        f"Feature ID {feat.id()} sur couche {layer.name()} a une géométrie vide ou nulle.",
                        layer.name(),
                        feat.id(),
                        None
                    ))
                    continue

                if geom.isMultipart():
                    multipart_ids.add(feat.id())
                    errors.append(self.add_error(
                        'Entité multipart interdite',
                        f"Feature ID {feat.id()} de {layer.name()} est multipart (interdit).",
                        layer.name(),
                        feat.id(),
                        geom
                    ))

            # stocker pour ignorer ces features plus tard
            if multipart_ids:
                self.multipart_feature_ids[layer.name()] = multipart_ids

        return errors

    # 2) boxes - branches
    def check_connections_boxes_branches(self):
        """
        Pour chaque boîte de branchement : vérifier qu'elle a au moins un branchement connecté (buffer).
        Pour chaque branchement : vérifier que son premier sommet est connecté à une boîte.
        Gère géométries nulles/invalides.
        """
        errors = []
        # on parcourt par réseau (eu/ep/uni) pour appliquer règles similaires
        networks = ['eu', 'ep', 'uni']
        for net in networks:
            box_key = f'box_{net}'
            branch_key = f'branch_{net}'

            box_layer = self.layers.get(box_key)
            branch_layer = self.layers.get(branch_key)

            # si pas de couche, on ignore
            if not box_layer and not branch_layer:
                continue

            # préparer index spatial pour branches (si exist)
            if branch_layer:
                branch_index = self.ensure_index(branch_layer)
            else:
                branch_index = None

            # Vérifier chaque boîte
            if box_layer:
                box_index = self.ensure_index(box_layer)
                for box_feat in box_layer.getFeatures():
                    # vérifier géom
                    geom = box_feat.geometry()
                    if not self.geometry_is_valid(geom):
                        errors.append(self.add_error(
                            'Géométrie invalide',
                            f"Boîte ID {box_feat.id()} sur {box_layer.name()} a géométrie invalide.",
                            box_layer.name(),
                            box_feat.id()
                        ))
                        continue

                    # buffer autour de la boîte et chercher branchements dans l'index des branches
                    buf = geom.buffer(self.connection_tolerance, 5)
                    if branch_layer:
                        # rechercher candidates via index
                        candidate_ids = branch_index.intersects(buf.boundingBox())
                        found = False
                        for cid in candidate_ids:
                            f = branch_layer.getFeature(cid)
                            if f.geometry().intersects(buf):
                                found = True
                                break
                        if not found:
                            errors.append(self.add_error(
                                'Connexion boîtes-branchements',
                                f"Boîte ID {box_feat.id()} sur {box_layer.name()} n'a pas de branchement connecté dans tolérance {self.connection_tolerance}.",
                                box_layer.name(),
                                box_feat.id(),
                                geom
                            ))

            # Vérifier chaque branche : son premier sommet doit être connecté à une boîte
            if branch_layer and box_layer:
                box_index = self.ensure_index(box_layer)
                for br_feat in branch_layer.getFeatures():
                    # ignorer multipart si marqués
                    if branch_layer.name() in self.multipart_feature_ids and br_feat.id() in self.multipart_feature_ids[branch_layer.name()]:
                        continue

                    geom = br_feat.geometry()
                    if not self.geometry_is_valid(geom):
                        errors.append(self.add_error(
                            'Géométrie invalide',
                            f"Branchement ID {br_feat.id()} sur {branch_layer.name()} a géométrie invalide.",
                            branch_layer.name(),
                            br_feat.id()
                        ))
                        continue

                    start_pt, _ = self.get_line_endpoints(geom)
                    if start_pt is None:
                        errors.append(self.add_error(
                            'Connexion boîtes-branchements',
                            f"Branchement ID {br_feat.id()} sur {branch_layer.name()} a pas d'extrémité départ valide.",
                            branch_layer.name(),
                            br_feat.id()
                        ))
                        continue

                    # buffer autour du start_pt et chercher boîte
                    rect = self.bbox_around_point(start_pt)
                    candidate_ids = box_index.intersects(rect)
                    connected = False
                    for cid in candidate_ids:
                        f = box_layer.getFeature(cid)
                        if f.geometry().intersects(QgsGeometry.fromPointXY(QgsPointXY(start_pt)) .buffer(self.connection_tolerance, 5)):
                            connected = True
                            break
                    if not connected:
                        errors.append(self.add_error(
                            'Connexion boîtes-branchements',
                            f"Branchement ID {br_feat.id()} sur {branch_layer.name()} semble ne pas commencer par une boîte (tolérance {self.connection_tolerance}).",
                            branch_layer.name(),
                            br_feat.id(),
                            geom
                        ))

        return errors

    # 3) branches -> réseau / regard / boîte autorisé
    def check_connections_branches_network(self):
        """
        Pour chaque branchement, vérifier que son extrémité est connectée à un réseau/regard/boîte autorisé.
        Règles:
        - Branchement EU peut se connecter sur EU ou UNI (mais pas EP)
        - Branchement EP peut se connecter sur EP ou UNI (mais pas EU)
        - Branchement UNI peut se connecter sur UNI uniquement
        """
        errors = []
        # Définitions autorisées par type de branchement
        allowed_targets = {
            'branch_eu': ['network_eu', 'manhole_eu', 'box_eu', 'network_uni', 'manhole_uni', 'box_uni'],
            'branch_ep': ['network_ep', 'manhole_ep', 'box_ep', 'network_uni', 'manhole_uni', 'box_uni'],
            'branch_uni': ['network_uni', 'manhole_uni', 'box_uni']
        }
        
        # Définir les connexions explicitement interdites
        forbidden_connections = {
            'branch_eu': ['network_ep', 'manhole_ep', 'box_ep'],
            'branch_ep': ['network_eu', 'manhole_eu', 'box_eu']
        }

        for branch_key, targets in allowed_targets.items():
            branch_layer = self.layers.get(branch_key)
            if not branch_layer:
                continue

            # préparer indexes pour toutes les couches cibles
            target_indexes = {}
            target_layers = {}
            for t in targets:
                layer_t = self.layers.get(t)
                if layer_t:
                    target_layers[t] = layer_t
                    target_indexes[t] = self.ensure_index(layer_t)

            # aussi préparer all other layers to detect forbidden connection (simple heuristic)
            for br_feat in branch_layer.getFeatures():
                if branch_layer.name() in self.multipart_feature_ids and br_feat.id() in self.multipart_feature_ids[branch_layer.name()]:
                    continue
                geom = br_feat.geometry()
                if not self.geometry_is_valid(geom):
                    errors.append(self.add_error(
                        'Géométrie invalide',
                        f"Branchement ID {br_feat.id()} sur {branch_layer.name()} géométrie invalide.",
                        branch_layer.name(),
                        br_feat.id()
                    ))
                    continue

                _, end_pt = self.get_line_endpoints(geom)
                if end_pt is None:
                    errors.append(self.add_error(
                        'Connexion branchements-réseau',
                        f"Branchement ID {br_feat.id()} sur {branch_layer.name()} n'a pas d'extrémité valide.",
                        branch_layer.name(),
                        br_feat.id()
                    ))
                    continue

                buf = QgsGeometry.fromPointXY(QgsPointXY(end_pt)).buffer(self.connection_tolerance, 5)
                connected_to_allowed = False

                # Vérifier connexion à une cible autorisée
                for tname, layer_t in target_layers.items():
                    idx = target_indexes[tname]
                    cand_ids = idx.intersects(buf.boundingBox())
                    for cid in cand_ids:
                        f = layer_t.getFeature(cid)
                        if f.geometry().intersects(buf):
                            connected_to_allowed = True
                            break
                    if connected_to_allowed:
                        break

                if not connected_to_allowed:
                    # Vérifier si connecté à une couche explicitement interdite
                    forbidden_targets_list = forbidden_connections.get(branch_key, [])
                    forbidden_conn = None
                    
                    for forbidden_key in forbidden_targets_list:
                        forbidden_layer = self.layers.get(forbidden_key)
                        if not forbidden_layer:
                            continue
                        idx = self.ensure_index(forbidden_layer)
                        cand_ids = idx.intersects(buf.boundingBox())
                        for cid in cand_ids:
                            f = forbidden_layer.getFeature(cid)
                            if f.geometry().intersects(buf):
                                forbidden_conn = forbidden_layer.name()
                                break
                        if forbidden_conn:
                            break

                    if forbidden_conn:
                        errors.append(self.add_error(
                            'Connexion branchements-réseau',
                            f"Branchement ID {br_feat.id()} de {branch_layer.name()} connecté à couche INTERDITE '{forbidden_conn}' (EU?EP).",
                            branch_layer.name(),
                            br_feat.id(),
                            geom
                        ))
                    else:
                        errors.append(self.add_error(
                            'Connexion branchements-réseau',
                            f"Branchement ID {br_feat.id()} de {branch_layer.name()} non connecté à un réseau/regard/boîte autorisé (tol:{self.connection_tolerance}).",
                            branch_layer.name(),
                            br_feat.id(),
                            geom
                        ))
        return errors

    # 4) regards - canalisations
    def check_connections_manholes_pipes(self):
        """
        - Pour chaque regard : vérifier qu'il est connecté à au moins une canalisation.
        - Pour chaque canalisation réseau : vérifier que ses pts de début/fin sont connectés à éléments conformes.
        """
        errors = []
        network_keys = ['network_eu', 'network_ep', 'network_uni']
        manhole_keys = ['manhole_eu', 'manhole_ep', 'manhole_uni']

        # construire index pour network layers
        network_indexes = {}
        for nk in network_keys:
            layer = self.layers.get(nk)
            if layer:
                network_indexes[nk] = self.ensure_index(layer)

        # --- regards connectés à une canalisation
        for mk in manhole_keys:
            man_layer = self.layers.get(mk)
            if not man_layer:
                continue
            # chercher connexion à *n'importe quelle* canalisation réseau (tous les network_keys)
            # construire index combiné? on interroge par bbox sur chaque réseau
            for man_feat in man_layer.getFeatures():
                geom = man_feat.geometry()
                if not self.geometry_is_valid(geom):
                    errors.append(self.add_error(
                        'Géométrie invalide',
                        f"Regard ID {man_feat.id()} sur {man_layer.name()} géométrie invalide.",
                        man_layer.name(),
                        man_feat.id()
                    ))
                    continue
                buf = geom.buffer(self.connection_tolerance, 5)
                connected = False
                for nk, idx in network_indexes.items():
                    layer_net = self.layers.get(nk)
                    cand_ids = idx.intersects(buf.boundingBox())
                    for cid in cand_ids:
                        f = layer_net.getFeature(cid)
                        if f.geometry().intersects(buf):
                            connected = True
                            break
                    if connected:
                        break
                if not connected:
                    errors.append(self.add_error(
                        'Connexion regards-canalisations',
                        f"Regard ID {man_feat.id()} sur {man_layer.name()} non connecté à une canalisation (tol:{self.connection_tolerance}).",
                        man_layer.name(),
                        man_feat.id(),
                        geom
                    ))

        # --- canalisations : vérifier pts début/fin connectés à éléments conformes
        # éléments conformes pour connexion : manhole, overflow, pump, grate, gully, box
        upstream_element_types = ['manhole_eu', 'manhole_ep', 'manhole_uni',
                                  'overflow', 'gully', 'grate', 'box_eu', 'box_ep', 'box_uni', 'pump']
        # créer indexes pour ces éléments s'ils existent
        element_indexes = {}
        element_layers = {}
        for et in upstream_element_types:
            layer = self.layers.get(et)
            if layer:
                element_layers[et] = layer
                element_indexes[et] = self.ensure_index(layer)

        for nk in network_keys:
            net_layer = self.layers.get(nk)
            if not net_layer:
                continue
            for pipe_feat in net_layer.getFeatures():
                # ignorer multipart marqués
                if net_layer.name() in self.multipart_feature_ids and pipe_feat.id() in self.multipart_feature_ids[net_layer.name()]:
                    continue

                geom = pipe_feat.geometry()
                if not self.geometry_is_valid(geom):
                    errors.append(self.add_error(
                        'Géométrie invalide',
                        f"Canalisation ID {pipe_feat.id()} sur {net_layer.name()} géométrie invalide.",
                        net_layer.name(),
                        pipe_feat.id()
                    ))
                    continue

                start_pt, end_pt = self.get_line_endpoints(geom)
                if start_pt is None or end_pt is None:
                    # signaler mais continuer
                    errors.append(self.add_error(
                        'Connexion regards-canalisations',
                        f"Canalisation ID {pipe_feat.id()} sur {net_layer.name()} a extrémités invalides.",
                        net_layer.name(),
                        pipe_feat.id(),
                        geom
                    ))
                    continue

                # fonction locale pour tester connexion d'un point à éléments conformes
                def point_connected_to_elements(pt):
                    buf = QgsGeometry.fromPointXY(QgsPointXY(pt)).buffer(self.connection_tolerance, 5)
                    for et_name, idx in element_indexes.items():
                        l = element_layers[et_name]
                        cand_ids = idx.intersects(buf.boundingBox())
                        for cid in cand_ids:
                            f = l.getFeature(cid)
                            if f.geometry().intersects(buf):
                                return True
                    return False

                if not point_connected_to_elements(start_pt):
                    errors.append(self.add_error(
                        'Connexion regards-canalisations',
                        f"Canalisation ID {pipe_feat.id()} sur {net_layer.name()} : point amont non connecté à élément conforme.",
                        net_layer.name(),
                        pipe_feat.id(),
                        geom
                    ))

                if not point_connected_to_elements(end_pt):
                    errors.append(self.add_error(
                        'Connexion regards-canalisations',
                        f"Canalisation ID {pipe_feat.id()} sur {net_layer.name()} : point aval non connecté à élément conforme.",
                        net_layer.name(),
                        pipe_feat.id(),
                        geom
                    ))

        return errors

    # 5) DO -> canalisations
    def check_connections_do_pipes(self):
        """
        Pour chaque déversoir d'orage (overflow / DO) vérifier qu'il est connecté à au moins une canalisation.
        """
        errors = []
        do_layers = []
        # possible noms : 'overflow' ou 'do'
        for key in ['overflow', 'do', 'déversoir', 'deversoir']:
            layer = self.layers.get(key)
            if layer:
                do_layers.append(layer)

        if not do_layers:
            return errors

        # préparer index des networks
        network_keys = ['network_eu', 'network_ep', 'network_uni']
        network_indexes = {}
        for nk in network_keys:
            l = self.layers.get(nk)
            if l:
                network_indexes[nk] = self.ensure_index(l)

        for do_layer in do_layers:
            for feat in do_layer.getFeatures():
                geom = feat.geometry()
                if not self.geometry_is_valid(geom):
                    errors.append(self.add_error(
                        'Géométrie invalide',
                        f"DO ID {feat.id()} sur {do_layer.name()} géométrie invalide.",
                        do_layer.name(),
                        feat.id()
                    ))
                    continue

                buf = geom.buffer(self.connection_tolerance, 5)
                connected = False
                for nk, idx in network_indexes.items():
                    l = self.layers.get(nk)
                    cand_ids = idx.intersects(buf.boundingBox())
                    for cid in cand_ids:
                        f = l.getFeature(cid)
                        if f.geometry().intersects(buf):
                            connected = True
                            break
                    if connected:
                        break
                if not connected:
                    errors.append(self.add_error(
                        'Connexion DO-canalisation',
                        f"DO ID {feat.id()} sur {do_layer.name()} non connecté à une canalisation (tol:{self.connection_tolerance}).",
                        do_layer.name(),
                        feat.id(),
                        geom
                    ))
        return errors

    # 6) PR (pumps/refoulement) -> canalisations de refoulement
    def check_connections_pr_pipes(self):
        """
        - Vérifie que chaque PR/pump est connecté à au moins une canalisation de refoulement.
        - Vérifie que les canalisations de refoulement commencent par un PR et finissent par un regard.
        IMPORTANT: Ne vérifie QUE si une couche de refoulement spécifique et une couche PR existent.
        """
        errors = []
        
        # Couche pump/PR
        pump_layer = self.layers.get('pump') or self.layers.get('PR') or self.layers.get('posterefoulement')
        
        # Couche de refoulement SPÉCIFIQUE uniquement (pas network_uni générique)
        refoulement_layer = self.layers.get('network_refoulement') or self.layers.get('network_ref') or self.layers.get('network_refo')
        
        # Si pas de couche PR OU pas de couche refoulement spécifique, on ne fait rien
        if not pump_layer or not refoulement_layer:
            return errors
        
        refoulement_layers = [refoulement_layer]

        # Vérifier chaque PR est connecté à au moins une canalisation de refoulement
        pump_index = self.ensure_index(pump_layer)
        for p_feat in pump_layer.getFeatures():
                geom = p_feat.geometry()
                if not self.geometry_is_valid(geom):
                    errors.append(self.add_error(
                        'Géométrie invalide',
                        f"PR ID {p_feat.id()} sur {pump_layer.name()} géométrie invalide.",
                        pump_layer.name(),
                        p_feat.id()
                    ))
                    continue
                buf = geom.buffer(self.connection_tolerance, 5)
                connected = False
                for rl in refoulement_layers:
                    idx = self.ensure_index(rl)
                    cand_ids = idx.intersects(buf.boundingBox())
                    for cid in cand_ids:
                        f = rl.getFeature(cid)
                        if f.geometry().intersects(buf):
                            connected = True
                            break
                    if connected:
                        break
                if not connected:
                    errors.append(self.add_error(
                        'Connexion refoulement-PR-regard',
                        f"PR ID {p_feat.id()} sur {pump_layer.name()} non connecté à une canalisation de refoulement.",
                        pump_layer.name(),
                        p_feat.id(),
                        geom
                    ))

        # Pour chaque canalisation de refoulement : vérifier commence par PR et finit par regard
        manhole_indexes = {}
        manhole_layers = {}
        for mk in ['manhole_eu', 'manhole_ep', 'manhole_uni']:
            l = self.layers.get(mk)
            if l:
                manhole_layers[mk] = l
                manhole_indexes[mk] = self.ensure_index(l)

        for rl in refoulement_layers:
            for feat in rl.getFeatures():
                # ignorer multipart marqués
                if rl.name() in self.multipart_feature_ids and feat.id() in self.multipart_feature_ids[rl.name()]:
                    continue
                geom = feat.geometry()
                if not self.geometry_is_valid(geom):
                    errors.append(self.add_error(
                        'Géométrie invalide',
                        f"Canalisation refoulement ID {feat.id()} sur {rl.name()} géométrie invalide.",
                        rl.name(),
                        feat.id()
                    ))
                    continue

                start_pt, end_pt = self.get_line_endpoints(geom)
                if start_pt is None or end_pt is None:
                    continue

                # Le point de départ doit être connecté à un PR
                start_buf = QgsGeometry.fromPointXY(QgsPointXY(start_pt)).buffer(self.connection_tolerance, 5)
                connected_to_pump = False
                cand_ids = pump_index.intersects(start_buf.boundingBox())
                for cid in cand_ids:
                    f = pump_layer.getFeature(cid)
                    if f.geometry().intersects(start_buf):
                        connected_to_pump = True
                        break
                        
                if not connected_to_pump:
                    errors.append(self.add_error(
                        'Connexion refoulement-PR-regard',
                        f"Canalisation refoulement ID {feat.id()} sur {rl.name()} ne commence pas par un PR.",
                        rl.name(),
                        feat.id(),
                        geom
                    ))

                # Le point d'arrivée doit être connecté à un regard
                end_buf = QgsGeometry.fromPointXY(QgsPointXY(end_pt)).buffer(self.connection_tolerance, 5)
                connected_to_manhole = False
                for mk, idx in manhole_indexes.items():
                    l = manhole_layers[mk]
                    cand_ids = idx.intersects(end_buf.boundingBox())
                    for cid in cand_ids:
                        f = l.getFeature(cid)
                        if f.geometry().intersects(end_buf):
                            connected_to_manhole = True
                            break
                    if connected_to_manhole:
                        break
                        
                if not connected_to_manhole:
                    errors.append(self.add_error(
                        'Connexion refoulement-PR-regard',
                        f"Canalisation refoulement ID {feat.id()} sur {rl.name()} ne finit pas par un regard.",
                        rl.name(),
                        feat.id(),
                        geom
                    ))

        return errors

    # 7) superpositions
    def check_entity_overlaps(self):
        """
        Détecte :
        - overlaps entre canalisations du même type (intra-couche et inter-couches)
        - points (regards/boîtes) trop proches (distance < connection_tolerance)
        Produit géométrie d'intersection pour affichage.
        """
        errors = []

        # Regrouper par familles réseau (eu/ep/uni) comme dans ton code initial
        network_groups = {
            'eu': [layer for key, layer in self.layers.items() if 'eu' in key and layer],
            'ep': [layer for key, layer in self.layers.items() if 'ep' in key and layer],
            'uni': [layer for key, layer in self.layers.items() if 'uni' in key and layer]
        }

        for network_type, layers_group in network_groups.items():
            # lignes
            line_layers = [layer for layer in layers_group if layer.geometryType() == QgsWkbTypes.LineGeometry]
            # intra et inter layer overlaps
            for i, layer1 in enumerate(line_layers):
                # index + features list (pour accès par id)
                idx1 = self.ensure_index(layer1)
                feats1 = {f.id(): f for f in layer1.getFeatures()}

                for fid, f in feats1.items():
                    # ignorer multipart déjà signalés
                    if layer1.name() in self.multipart_feature_ids and fid in self.multipart_feature_ids[layer1.name()]:
                        continue
                    g1 = f.geometry()
                    if not self.geometry_is_valid(g1):
                        continue
                    bbox = g1.boundingBox()
                    cand_ids = idx1.intersects(bbox)
                    for cid in cand_ids:
                        if cid == fid:
                            continue
                        # éviter double rapport  n'utiliser condition fid < cid pour n'ajouter qu'une fois
                        if fid >= cid:
                            continue
                        cf = feats1.get(cid)
                        if cf is None:
                            continue
                        g2 = cf.geometry()
                        if g1.overlaps(g2):  # overlap (pas juste toucher)
                            inter = g1.intersection(g2)
                            errors.append(self.add_error(
                                "Superposition d'entités",
                                f"Canalisation {network_type.upper()} (ID:{fid}) superposée avec canalisation (ID:{cid}) dans {layer1.name()}",
                                layer1.name(),
                                fid,
                                inter
                            ))

                # inter-layer
                for j in range(i + 1, len(line_layers)):
                    layer2 = line_layers[j]
                    idx2 = self.ensure_index(layer2)
                    # parcourir features de layer1 et rechercher dans layer2
                    for feat in layer1.getFeatures():
                        fid = feat.id()
                        if layer1.name() in self.multipart_feature_ids and fid in self.multipart_feature_ids[layer1.name()]:
                            continue
                        g1 = feat.geometry()
                        if not self.geometry_is_valid(g1):
                            continue
                        request = QgsFeatureRequest().setFilterRect(g1.boundingBox())
                        for cf in layer2.getFeatures(request):
                            cid = cf.id()
                            if layer2.name() in self.multipart_feature_ids and cid in self.multipart_feature_ids[layer2.name()]:
                                continue
                            g2 = cf.geometry()
                            if g1.overlaps(g2):
                                inter = g1.intersection(g2)
                                errors.append(self.add_error(
                                    "Superposition d'entités",
                                    f"Canalisation {network_type.upper()} de {layer1.name()} (ID:{fid}) superposée avec canalisation de {layer2.name()} (ID:{cid})",
                                    layer1.name(),
                                    fid,
                                    inter
                                ))

            # points : regards/boîtes
            point_layers = [layer for layer in layers_group if layer.geometryType() == QgsWkbTypes.PointGeometry]
            for i, layer1 in enumerate(point_layers):
                idx1 = self.ensure_index(layer1)
                feats1 = {f.id(): f for f in layer1.getFeatures()}
                for fid, f in feats1.items():
                    g1 = f.geometry()
                    if not self.geometry_is_valid(g1):
                        continue
                    # buffer pour détecter proximité
                    buf = g1.buffer(self.connection_tolerance, 5)
                    cand_ids = idx1.intersects(buf.boundingBox())
                    for cid in cand_ids:
                        if cid == fid:
                            continue
                        # deduplicate: only report once when fid < cid
                        if fid >= cid:
                            continue
                        cf = feats1.get(cid)
                        if cf is None:
                            continue
                        g2 = cf.geometry()
                        if g1.distance(g2) < self.connection_tolerance:
                            errors.append(self.add_error(
                                "Superposition d'entités",
                                f"Point {network_type.upper()} (ID:{fid}) superposé/trop proche avec point (ID:{cid}) dans {layer1.name()}",
                                layer1.name(),
                                fid,
                                g1
                            ))

                # inter-layer points
                for j in range(i + 1, len(point_layers)):
                    layer2 = point_layers[j]
                    idx2 = self.ensure_index(layer2)
                    for feat in layer1.getFeatures():
                        fid = feat.id()
                        g1 = feat.geometry()
                        if not self.geometry_is_valid(g1):
                            continue
                        buf = g1.buffer(self.connection_tolerance, 5)
                        request = QgsFeatureRequest().setFilterRect(buf.boundingBox())
                        for cf in layer2.getFeatures(request):
                            cid = cf.id()
                            g2 = cf.geometry()
                            if g1.distance(g2) < self.connection_tolerance:
                                errors.append(self.add_error(
                                    "Superposition d'entités",
                                    f"Point {network_type.upper()} de {layer1.name()} (ID:{fid}) superposé avec point de {layer2.name()} (ID:{cid})",
                                    layer1.name(),
                                    fid,
                                    g1
                                ))

        return errors

    # 8) sens d'écoulement
    def check_flow_direction(self):
        """
        ANALYSE TOPOLOGIQUE INTELLIGENTE DU RÉSEAU
        
        Vérifie la cohérence du réseau d'assainissement gravitaire en analysant 
        uniquement la géométrie des tracés (sans regards, sans altitudes).
        
        Vérifications effectuées :
        1. Cohérence globale : toutes les canalisations convergent vers un exutoire
        2. PR/STEU isolés : un exutoire sans arrivée est une erreur
        3. Divisions de flux : vérifier que les branches rejoignent le réseau
        4. Branches mortes : cul-de-sac qui ne convergent pas vers un exutoire
        5. Canalisations isolées : tronçons sans connexion au réseau
        """
        from qgis.PyQt.QtWidgets import QApplication
        
        errors = []
        self.log("\n=== VÉRIFICATION TOPOLOGIQUE DU RÉSEAU (ANALYSE INTELLIGENTE) ===")
        QApplication.processEvents()
        
        # Récupérer les couches d'exutoires
        pr_layer = self.layers.get('pump')
        steu_layer = self.layers.get('steu')
        
        self.log(f"Couche PR : {'✓ ' + pr_layer.name() if pr_layer else '✖ Non définie'}")
        self.log(f"Couche STEU : {'✓ ' + steu_layer.name() if steu_layer else '✖ Non définie'}")
        QApplication.processEvents()
        
        if not pr_layer and not steu_layer:
            self.log("✖✖ ATTENTION : Aucun exutoire (PR ou STEU) défini - vérification impossible")
            QApplication.processEvents()
            return errors
        
        # ÉTAPE 1 : Construire le graphe unifié du réseau gravitaire
        self.log(f"\n--- ÉTAPE 1 : CONSTRUCTION DU GRAPHE DE RÉSEAU ---")
        QApplication.processEvents()
        graph_data = self._build_network_graph()
        
        if not graph_data['pipes']:
            self.log("✖✖ Aucune canalisation gravitaire trouvée")
            QApplication.processEvents()
            return errors
        
        self.log(f"✓✓ Graphe construit : {len(graph_data['pipes'])} canalisations, {len(graph_data['nodes'])} nœuds")
        QApplication.processEvents()
        
        # ÉTAPE 2 : Identifier les exutoires du réseau
        self.log(f"\n--- ÉTAPE 2 : IDENTIFICATION DES EXUTOIRES ---")
        QApplication.processEvents()
        outlets_data = self._identify_outlets(graph_data, pr_layer, steu_layer)
        
        self.log(f"✓ {len(outlets_data['outlet_pipes'])} canalisation(s) connectée(s) à des exutoires")
        self.log(f"✓ {len(outlets_data['outlet_nodes'])} nœud(s) exutoire identifié(s)")
        QApplication.processEvents()
        
        # ÉTAPE 3 : Analyser la connectivité du réseau
        self.log(f"\n--- ÉTAPE 3 : ANALYSE DE CONNECTIVITÉ ---")
        QApplication.processEvents()
        connectivity = self._analyze_network_connectivity(graph_data, outlets_data)
        
        self.log(f"✓ Canalisations atteignables : {len(connectivity['reachable'])}/{len(graph_data['pipes'])}")
        self.log(f"✖ Canalisations isolées : {len(connectivity['isolated'])}")
        QApplication.processEvents()
        
        # ÉTAPE 4 : Détecter les anomalies topologiques
        self.log(f"\n--- ÉTAPE 4 : DÉTECTION DES ANOMALIES ---")
        QApplication.processEvents()
        anomalies = self._detect_topological_anomalies(graph_data, outlets_data, connectivity)
        
        self.log(f"Résultats de l'analyse :")
        self.log(f"  - Exutoires isolés : {len(anomalies['isolated_outlets'])}")
        self.log(f"  - Points de rupture (cause racine) : {len(anomalies['break_points'])}")
        self.log(f"  - Canalisations isolées : {len(anomalies['unconnected_pipes'])}")
        self.log(f"  - Divisions suspectes : {len(anomalies['suspicious_splits'])}")
        
        # ÉTAPE 5 : Créer les erreurs
        self.log(f"\n--- ÉTAPE 5 : GÉNÉRATION DES ERREURS ---")
        QApplication.processEvents()
        errors = self._generate_topology_errors(anomalies, graph_data)
        
        self.log(f"  Erreurs générées (avant consolidation) : {len(errors)}")
        flow_errors = sum(1 for e in errors if e['type'] == "Sens d'écoulement")
        self.log(f"    - Par type 'Sens d'écoulement' : {flow_errors}")
        
        self.log(f"\n=== FIN VÉRIFICATION TOPOLOGIQUE ===")
        self.log(f"✖✖ TOTAL : {len(errors)} erreur(s) topologique(s) détectée(s)")
        QApplication.processEvents()
        
        return errors
    
    def _prepare_pipe_cache(self, network_layer):
        """Prépare un cache optimisé avec les points de début et fin de chaque canalisation"""
        cache = {}
        
        for feature in network_layer.getFeatures():
            # Ignorer les multipart
            if network_layer.name() in self.multipart_feature_ids and feature.id() in self.multipart_feature_ids[network_layer.name()]:
                continue
            
            geom = feature.geometry()
            if not self.geometry_is_valid(geom):
                continue
            
            start_pt, end_pt = self.get_line_endpoints(geom)
            if start_pt is None or end_pt is None:
                continue
            
            cache[feature.id()] = {
                'feature': feature,
                'geometry': geom,
                'start_point': start_pt,  # Point amont (début du tracé)
                'end_point': end_pt       # Point aval (fin du tracé)
            }
        
        return cache
    
    def _find_network_outlets(self, network_layer, pipe_cache, spatial_index, pr_layer, steu_layer):
        """Trouve toutes les canalisations connectées aux exutoires (PR ou STEU)"""
        outlets = []
        search_tolerance = self.connection_tolerance
        
        # Chercher les connexions aux PR
        if pr_layer:
            pr_index = self.ensure_index(pr_layer)
            for pr_feature in pr_layer.getFeatures():
                pr_geom = pr_feature.geometry()
                pr_buf = pr_geom.buffer(search_tolerance, 5)
                
                # Trouver les canalisations dont l'extrémité aval touche le PR
                candidate_ids = spatial_index.intersects(pr_buf.boundingBox())
                for pipe_id in candidate_ids:
                    if pipe_id not in pipe_cache:
                        continue
                    pipe_data = pipe_cache[pipe_id]
                    end_buf = QgsGeometry.fromPointXY(QgsPointXY(pipe_data['end_point'])).buffer(search_tolerance, 5)
                    
                    if pr_geom.intersects(end_buf):
                        outlets.append((pipe_id, 'PR'))
        
        # Chercher les connexions aux STEU
        if steu_layer:
            steu_index = self.ensure_index(steu_layer)
            for steu_feature in steu_layer.getFeatures():
                steu_geom = steu_feature.geometry()
                steu_buf = steu_geom.buffer(search_tolerance, 5)
                
                # Trouver les canalisations dont l'extrémité aval touche la STEU
                candidate_ids = spatial_index.intersects(steu_buf.boundingBox())
                for pipe_id in candidate_ids:
                    if pipe_id not in pipe_cache:
                        continue
                    pipe_data = pipe_cache[pipe_id]
                    end_buf = QgsGeometry.fromPointXY(QgsPointXY(pipe_data['end_point'])).buffer(search_tolerance, 5)
                    
                    if steu_geom.intersects(end_buf):
                        outlets.append((pipe_id, 'STEU'))
        
        return outlets
    
    def _trace_network_from_outlet(self, start_pipe_id, network_layer, pipe_cache, spatial_index, point_indexes, point_layers, processed_global):
        """
        Remonte le réseau depuis un exutoire en détectant les inversions.
        Retourne les IDs visités et les tronçons inversés.
        """
        visited = set()
        reversed_pipes = []
        to_process = [(start_pipe_id, False)]  # (pipe_id, is_reversed)
        search_tolerance = self.connection_tolerance
        
        visited.add(start_pipe_id)
        processed_global.add(start_pipe_id)
        
        while to_process:
            current_pipe_id, current_is_reversed = to_process.pop(0)
            
            if current_pipe_id not in pipe_cache:
                continue
            
            current_data = pipe_cache[current_pipe_id]
            
            # Point de recherche pour les connexions amont
            # Si le tronçon est inversé, on cherche depuis son end_point (qui est son "vrai" amont)
            # Sinon, on cherche depuis son start_point (début normal)
            if current_is_reversed:
                search_point = current_data['end_point']
            else:
                search_point = current_data['start_point']
            
            # Créer bbox pour recherche
            bbox = QgsRectangle(
                search_point.x() - search_tolerance,
                search_point.y() - search_tolerance,
                search_point.x() + search_tolerance,
                search_point.y() + search_tolerance
            )
            
            # Chercher les canalisations connectées
            candidate_ids = spatial_index.intersects(bbox)
            
            for candidate_id in candidate_ids:
                # Ne pas retraiter
                if candidate_id in processed_global or candidate_id not in pipe_cache:
                    continue
                
                candidate_data = pipe_cache[candidate_id]
                
                # Calcul de distance pour connexion normale (end_point du candidat vers notre search_point)
                dx_normal = search_point.x() - candidate_data['end_point'].x()
                dy_normal = search_point.y() - candidate_data['end_point'].y()
                distance_normal = (dx_normal * dx_normal + dy_normal * dy_normal) ** 0.5
                
                # Calcul de distance pour connexion inversée (start_point du candidat vers notre search_point)
                dx_reversed = search_point.x() - candidate_data['start_point'].x()
                dy_reversed = search_point.y() - candidate_data['start_point'].y()
                distance_reversed = (dx_reversed * dx_reversed + dy_reversed * dy_reversed) ** 0.5
                
                # Connexion normale : le candidat arrive correctement
                if distance_normal < search_tolerance:
                    visited.add(candidate_id)
                    processed_global.add(candidate_id)
                    to_process.append((candidate_id, False))
                
                # Connexion inversée : le candidat est tracé à l'envers
                elif distance_reversed < search_tolerance:
                    visited.add(candidate_id)
                    processed_global.add(candidate_id)
                    reversed_pipes.append((candidate_id, 'reversed'))
                    to_process.append((candidate_id, True))
        
        return visited, reversed_pipes
    
    def _trace_unified_network(self, start_key, unified_cache, unified_spatial_index, point_indexes, point_layers, processed_global):
        """
        Remonte le réseau unifié (tous les réseaux gravitaires) depuis un exutoire.
        Gère les connexions inter-réseaux (EU→UNI, EP→UNI, etc.)
        
        Args:
            start_key: Clé unifiée de départ (format "network_type_id")
            unified_cache: Cache unifié de toutes les canalisations
            unified_spatial_index: Index spatial unifié
            point_indexes: Indices des couches de points (tous réseaux)
            point_layers: Couches de points (tous réseaux)
            processed_global: Set des clés déjà traitées
        
        Returns:
            (visited, reversed_pipes) - Sets des clés visitées et inversées
        """
        visited = set()
        reversed_pipes = []
        to_process = [(start_key, False)]  # (unified_key, is_reversed)
        search_tolerance = self.connection_tolerance
        
        visited.add(start_key)
        processed_global.add(start_key)
        
        while to_process:
            current_key, current_is_reversed = to_process.pop(0)
            
            if current_key not in unified_cache:
                continue
            
            current_data = unified_cache[current_key]
            
            # Point de recherche pour les connexions amont
            if current_is_reversed:
                search_point = current_data['end_point']
            else:
                search_point = current_data['start_point']
            
            # Créer bbox pour recherche
            bbox = QgsRectangle(
                search_point.x() - search_tolerance,
                search_point.y() - search_tolerance,
                search_point.x() + search_tolerance,
                search_point.y() + search_tolerance
            )
            
            # Chercher les canalisations connectées dans le cache unifié
            for candidate_key, candidate_data in unified_cache.items():
                # Ne pas retraiter
                if candidate_key in processed_global:
                    continue
                
                # Calcul de distance pour connexion normale (end_point du candidat vers notre search_point)
                dx_normal = search_point.x() - candidate_data['end_point'].x()
                dy_normal = search_point.y() - candidate_data['end_point'].y()
                distance_normal = (dx_normal * dx_normal + dy_normal * dy_normal) ** 0.5
                
                # Calcul de distance pour connexion inversée (start_point du candidat vers notre search_point)
                dx_reversed = search_point.x() - candidate_data['start_point'].x()
                dy_reversed = search_point.y() - candidate_data['start_point'].y()
                distance_reversed = (dx_reversed * dx_reversed + dy_reversed * dy_reversed) ** 0.5
                
                # Connexion normale : le candidat arrive correctement
                if distance_normal < search_tolerance:
                    visited.add(candidate_key)
                    processed_global.add(candidate_key)
                    to_process.append((candidate_key, False))
                
                # Connexion inversée : le candidat est tracé à l'envers
                elif distance_reversed < search_tolerance:
                    visited.add(candidate_key)
                    processed_global.add(candidate_key)
                    reversed_pipes.append(candidate_key)
                    to_process.append((candidate_key, True))
        
        return visited, reversed_pipes
    
    def _build_network_graph(self):
        """
        Construit un graphe unifié du réseau gravitaire (EU, UNI, EP).
        
        Returns:
            dict avec :
            - 'pipes': {unified_key: {pipe_data, layer, original_id}}
            - 'nodes': {node_key: {coordinates, connected_pipes}}
            - 'adjacency': {unified_key: [connected_keys]}
        """
        from qgis.PyQt.QtWidgets import QApplication
        
        self.log("Construction du graphe de réseau...")
        QApplication.processEvents()
        
        pipes = {}  # Toutes les canalisations
        nodes = {}  # Tous les nœuds (points de connexion)
        adjacency = {}  # Liste d'adjacence pour le graphe
        tolerance = self.connection_tolerance
        
        # Charger toutes les canalisations gravitaires
        for network_type in ['network_eu', 'network_uni', 'network_ep']:
            network_layer = self.layers.get(network_type)
            if not network_layer:
                continue
            
            pipe_cache = self._prepare_pipe_cache(network_layer)
            self.log(f"  {network_type.upper()}: {len(pipe_cache)} canalisations")
            
            for pipe_id, pipe_data in pipe_cache.items():
                unified_key = f"{network_type}_{pipe_id}"
                pipes[unified_key] = {
                    'data': pipe_data,
                    'layer': network_layer,
                    'original_id': pipe_id,
                    'network_type': network_type
                }
                adjacency[unified_key] = {'upstream': [], 'downstream': []}
                
                # Créer/mettre à jour les nœuds
                start_node = self._get_node_key(pipe_data['start_point'], tolerance)
                end_node = self._get_node_key(pipe_data['end_point'], tolerance)
                
                if start_node not in nodes:
                    nodes[start_node] = {
                        'point': pipe_data['start_point'],
                        'pipes_in': [],   # Tuyaux qui arrivent ici (end_point)
                        'pipes_out': []   # Tuyaux qui partent d'ici (start_point)
                    }
                nodes[start_node]['pipes_out'].append(unified_key)
                
                if end_node not in nodes:
                    nodes[end_node] = {
                        'point': pipe_data['end_point'],
                        'pipes_in': [],
                        'pipes_out': []
                    }
                nodes[end_node]['pipes_in'].append(unified_key)
        
        # Construire la liste d'adjacence (connexions entre tuyaux)
        for unified_key, pipe_info in pipes.items():
            pipe_data = pipe_info['data']
            start_node = self._get_node_key(pipe_data['start_point'], tolerance)
            end_node = self._get_node_key(pipe_data['end_point'], tolerance)
            
            # En amont : tuyaux dont le end_point arrive au start_point de ce tuyau
            adjacency[unified_key]['upstream'] = [k for k in nodes[start_node]['pipes_in'] if k != unified_key]
            
            # En aval : tuyaux dont le start_point part du end_point de ce tuyau
            adjacency[unified_key]['downstream'] = [k for k in nodes[end_node]['pipes_out'] if k != unified_key]
        
        self.log(f"✓ Graphe construit: {len(pipes)} tuyaux, {len(nodes)} nœuds")
        
        # DIAGNOSTIC : Statistiques par type de réseau
        eu_count = sum(1 for k in pipes.keys() if k.startswith('network_eu_'))
        uni_count = sum(1 for k in pipes.keys() if k.startswith('network_uni_'))
        ep_count = sum(1 for k in pipes.keys() if k.startswith('network_ep_'))
        self.log(f"  Répartition: EU={eu_count}, UNI={uni_count}, EP={ep_count}")
        
        # DIAGNOSTIC : Vérifier les connexions inter-réseaux
        inter_network_connections = 0
        for pipe_key, adj in adjacency.items():
            pipe_network = pipe_key.split('_')[0] + '_' + pipe_key.split('_')[1]  # ex: network_eu
            for downstream_key in adj['downstream']:
                downstream_network = downstream_key.split('_')[0] + '_' + downstream_key.split('_')[1]
                if pipe_network != downstream_network:
                    inter_network_connections += 1
                    self.log(f"  Connexion inter-réseau: {pipe_network} → {downstream_network} (tuyau {pipe_key})")
        self.log(f"  Total connexions inter-réseaux: {inter_network_connections}")
        
        QApplication.processEvents()
        
        return {'pipes': pipes, 'nodes': nodes, 'adjacency': adjacency}
    
    def _get_node_key(self, point, tolerance):
        """Génère une clé unique pour un nœud avec tolérance spatiale."""
        # Arrondir les coordonnées selon la tolérance
        x = round(point.x() / tolerance) * tolerance
        y = round(point.y() / tolerance) * tolerance
        return f"{x:.3f}_{y:.3f}"
    
    def _identify_outlets(self, graph_data, pr_layer, steu_layer):
        """
        Identifie les nœuds et canalisations connectés aux exutoires (PR/STEU).
        
        Returns:
            dict avec :
            - 'outlet_nodes': set des nœuds exutoires
            - 'outlet_pipes': {unified_key: outlet_type}
            - 'outlet_points': {node_key: outlet_type}
        """
        outlet_nodes = set()
        outlet_pipes = {}
        outlet_points = {}
        tolerance = self.connection_tolerance
        
        # Chercher les connexions aux PR
        if pr_layer:
            for pr_feat in pr_layer.getFeatures():
                pr_geom = pr_feat.geometry()
                if not pr_geom or pr_geom.isEmpty():
                    continue
                
                pr_point = pr_geom.asPoint()
                node_key = self._get_node_key(pr_point, tolerance)
                
                # Chercher le nœud le plus proche
                for nk, node_data in graph_data['nodes'].items():
                    dist = pr_point.distance(node_data['point'])
                    if dist < tolerance:
                        outlet_nodes.add(nk)
                        outlet_points[nk] = 'PR'
                        # Marquer les tuyaux qui arrivent à ce nœud
                        for pipe_key in node_data['pipes_in']:
                            if pipe_key not in outlet_pipes:
                                outlet_pipes[pipe_key] = 'PR'
        
        # Chercher les connexions aux STEU
        if steu_layer:
            for steu_feat in steu_layer.getFeatures():
                steu_geom = steu_feat.geometry()
                if not steu_geom or steu_geom.isEmpty():
                    continue
                
                steu_point = steu_geom.asPoint()
                
                # Chercher le nœud le plus proche
                for nk, node_data in graph_data['nodes'].items():
                    dist = steu_point.distance(node_data['point'])
                    if dist < tolerance:
                        outlet_nodes.add(nk)
                        outlet_points[nk] = 'STEU'
                        # Marquer les tuyaux qui arrivent à ce nœud
                        for pipe_key in node_data['pipes_in']:
                            if pipe_key not in outlet_pipes:
                                outlet_pipes[pipe_key] = 'STEU'
        
        self.log(f"  Nœuds exutoires: {len(outlet_nodes)}")
        self.log(f"  Tuyaux vers exutoires: {len(outlet_pipes)}")
        
        # DIAGNOSTIC : Types de réseaux connectés aux exutoires
        for pipe_key, outlet_type in outlet_pipes.items():
            network_type = pipe_key.split('_')[0] + '_' + pipe_key.split('_')[1]
            self.log(f"    {network_type} connecté à {outlet_type}")
        
        # DIAGNOSTIC : Vérifier si certaines canalisations sont proches d'exutoires mais non connectées
        suspect_pipes = ['network_uni_32']  # Canalisations suspectes à vérifier
        for pipe_key in suspect_pipes:
            if pipe_key in graph_data['pipes']:
                pipe_info = graph_data['pipes'][pipe_key]
                pipe_data = pipe_info['data']
                end_point = pipe_data['end_point']
                
                self.log(f"  DIAGNOSTIC {pipe_key}:")
                self.log(f"    Point final: ({end_point.x():.2f}, {end_point.y():.2f})")
                
                # Chercher les PR/STEU proches
                min_dist_pr = float('inf')
                min_dist_steu = float('inf')
                
                if pr_layer:
                    for pr_feat in pr_layer.getFeatures():
                        pr_point = pr_feat.geometry().asPoint()
                        dist = end_point.distance(pr_point)
                        if dist < min_dist_pr:
                            min_dist_pr = dist
                
                if steu_layer:
                    for steu_feat in steu_layer.getFeatures():
                        steu_point = steu_feat.geometry().asPoint()
                        dist = end_point.distance(steu_point)
                        if dist < min_dist_steu:
                            min_dist_steu = dist
                
                self.log(f"    Distance au PR le plus proche: {min_dist_pr:.3f}m (tolérance: {tolerance}m)")
                self.log(f"    Distance à STEU la plus proche: {min_dist_steu:.3f}m (tolérance: {tolerance}m)")
                
                if min_dist_pr < 1.0 or min_dist_steu < 1.0:
                    self.log(f"    ⚠️ ATTENTION: Exutoire à moins de 1m mais pas connecté!")
        
        return {
            'outlet_nodes': outlet_nodes,
            'outlet_pipes': outlet_pipes,
            'outlet_points': outlet_points
        }
    
    def _analyze_network_connectivity(self, graph_data, outlets_data):
        """
        Analyse la connectivité du réseau depuis les exutoires.
        
        Returns:
            dict avec :
            - 'reachable': set des tuyaux atteignables depuis les exutoires
            - 'isolated': set des tuyaux isolés
            - 'dead_ends': set des branches mortes
            - 'paths': {pipe_key: path_to_outlet}
        """
        reachable = set()
        paths = {}
        
        # Parcourir le réseau depuis chaque exutoire EN REMONTANT
        to_process = list(outlets_data['outlet_pipes'].keys())
        processed = set()
        
        # DIAGNOSTIC : Canalisations de test à surveiller
        test_pipes = ['network_eu_301', 'network_eu_308']
        
        self.log(f"  Départ du parcours depuis {len(to_process)} exutoire(s)...")
        for test_pipe in test_pipes:
            if test_pipe in to_process:
                self.log(f"  ✓ {test_pipe} est un exutoire direct")
        
        while to_process:
            current_key = to_process.pop(0)
            if current_key in processed:
                continue
            
            processed.add(current_key)
            reachable.add(current_key)
            
            # Remonter en amont (tuyaux qui arrivent au start_point)
            upstream_pipes = graph_data['adjacency'][current_key]['upstream']
            
            # DIAGNOSTIC : Pour les canalisations de test
            for test_pipe in test_pipes:
                if test_pipe == current_key:
                    self.log(f"  → Traitement de {test_pipe}, {len(upstream_pipes)} voisin(s) amont")
                if test_pipe in upstream_pipes:
                    self.log(f"  → {test_pipe} trouvé en amont de {current_key}, ajout à la file")
            
            for upstream_key in upstream_pipes:
                if upstream_key not in processed:
                    to_process.append(upstream_key)
                    if upstream_key not in paths:
                        paths[upstream_key] = current_key
        
        # Identifier les tuyaux isolés
        all_pipes = set(graph_data['pipes'].keys())
        isolated = all_pipes - reachable
        
        # DIAGNOSTIC : Vérifier les canalisations de test
        for test_pipe in test_pipes:
            if test_pipe in graph_data['pipes']:
                is_reachable = test_pipe in reachable
                self.log(f"  {test_pipe}: {'✓ ACCESSIBLE' if is_reachable else '✖ ISOLÉ'}")
                if not is_reachable:
                    # Vérifier les connexions
                    adj = graph_data['adjacency'][test_pipe]
                    self.log(f"    Amont: {len(adj['upstream'])} connexion(s)")
                    self.log(f"    Aval: {len(adj['downstream'])} connexion(s)")
                    if adj['downstream']:
                        self.log(f"    Connecté en aval à: {adj['downstream'][:3]}")
                        
                        # Tracer la chaîne descendante pour trouver la rupture
                        self.log(f"    Traçage de la chaîne descendante:")
                        current = test_pipe
                        visited_chain = set()
                        max_depth = 20
                        depth = 0
                        
                        while depth < max_depth and current not in visited_chain:
                            visited_chain.add(current)
                            downstream = graph_data['adjacency'][current]['downstream']
                            
                            if not downstream:
                                self.log(f"      [{depth}] {current} → FIN (pas de connexion aval)")
                                break
                            
                            next_pipe = downstream[0]
                            is_next_reachable = next_pipe in reachable
                            status = '✓' if is_next_reachable else '✖'
                            self.log(f"      [{depth}] {current} → {next_pipe} {status}")
                            
                            if is_next_reachable:
                                self.log(f"      → RUPTURE TROUVÉE: {next_pipe} est accessible mais {current} ne l'est pas!")
                                break
                            
                            current = next_pipe
                            depth += 1
                        
                        if depth >= max_depth:
                            self.log(f"      → Profondeur max atteinte (boucle?)")
        
        # DIAGNOSTIC : Statistiques de connectivité par réseau
        self.log(f"  Canalisations accessibles: {len(reachable)}")
        self.log(f"  Canalisations isolées: {len(isolated)}")
        
        reachable_eu = sum(1 for k in reachable if k.startswith('network_eu_'))
        reachable_uni = sum(1 for k in reachable if k.startswith('network_uni_'))
        reachable_ep = sum(1 for k in reachable if k.startswith('network_ep_'))
        self.log(f"    Accessibles: EU={reachable_eu}, UNI={reachable_uni}, EP={reachable_ep}")
        
        isolated_eu = sum(1 for k in isolated if k.startswith('network_eu_'))
        isolated_uni = sum(1 for k in isolated if k.startswith('network_uni_'))
        isolated_ep = sum(1 for k in isolated if k.startswith('network_ep_'))
        self.log(f"    Isolées: EU={isolated_eu}, UNI={isolated_uni}, EP={isolated_ep}")
        
        # Note : Les branches mortes (dead_ends) ne sont PAS des erreurs !
        # Ce sont des extrémités normales du réseau (bout de rue, dernier branchement, etc.)
        # Tant qu'elles convergent vers un exutoire (dans reachable), c'est OK.
        
        return {
            'reachable': reachable,
            'isolated': isolated,
            'paths': paths
        }
    
    def _find_network_break_points(self, graph_data, reachable_pipes, isolated_pipes):
        """
        Identifie les points de rupture du réseau - canalisations isolées qui ont une 
        connexion physique au réseau accessible, indiquant qu'elles sont la SOURCE du problème.
        
        Args:
            graph_data: Structure du graphe
            reachable_pipes: Ensemble des clés de canalisations accessibles
            isolated_pipes: Ensemble des clés de canalisations isolées
            
        Returns:
            set: Ensemble des clés de canalisations qui sont des points de rupture
        """
        break_points = set()
        nodes = graph_data['nodes']
        pipes_dict = graph_data['pipes']
        tolerance = self.connection_tolerance
        
        # Pour chaque canalisation isolée, vérifier si elle a une connexion physique 
        # au réseau accessible
        for pipe_key in isolated_pipes:
            pipe_info = pipes_dict[pipe_key]
            pipe_data = pipe_info['data']
            
            # Vérifier le point de fin (downstream)
            end_point = pipe_data['end_point']
            end_node_key = self._get_node_key(end_point, tolerance)
            
            # Si le nœud de fin existe et contient des canalisations accessibles en aval
            if end_node_key in nodes:
                node_data = nodes[end_node_key]
                # Vérifier si des canalisations accessibles partent de ce nœud
                for connected_pipe_key in node_data['pipes_out']:
                    if connected_pipe_key in reachable_pipes and connected_pipe_key != pipe_key:
                        # Cette canalisation isolée est connectée au réseau accessible
                        # Elle est probablement inversée ou mal raccordée
                        break_points.add(pipe_key)
                        break
                
                # Vérifier également les canalisations qui arrivent à ce nœud
                if pipe_key not in break_points:
                    for connected_pipe_key in node_data['pipes_in']:
                        if connected_pipe_key in reachable_pipes and connected_pipe_key != pipe_key:
                            break_points.add(pipe_key)
                            break
        
        # Si on n'a pas trouvé de points de rupture clairs, essayer une approche alternative:
        # trouver les canalisations accessibles qui ont des voisins isolés en amont
        if not break_points:
            for pipe_key in reachable_pipes:
                pipe_info = pipes_dict[pipe_key]
                pipe_data = pipe_info['data']
                
                # Vérifier le point de début (upstream)
                start_point = pipe_data['start_point']
                start_node_key = self._get_node_key(start_point, tolerance)
                
                if start_node_key in nodes:
                    node_data = nodes[start_node_key]
                    # Vérifier si des canalisations isolées arrivent à ce nœud
                    for connected_pipe_key in node_data['pipes_in']:
                        if connected_pipe_key in isolated_pipes:
                            # La canalisation isolée qui se connecte ici est probablement le problème
                            break_points.add(connected_pipe_key)
        
        return break_points
    
    def _detect_topological_anomalies(self, graph_data, outlets_data, connectivity):
        """
        Détecte les anomalies topologiques dans le réseau.
        Identifie les CAUSES RACINES des problèmes, pas les conséquences.
        
        Returns:
            dict avec différents types d'anomalies
        """
        anomalies = {
            'isolated_outlets': [],
            'reversed_pipes': [],
            'suspicious_splits': [],
            'unconnected_pipes': [],
            'break_points': []  # Points de rupture du réseau
        }
        
        # 1. Exutoires isolés (PR/STEU sans arrivée)
        for node_key in outlets_data['outlet_nodes']:
            node_data = graph_data['nodes'][node_key]
            if len(node_data['pipes_in']) == 0:
                anomalies['isolated_outlets'].append({
                    'node': node_key,
                    'type': outlets_data['outlet_points'].get(node_key, 'INCONNU'),
                    'point': node_data['point']
                })
        
        # 2. Identifier les points de rupture (canalisations à la frontière)
        # Ce sont les canalisations qui, si elles étaient bien connectées,
        # permettraient aux canalisations amont d'atteindre les exutoires
        break_points = self._find_network_break_points(
            graph_data, 
            connectivity['reachable'], 
            connectivity['isolated']
        )
        
        # 3. Pour les canalisations isolées, ne signaler QUE les points de rupture
        if break_points:
            # Il y a des points de rupture identifiés = problème de connexion localisé
            for pipe_key in break_points:
                pipe_info = graph_data['pipes'][pipe_key]
                anomalies['break_points'].append({
                    'key': pipe_key,
                    'layer': pipe_info['layer'],
                    'id': pipe_info['original_id'],
                    'geometry': pipe_info['data']['geometry']
                })
        else:
            # Pas de point de rupture = les canalisations sont vraiment isolées
            for pipe_key in connectivity['isolated']:
                pipe_info = graph_data['pipes'][pipe_key]
                anomalies['unconnected_pipes'].append({
                    'key': pipe_key,
                    'layer': pipe_info['layer'],
                    'id': pipe_info['original_id'],
                    'geometry': pipe_info['data']['geometry']
                })
        
        # 4. Divisions suspectes (un tuyau qui part vers plusieurs directions)
        for pipe_key, pipe_info in graph_data['pipes'].items():
            downstream = graph_data['adjacency'][pipe_key]['downstream']
            if len(downstream) > 1:
                # Vérifier si les branches rejoignent le réseau
                all_reach_outlet = all(
                    branch_key in connectivity['reachable']
                    for branch_key in downstream
                )
                if not all_reach_outlet:
                    anomalies['suspicious_splits'].append({
                        'key': pipe_key,
                        'layer': pipe_info['layer'],
                        'id': pipe_info['original_id'],
                        'branches': downstream,
                        'geometry': pipe_info['data']['geometry']
                    })
        
        # 5. Inversions potentielles (à affiner avec plus de logique)
        # Pour l'instant, on ne peut pas détecter sans altitudes
        
        return anomalies
    
    def _generate_topology_errors(self, anomalies, graph_data):
        """Génère les erreurs à partir des anomalies détectées avec déduplication."""
        errors = []
        processed_pipes = set()  # Pour éviter les doublons (layer_id, pipe_id)
        
        # Exutoires isolés
        for outlet_anomaly in anomalies['isolated_outlets']:
            errors.append({
                'type': 'Sens d\'écoulement',
                'description': f"Exutoire isolé ({outlet_anomaly['type']}) : aucune canalisation n'arrive à ce point",
                'layer': outlet_anomaly['type'],
                'feature_id': None,
                'geometry': QgsGeometry.fromPointXY(outlet_anomaly['point'])
            })
        
        # Points de rupture du réseau (CAUSE RACINE)
        for pipe_anomaly in anomalies['break_points']:
            pipe_key = (pipe_anomaly['layer'].id(), pipe_anomaly['id'])
            if pipe_key in processed_pipes:
                continue
            processed_pipes.add(pipe_key)
            
            errors.append(self.add_error(
                'Sens d\'écoulement',
                f"Point de rupture du réseau : ID {pipe_anomaly['id']} ({pipe_anomaly['layer'].name()}). Cette canalisation bloque l'accès aux exutoires pour le réseau en amont.",
                pipe_anomaly['layer'].name(),
                pipe_anomaly['id'],
                pipe_anomaly['geometry']
            ))
        
        # Canalisations vraiment isolées (pas de connexion du tout)
        for pipe_anomaly in anomalies['unconnected_pipes']:
            pipe_key = (pipe_anomaly['layer'].id(), pipe_anomaly['id'])
            if pipe_key in processed_pipes:
                continue
            processed_pipes.add(pipe_key)
            
            errors.append(self.add_error(
                'Sens d\'écoulement',
                f"Tronçon isolé : ID {pipe_anomaly['id']} ({pipe_anomaly['layer'].name()}). Aucune connexion au réseau détectée.",
                pipe_anomaly['layer'].name(),
                pipe_anomaly['id'],
                pipe_anomaly['geometry']
            ))
        
        # Divisions suspectes - regrouper pour éviter les doublons
        splits_by_pipe = {}
        for split in anomalies['suspicious_splits']:
            pipe_key = (split['layer'].id(), split['id'])
            if pipe_key not in splits_by_pipe:
                splits_by_pipe[pipe_key] = split
        
        for pipe_key, split in splits_by_pipe.items():
            if pipe_key in processed_pipes:
                continue
            processed_pipes.add(pipe_key)
            
            errors.append(self.add_error(
                'Sens d\'écoulement',
                f"Division de flux suspecte : ID {split['id']} ({split['layer'].name()}). Une ou plusieurs branches ne rejoignent pas le réseau.",
                split['layer'].name(),
                split['id'],
                split['geometry']
            ))
        
        return errors
    
    def _has_connection_to_points(self, buf_geom, point_layers, point_indexes):
        """Vérifie si le buffer intersecte des points (regards/boîtes)."""
        for i, pt_layer in enumerate(point_layers):
            if point_indexes[i]:
                cand_ids = point_indexes[i].intersects(buf_geom.boundingBox())
                for cid in cand_ids:
                    f = pt_layer.getFeature(cid)
                    if f.geometry().intersects(buf_geom):
                        return True
        return False
    
    def _has_connection_to_layer(self, buf_geom, layer, index):
        """Vérifie si le buffer intersecte une couche donnée."""
        if not layer or not index:
            return False
        cand_ids = index.intersects(buf_geom.boundingBox())
        for cid in cand_ids:
            f = layer.getFeature(cid)
            if f.geometry().intersects(buf_geom):
                return True
        return False
    
    def _count_connected_pipes(self, buf_geom, spatial_index, network_layer, current_pipe_id, pipe_cache):
        """Compte le nombre de canalisations connectées au point (buffer)."""
        count = 0
        cand_ids = spatial_index.intersects(buf_geom.boundingBox())
        for cid in cand_ids:
            if cid == current_pipe_id or cid not in pipe_cache:
                continue
            pipe_data = pipe_cache[cid]
            if pipe_data['geometry'].intersects(buf_geom):
                count += 1
        return count

    def check_coherence_altitudes(self):
        """
        Vérifie la cohérence des altitudes entre canalisations et points.
        Utilise la configuration CSV pour les noms de champs selon le MO.
        """
        erreurs = []
        self.log("\n=== VÉRIFICATION COHÉRENCE DES ALTITUDES ===")
        self.log(f"Configuration MO : {self.mo}")
        
        def get_altitude_field(layer):
            """Trouve le premier champ d'altitude disponible dans la couche."""
            for fld in layer.fields():
                if fld.name() in self.altitude_config['champs_point']:
                    return fld.name()
            return None

        CHAMP_ALTITUDE_AMONT = self.altitude_config['champ_amont']
        CHAMP_ALTITUDE_AVAL = self.altitude_config['champ_aval']
        tolerance = 0.20  # marge d'erreur en mètres
        
        self.log(f"Champ altitude amont : {CHAMP_ALTITUDE_AMONT}")
        self.log(f"Champ altitude aval : {CHAMP_ALTITUDE_AVAL}")
        self.log(f"Champs altitude points : {', '.join(self.altitude_config['champs_point'])}")
        self.log(f"Tolérance : {tolerance} m")
        
        def has_field(layer, field_name):
            """Vérifie si un champ existe dans une couche."""
            return field_name in [f.name() for f in layer.fields()]
        
        # Mapping des couches réseau vers leurs points correspondants
        network_to_points_mapping = {
            'network_eu': 'manhole_eu',
            'network_ep': 'manhole_ep',
            'network_uni': 'manhole_uni',
            'network_refoulement': 'manhole_uni',  # Refoulement utilise regards UNI généralement
            'branch_eu': 'box_eu',
            'branch_ep': 'box_ep',
            'branch_uni': 'box_uni'
        }
        
        total_checked = 0
        total_errors = 0

        for clef_couche, couche_ligne in self.layers.items():
            # Ne traiter que les couches de lignes
            if not couche_ligne or couche_ligne.geometryType() != QgsWkbTypes.LineGeometry:
                continue
            
            # Ne vérifier que les couches réseau/branchement
            if clef_couche not in network_to_points_mapping:
                continue
            
            self.log(f"\n--- Analyse {clef_couche} ({couche_ligne.name()}) ---")

            # Identifier la couche de points correspondante
            clef_points = network_to_points_mapping.get(clef_couche)
            couche_points = self.layers.get(clef_points)
            
            if not couche_points:
                self.log(f"?? Couche de points {clef_points} non définie, ignorée")
                continue
            
            self.log(f"? Couche de points : {couche_points.name()}")

            # Vérifier que les champs d'altitude existent dans la couche de lignes
            if not has_field(couche_ligne, CHAMP_ALTITUDE_AMONT):
                champs_disponibles = ', '.join([f.name() for f in couche_ligne.fields()])
                self.log(f"? Champ '{CHAMP_ALTITUDE_AMONT}' non trouvé")
                self.log(f"   Champs disponibles: {champs_disponibles}")
                self.error_id += 1
                erreurs.append({
                    'id': self.error_id,
                    'type': 'Champ manquant',
                    'description': f"Champ '{CHAMP_ALTITUDE_AMONT}' non trouvé dans {couche_ligne.name()}. Champs disponibles: {champs_disponibles}",
                    'layer': couche_ligne.name(),
                    'feature_id': None,
                    'geometry': None
                })
                continue
            
            if not has_field(couche_ligne, CHAMP_ALTITUDE_AVAL):
                champs_disponibles = ', '.join([f.name() for f in couche_ligne.fields()])
                self.log(f"? Champ '{CHAMP_ALTITUDE_AVAL}' non trouvé")
                self.log(f"   Champs disponibles: {champs_disponibles}")
                self.error_id += 1
                erreurs.append({
                    'id': self.error_id,
                    'type': 'Champ manquant',
                    'description': f"Champ '{CHAMP_ALTITUDE_AVAL}' non trouvé dans {couche_ligne.name()}. Champs disponibles: {champs_disponibles}",
                    'layer': couche_ligne.name(),
                    'feature_id': None,
                    'geometry': None
                })
                continue

            # Vérifier le champ altitude pour la couche de points
            CHAMP_ALTITUDE_POINT = get_altitude_field(couche_points)
            if CHAMP_ALTITUDE_POINT is None:
                self.log(f"? Aucun champ d'altitude trouvé dans {couche_points.name()}")
                self.error_id += 1
                erreurs.append({
                    'id': self.error_id,
                    'type': 'Champ manquant',
                    'description': f"Aucun champ d'altitude trouvé dans la couche {couche_points.name()}.",
                    'layer': couche_points.name(),
                    'feature_id': None,
                    'geometry': None
                })
                continue
            
            self.log(f"? Champ altitude points : {CHAMP_ALTITUDE_POINT}")
            
            # Index spatial des points
            index_points = QgsSpatialIndex(couche_points.getFeatures())
            
            layer_checked = 0
            layer_errors = 0

            for canalisation in couche_ligne.getFeatures():
                geom_canal = canalisation.geometry()
                id_canalisation = canalisation.id()
                
                # Récupérer et convertir les altitudes en float
                altitude_amont_raw = canalisation[CHAMP_ALTITUDE_AMONT]
                altitude_aval_raw = canalisation[CHAMP_ALTITUDE_AVAL]
                
                # Convertir en float si non nul
                try:
                    altitude_amont = float(altitude_amont_raw) if altitude_amont_raw is not None else None
                except (ValueError, TypeError):
                    altitude_amont = None
                    
                try:
                    altitude_aval = float(altitude_aval_raw) if altitude_aval_raw is not None else None
                except (ValueError, TypeError):
                    altitude_aval = None

                if altitude_amont is None or altitude_aval is None:
                    erreurs.append(self.add_error(
                        'Altitude manquante',
                        f"Canalisation ID {id_canalisation} sans altitude amont ou aval.",
                        couche_ligne.name(),
                        id_canalisation,
                        geom_canal
                    ))
                    continue

                # Géométrie
                if geom_canal.isMultipart():
                    polyline = geom_canal.asMultiPolyline()[0]
                else:
                    polyline = geom_canal.asPolyline()
                if not polyline:
                    continue

                point_debut = polyline[0]
                point_fin = polyline[-1]

                # Fonction pour trouver le point le plus proche
                def trouver_point_proche(pt):
                    zone_recherche = QgsRectangle(pt.x() - 1, pt.y() - 1, pt.x() + 1, pt.y() + 1)
                    candidats = index_points.intersects(zone_recherche)
                    point_plus_proche = None
                    distance_min = float('inf')
                    for cand in candidats:
                        f = couche_points.getFeature(cand)
                        dist = QgsGeometry.fromPointXY(pt).distance(f.geometry())
                        if dist < distance_min:
                            point_plus_proche = f
                            distance_min = dist
                    return point_plus_proche

                point_amont = trouver_point_proche(point_debut)
                point_aval = trouver_point_proche(point_fin)

                if point_amont:
                    altitude_point_amont_raw = point_amont[CHAMP_ALTITUDE_POINT]
                    try:
                        altitude_point_amont = float(altitude_point_amont_raw) if altitude_point_amont_raw is not None else None
                    except (ValueError, TypeError):
                        altitude_point_amont = None
                    
                    if altitude_point_amont is not None and abs(altitude_point_amont - altitude_amont) > tolerance:
                        layer_errors += 1
                        erreurs.append(self.add_error(
                            'Incohérence altitude amont',
                            f"Canalisation {id_canalisation} : ALDEP={altitude_amont} différent de COORLAMZ={altitude_point_amont}",
                            couche_ligne.name(),
                            id_canalisation,
                            geom_canal
                        ))

                if point_aval:
                    altitude_point_aval_raw = point_aval[CHAMP_ALTITUDE_POINT]
                    try:
                        altitude_point_aval = float(altitude_point_aval_raw) if altitude_point_aval_raw is not None else None
                    except (ValueError, TypeError):
                        altitude_point_aval = None
                    
                    if altitude_point_aval is not None and abs(altitude_point_aval - altitude_aval) > tolerance:
                        layer_errors += 1
                        erreurs.append(self.add_error(
                            'Incohérence altitude aval',
                            f"Canalisation {id_canalisation} : ALTPIQ={altitude_aval} différent de COORLAMZ={altitude_point_aval}",
                            couche_ligne.name(),
                            id_canalisation,
                            geom_canal
                        ))

                if altitude_amont <= altitude_aval:
                    erreurs.append(self.add_error(
                        'Sens d\'écoulement incorrect',
                        f"Canalisation {id_canalisation} : ALDEP {altitude_amont} <= ALTPIQ {altitude_aval}",
                        couche_ligne.name(),
                        id_canalisation,
                        geom_canal
                    ))
                
                layer_checked += 1
                total_checked += 1
            
            # Résumé pour cette couche
            self.log(f"?? {layer_checked} canalisation(s) vérifiée(s), {layer_errors} erreur(s)")
            total_errors += layer_errors

        self.log(f"\n=== FIN VÉRIFICATION ALTITUDES ===")
        self.log(f"?? TOTAL : {total_checked} canalisation(s) vérifiée(s)")
        self.log(f"?? {len(erreurs)} erreur(s) détectée(s)")
        
        return erreurs

