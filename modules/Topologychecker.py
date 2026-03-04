from qgis.core import (
    QgsGeometry, 
    QgsFeatureRequest, 
    QgsSpatialIndex, 
    QgsPointXY,
    QgsProject,
    QgsWkbTypes
)
from PyQt5.QtCore import Qt

class TopologyChecker:
    """Classe pour la vérification topologique des réseaux hydrauliques."""
    
    def __init__(self, layers):
        """Initialise le vérificateur avec les couches à analyser."""
        self.layers = layers
        self.error_id = 0  # Pour générer des identifiants uniques d'erreurs
        
        # Tolérance de connexion (pixels)
        self.connection_tolerance = 0.01  # 1cm
        
        # Initialiser les index spatiaux pour optimiser les recherches
        self.spatial_indexes = {}
        for key, layer in self.layers.items():
            if layer:
                self.spatial_indexes[key] = QgsSpatialIndex(layer.getFeatures())

    def get_line_endpoints(self, geometry):
        """Extrait les points de départ et d'arrivée d'une géométrie linéaire.
        
        Fonctionne avec LineString et MultiLineString.
        
        Args:
            geometry: Géométrie QgsGeometry linéaire
            
        Returns:
            tuple: (point_début, point_fin) où chaque point est un QgsPointXY
                  ou (None, None) si la géométrie n'est pas une ligne valide
        """
        if not geometry or geometry.type() != QgsWkbTypes.LineGeometry:
            return None, None
            
        start_point = None
        end_point = None
        
        # Gérer différemment selon le type de géométrie
        if geometry.isMultipart():
            parts = geometry.asMultiPolyline()
            if parts and parts[0]:
                start_point = parts[0][0]  # Premier point de la première ligne
                if parts[-1]:
                    end_point = parts[-1][-1]  # Dernier point de la dernière ligne
        else:
            line = geometry.asPolyline()
            if line:
                start_point = line[0]
                end_point = line[-1]
                
        return start_point, end_point 

    def run_all_checks(self):
        """Exécute toutes les vérifications et retourne une liste des erreurs."""
        all_errors = []
        
        # Vérification des connexions entre boîtes et branchements
        all_errors.extend(self.check_connections_boxes_branches())
        
        # Vérification des connexions entre branchements et réseau
        all_errors.extend(self.check_connections_branches_network())
        
        # Vérification des connexions entre regards et canalisations
        all_errors.extend(self.check_connections_manholes_pipes())
        
        # Vérification des connexions entre DO et canalisations
        all_errors.extend(self.check_connections_do_pipes())
        
        # Vérification des connexions entre PR, refoulement et regards
        all_errors.extend(self.check_connections_pr_pipes())
        
        # Vérification des superpositions d'entités
        all_errors.extend(self.check_entity_overlaps())
        
        # Vérification du sens d'écoulement
        all_errors.extend(self.check_flow_direction())
        
        return all_errors

    def check_connections_boxes_branches(self):
        """Vérifie les connexions entre boîtes de branchement et branchements.
        
        Règles :
        - Les boites de branchement doivent être connectées à un branchement
        - Les branchements doivent commencer par une boite de branchement
        - Boîte EU avec branchement EU
        - Boîte EP avec branchement EP
        - Boîte UNI avec branchement UNI
        """
        errors = []
        
        # Vérifier les connexions boites-branchements pour chaque type (EU, EP, UNI)
        for network_type in ["eu", "ep", "uni"]:
            box_layer = self.layers.get(f'box_{network_type}')
            branch_layer = self.layers.get(f'branch_{network_type}')
            
            if not box_layer or not branch_layer:
                continue
                
            box_index = self.spatial_indexes.get(f'box_{network_type}')
            if not box_index:
                box_index = QgsSpatialIndex(box_layer.getFeatures())
                self.spatial_indexes[f'box_{network_type}'] = box_index
        
        # 1. Vérifier que chaque boîte est connectée à un branchement
        for box_feature in box_layer.getFeatures():
            box_id = box_feature.id()
            box_geom = box_feature.geometry()
                # Vérifier si la géométrie est nulle ou invalide
            if not box_geom or box_geom.isEmpty() or box_geom.isNull():
                self.error_id += 1
                errors.append({
                    'id': self.error_id,
                    'type': 'Connexion boîtes-branchements',
                    'description': f"Boîte {network_type.upper()} (ID:{box_id}) a une géométrie nulle ou invalide",
                    'layer': box_layer.name(),
                    'feature_id': box_id,
                    'geometry': None  # Pas de géométrie à afficher
                })
                continue  # Passer à la boîte suivante
            
            # Récupérer le point seulement si la géométrie est valide
            box_point = box_geom.asPoint()
            
            # Rechercher les branchements connectés à cette boîte
            buffer_geom = box_geom.buffer(self.connection_tolerance, 5)
            
            # Utiliser un filtre spatial pour trouver les branchements à proximité
            request = QgsFeatureRequest().setFilterRect(buffer_geom.boundingBox())
            connected_branches = []
            
            for branch_feature in branch_layer.getFeatures(request):
                branch_geom = branch_feature.geometry()
                if branch_geom.intersects(buffer_geom):
                    connected_branches.append(branch_feature.id())
            
            # Si aucun branchement n'est connecté à cette boîte
            if not connected_branches:
                self.error_id += 1
                errors.append({
                    'id': self.error_id,
                    'type': 'Connexion boîtes-branchements',
                    'description': f"Boîte {network_type.upper()} (ID:{box_id}) non connectée à un branchement",
                    'layer': box_layer.name(),
                    'feature_id': box_id,
                    'geometry': box_geom
                })
        
        # 2. Vérifier que chaque branchement commence par une boîte
        for branch_feature in branch_layer.getFeatures():
            branch_id = branch_feature.id()
            branch_geom = branch_feature.geometry()
            
            if branch_geom.type() != QgsWkbTypes.LineGeometry:
                continue
            
            # Obtenir le dernier point du branchement (point d'arrivée)
            start_point, end_point = self.get_line_endpoints(branch_geom)
            
            if not end_point:
                continue  # Ignorer les géométries invalides
                
            end_point_geom = QgsGeometry.fromPointXY(end_point)

            # Obtenir le premier point du branchement (point de départ)
            if branch_geom.type() == QgsWkbTypes.LineGeometry:
                start_point = None
                
                # Gérer différemment les géométries simples et multi-lignes
                if branch_geom.isMultipart():
                    # Pour les MultiLineString, prendre le premier point de la première ligne
                    parts = branch_geom.asMultiPolyline()
                    if parts and parts[0]:
                        start_point = parts[0][0]  # Premier point de la première ligne
                else:
                    # Pour les LineString simples
                    line = branch_geom.asPolyline()
                    if line:
                        start_point = line[0]  # Premier point de la ligne
                
                # Continuer seulement si nous avons pu extraire un point de départ
                if start_point:
                    start_point_geom = QgsGeometry.fromPointXY(start_point)
                    
                    # Créer un buffer autour du point de départ
                    buffer_geom = start_point_geom.buffer(self.connection_tolerance, 5)
                    
                    # Rechercher les boîtes à proximité du point de départ
                    request = QgsFeatureRequest().setFilterRect(buffer_geom.boundingBox())
                    connected_boxes = []
                    
                    for box_feature in box_layer.getFeatures(request):
                        box_geom = box_feature.geometry()
                        if box_geom.intersects(buffer_geom):
                            connected_boxes.append(box_feature.id())
                    
                    # Si aucune boîte n'est connectée au début du branchement
                    if not connected_boxes:
                        self.error_id += 1
                        errors.append({
                            'id': self.error_id,
                            'type': 'Connexion boîtes-branchements',
                            'description': f"Branchement {network_type.upper()} (ID:{branch_id}) ne commence pas par une boîte",
                            'layer': branch_layer.name(),
                            'feature_id': branch_id,
                            'geometry': start_point_geom
                        })
        
        return errors        
        
    def check_connections_branches_network(self):
        """Vérifie les connexions entre branchements et réseau principal.
        
        Règles :
        - Branchement EU peut être connecté à réseau EU, regard EU, boite EU, réseau UNI, regard UNI, boite UNI
        - Branchement UNI peut être connecté à réseau UNI, regard UNI, boite UNI
        - Branchement EP peut être connecté à réseau EP, regard EP, boite EP, réseau UNI, regard UNI, boite UNI
        - Branchement EP ne peut pas être connecté à des objets EU
        """
        errors = []
        
        # Définir les règles de connexion autorisées par type de branchement
        connection_rules = {
            'branch_eu': ['network_eu', 'manhole_eu', 'box_eu', 'network_uni', 'manhole_uni', 'box_uni'],
            'branch_uni': ['network_uni', 'manhole_uni', 'box_uni'],
            'branch_ep': ['network_ep', 'manhole_ep', 'box_ep', 'network_uni', 'manhole_uni', 'box_uni', 'gully', 'grate', 'outlet']
        }
        
        # Vérifier les connexions pour chaque type de branchement
        for branch_type, allowed_connections in connection_rules.items():
            branch_layer = self.layers.get(branch_type)
            if not branch_layer:
                continue
            
            # Pour chaque branchement
            for branch_feature in branch_layer.getFeatures():
                branch_id = branch_feature.id()
                branch_geom = branch_feature.geometry()
                
                if branch_geom.type() != QgsWkbTypes.LineGeometry:
                    continue
                
                # Obtenir le dernier point du branchement (point d'arrivée)
                branch_line = branch_geom.asPolyline()
                end_point = branch_line[-1]
                end_point_geom = QgsGeometry.fromPointXY(end_point)
                
                # Créer un buffer autour du point d'arrivée
                buffer_geom = end_point_geom.buffer(self.connection_tolerance, 5)
                
                # Vérifier les connexions avec toutes les couches autorisées
                valid_connection_found = False
                
                for target_type in allowed_connections:
                    target_layer = self.layers.get(target_type)
                    if not target_layer:
                        continue
                    
                    # Pour les couches de type ligne (réseaux)
                    if target_layer.geometryType() == QgsWkbTypes.LineGeometry:
                        for target_feature in target_layer.getFeatures(QgsFeatureRequest().setFilterRect(buffer_geom.boundingBox())):
                            target_geom = target_feature.geometry()
                            # Vérifier si le point final du branchement est sur la ligne (et pas juste à proximité)
                            if target_geom.intersects(buffer_geom):
                                valid_connection_found = True
                                break
                    
                    # Pour les couches de type point (regards, boîtes)
                    elif target_layer.geometryType() == QgsWkbTypes.PointGeometry:
                        for target_feature in target_layer.getFeatures(QgsFeatureRequest().setFilterRect(buffer_geom.boundingBox())):
                            target_geom = target_feature.geometry()
                            if target_geom.intersects(buffer_geom):
                                valid_connection_found = True
                                break
                
                # Si aucune connexion valide n'est trouvée pour ce branchement
                if not valid_connection_found:
                    network_type = branch_type.split('_')[1].upper()
                    self.error_id += 1
                    errors.append({
                        'id': self.error_id,
                        'type': 'Connexion branchements-réseau',
                        'description': f"Branchement {network_type} (ID:{branch_id}) non connecté correctement au réseau",
                        'layer': branch_layer.name(),
                        'feature_id': branch_id,
                        'geometry': end_point_geom
                    })
                
                # Vérification spécifique pour EP: ne pas être connecté à EU
                if branch_type == 'branch_ep':
                    for forbidden_type in ['network_eu', 'manhole_eu', 'box_eu']:
                        forbidden_layer = self.layers.get(forbidden_type)
                        if not forbidden_layer:
                            continue
                        
                        # Vérifier si le branchement EP est connecté à des éléments EU
                        for forbidden_feature in forbidden_layer.getFeatures(QgsFeatureRequest().setFilterRect(buffer_geom.boundingBox())):
                            forbidden_geom = forbidden_feature.geometry()
                            if forbidden_geom.intersects(buffer_geom):
                                self.error_id += 1
                                errors.append({
                                    'id': self.error_id,
                                    'type': 'Connexion branchements-réseau',
                                    'description': f"Branchement EP (ID:{branch_id}) connecté à un élément EU (interdit)",
                                    'layer': branch_layer.name(),
                                    'feature_id': branch_id,
                                    'geometry': end_point_geom
                                })
                                break
        
        return errors
        
    def check_connections_manholes_pipes(self):
        """Vérifie les connexions entre regards et canalisations.
        
        Règles :
        - Les regards doivent être connectés à au moins une canalisation
        - Les réseaux EU commencent/finissent par un regard EU, DO ou PR
        - Les réseaux EP commencent par un regard EP, grille, avaloir, DO et finissent par un regard EP, exutoire, regard UNI, avaloir, grille
        - Les réseaux UNI commencent/finissent par un regard UNI, DO, PR
        """
        errors = []
        
        # Définir les règles pour les points de départ/arrivée des réseaux
        network_rules = {
            'network_eu': {
                'start': ['manhole_eu', 'overflow'],
                'end': ['manhole_eu', 'manhole_uni', 'pump']
            },
            'network_ep': {
                'start': ['manhole_ep', 'gully', 'grate', 'overflow'],
                'end': ['manhole_ep', 'outlet', 'manhole_uni', 'gully', 'grate']
            },
            'network_uni': {
                'start': ['manhole_uni'],
                'end': ['manhole_uni', 'overflow', 'pump']
            }
        }
        
        # 1. Vérifier que chaque regard est connecté à au moins une canalisation
        for manhole_type in ['manhole_eu', 'manhole_ep', 'manhole_uni']:
            manhole_layer = self.layers.get(manhole_type)
            if not manhole_layer:
                continue
            
            for manhole_feature in manhole_layer.getFeatures():
                manhole_id = manhole_feature.id()
                manhole_geom = manhole_feature.geometry()
                
                # Créer un buffer autour du regard
                buffer_geom = manhole_geom.buffer(self.connection_tolerance, 5)
                
                # Rechercher les canalisations connectées
                connected_pipes = []
                for network_type in ['network_eu', 'network_ep', 'network_uni']:
                    network_layer = self.layers.get(network_type)
                    if not network_layer:
                        continue
                    
                    request = QgsFeatureRequest().setFilterRect(buffer_geom.boundingBox())
                    for pipe_feature in network_layer.getFeatures(request):
                        pipe_geom = pipe_feature.geometry()
                        if pipe_geom.intersects(buffer_geom):
                            connected_pipes.append((pipe_feature.id(), network_type))
                
                # Si aucune canalisation n'est connectée à ce regard
                if not connected_pipes:
                    network_type = manhole_type.split('_')[1].upper()
                    self.error_id += 1
                    errors.append({
                        'id': self.error_id,
                        'type': 'Connexion regards-canalisations',
                        'description': f"Regard {network_type} (ID:{manhole_id}) non connecté à une canalisation",
                        'layer': manhole_layer.name(),
                        'feature_id': manhole_id,
                        'geometry': manhole_geom
                    })
        
        # 2. Vérifier que chaque canalisation commence/finit par des éléments conformes aux règles
        for network_type, rules in network_rules.items():
            network_layer = self.layers.get(network_type)
            if not network_layer:
                continue
            
            for network_type, rules in network_rules.items():
                # Code existant...
                
                for pipe_feature in network_layer.getFeatures():
                    pipe_id = pipe_feature.id()
                    pipe_geom = pipe_feature.geometry()
                    
                    if pipe_geom.type() != QgsWkbTypes.LineGeometry:
                        continue
                    
                    start_point, end_point = self.get_line_endpoints(pipe_geom)
                    
                    if not start_point or not end_point:
                        continue  # Ignorer les géométries invalides
                        
                    start_point_geom = QgsGeometry.fromPointXY(start_point)
                    end_point_geom = QgsGeometry.fromPointXY(end_point)
                
                
                # Buffer autour des points de départ et d'arrivée
                start_buffer = start_point_geom.buffer(self.connection_tolerance, 5)
                end_buffer = end_point_geom.buffer(self.connection_tolerance, 5)
                
                # Vérifier la connexion au point de départ
                start_valid_connection = False
                for start_type in rules['start']:
                    start_layer = self.layers.get(start_type)
                    if not start_layer:
                        continue
                    
                    request = QgsFeatureRequest().setFilterRect(start_buffer.boundingBox())
                    for start_feature in start_layer.getFeatures(request):
                        if start_feature.geometry().intersects(start_buffer):
                            start_valid_connection = True
                            break
                    
                    if start_valid_connection:
                        break
                
                # Vérifier la connexion au point d'arrivée
                end_valid_connection = False
                for end_type in rules['end']:
                    end_layer = self.layers.get(end_type)
                    if not end_layer:
                        continue
                    
                    request = QgsFeatureRequest().setFilterRect(end_buffer.boundingBox())
                    for end_feature in end_layer.getFeatures(request):
                        if end_feature.geometry().intersects(end_buffer):
                            end_valid_connection = True
                            break
                    
                    if end_valid_connection:
                        break
                
                # Signaler les erreurs de connexion
                type_abbr = network_type.split('_')[1].upper()
                
                if not start_valid_connection:
                    self.error_id += 1
                    errors.append({
                        'id': self.error_id,
                        'type': 'Connexion regards-canalisations',
                        'description': f"Réseau {type_abbr} (ID:{pipe_id}) ne commence pas par un élément valide",
                        'layer': network_layer.name(),
                        'feature_id': pipe_id,
                        'geometry': start_point_geom
                    })
                
                if not end_valid_connection:
                    self.error_id += 1
                    errors.append({
                        'id': self.error_id,
                        'type': 'Connexion regards-canalisations',
                        'description': f"Réseau {type_abbr} (ID:{pipe_id}) ne finit pas par un élément valide",
                        'layer': network_layer.name(),
                        'feature_id': pipe_id,
                        'geometry': end_point_geom
                    })
        
        return errors
    
    def check_connections_do_pipes(self):
        """Vérifie les connexions entre déversoirs d'orage (DO) et canalisations.
        
        Règles :
        - Les DO doivent être connectés à au moins une canalisation
        """
        errors = []
        
        # Vérifier les DO
        do_layer = self.layers.get('overflow')
        if not do_layer:
            return errors
        
        for do_feature in do_layer.getFeatures():
            do_id = do_feature.id()
            do_geom = do_feature.geometry()
            
            # Créer un buffer autour du DO
            buffer_geom = do_geom.buffer(self.connection_tolerance, 5)
            
            # Rechercher les canalisations connectées
            connected_pipes = []
            for network_type in ['network_eu', 'network_ep', 'network_uni']:
                network_layer = self.layers.get(network_type)
                if not network_layer:
                    continue
                
                request = QgsFeatureRequest().setFilterRect(buffer_geom.boundingBox())
                for pipe_feature in network_layer.getFeatures(request):
                    pipe_geom = pipe_feature.geometry()
                    if pipe_geom.intersects(buffer_geom):
                        connected_pipes.append((pipe_feature.id(), network_type))
            
            # Si aucune canalisation n'est connectée à ce DO
            if not connected_pipes:
                self.error_id += 1
                errors.append({
                    'id': self.error_id,
                    'type': 'Connexion DO-canalisation',
                    'description': f"Déversoir d'orage (ID:{do_id}) non connecté à une canalisation",
                    'layer': do_layer.name(),
                    'feature_id': do_id,
                    'geometry': do_geom
                })
        
        return errors
    
    def check_connections_pr_pipes(self):
        """Vérifie les connexions entre postes de refoulement (PR), canalisations de refoulement et regards.
        
        Règles :
        - Les réseaux de refoulement commencent par un PR et se terminent par un regard
        """
        errors = []
        
        # Vérifier que les PR sont connectés à des canalisations de refoulement
        pr_layer = self.layers.get('pump')
        refoulement_layer = self.layers.get('refoulement')
        
        if not pr_layer or not refoulement_layer:
            return errors
        
        # 1. Vérifier que chaque PR est connecté à au moins une canalisation de refoulement
        for pr_feature in pr_layer.getFeatures():
            pr_id = pr_feature.id()
            pr_geom = pr_feature.geometry()
            
            # Créer un buffer autour du PR
            buffer_geom = pr_geom.buffer(self.connection_tolerance, 5)
            
            # Rechercher les canalisations de refoulement connectées
            connected_refoulement = []
            request = QgsFeatureRequest().setFilterRect(buffer_geom.boundingBox())
            
            for refoulement_feature in refoulement_layer.getFeatures(request):
                refoulement_geom = refoulement_feature.geometry()
                
                if refoulement_geom.type() == QgsWkbTypes.LineGeometry:
                    # Vérifier si le PR est connecté au point de départ de la canalisation
                    refoulement_line = refoulement_geom.asPolyline()
                    start_point_geom = QgsGeometry.fromPointXY(refoulement_line[0])
                    
                    if start_point_geom.intersects(buffer_geom):
                        connected_refoulement.append(refoulement_feature.id())
            
            # Si aucune canalisation de refoulement ne commence par ce PR
            if not connected_refoulement:
                self.error_id += 1
                errors.append({
                    'id': self.error_id,
                    'type': 'Connexion refoulement-PR-regard',
                    'description': f"Poste de refoulement (ID:{pr_id}) non connecté au début d'une canalisation de refoulement",
                    'layer': pr_layer.name(),
                    'feature_id': pr_id,
                    'geometry': pr_geom
                })
        
        # 2. Vérifier que chaque canalisation de refoulement commence par un PR et finit par un regard
        for refoulement_feature in refoulement_layer.getFeatures():
            refoulement_id = refoulement_feature.id()
            refoulement_geom = refoulement_feature.geometry()
            
            if refoulement_geom.type() != QgsWkbTypes.LineGeometry:
                continue
            
            refoulement_line = refoulement_geom.asPolyline()
            start_point = refoulement_line[0]
            end_point = refoulement_line[-1]
            
            start_point_geom = QgsGeometry.fromPointXY(start_point)
            end_point_geom = QgsGeometry.fromPointXY(end_point)
            
            # Buffer autour des points de départ et d'arrivée
            start_buffer = start_point_geom.buffer(self.connection_tolerance, 5)
            end_buffer = end_point_geom.buffer(self.connection_tolerance, 5)
            
            # Vérifier la connexion à un PR au point de départ
            start_connected_to_pr = False
            for pr_feature in pr_layer.getFeatures(QgsFeatureRequest().setFilterRect(start_buffer.boundingBox())):
                if pr_feature.geometry().intersects(start_buffer):
                    start_connected_to_pr = True
                    break
            
            # Vérifier la connexion à un regard au point d'arrivée
            end_connected_to_manhole = False
            for manhole_type in ['manhole_eu', 'manhole_ep', 'manhole_uni']:
                manhole_layer = self.layers.get(manhole_type)
                if not manhole_layer:
                    continue
                
                for manhole_feature in manhole_layer.getFeatures(QgsFeatureRequest().setFilterRect(end_buffer.boundingBox())):
                    if manhole_feature.geometry().intersects(end_buffer):
                        end_connected_to_manhole = True
                        break
                
                if end_connected_to_manhole:
                    break
            
            # Signaler les erreurs
            if not start_connected_to_pr:
                self.error_id += 1
                errors.append({
                    'id': self.error_id,
                    'type': 'Connexion refoulement-PR-regard',
                    'description': f"Canalisation de refoulement (ID:{refoulement_id}) ne commence pas par un poste de refoulement",
                    'layer': refoulement_layer.name(),
                    'feature_id': refoulement_id,
                    'geometry': start_point_geom
                })
            
            if not end_connected_to_manhole:
                self.error_id += 1
                errors.append({
                    'id': self.error_id,
                    'type': 'Connexion refoulement-PR-regard',
                    'description': f"Canalisation de refoulement (ID:{refoulement_id}) ne finit pas par un regard",
                    'layer': refoulement_layer.name(),
                    'feature_id': refoulement_id,
                    'geometry': end_point_geom
                })
        
        return errors
    
    def check_entity_overlaps(self):
        """Vérifie la superposition d'entités du même type.
        
        Règles :
        - Les canalisations du même type ne doivent pas se superposer
        - Les regards/boîtes du même type ne doivent pas se superposer
        """
        errors = []
        
        # Regrouper les couches par type de géométrie et famille de réseau
        network_groups = {
            'eu': [layer for key, layer in self.layers.items() if 'eu' in key and layer],
            'ep': [layer for key, layer in self.layers.items() if 'ep' in key and layer],
            'uni': [layer for key, layer in self.layers.items() if 'uni' in key and layer]
        }
        
        # Pour chaque groupe, vérifier les superpositions entre couches de même type
        for network_type, layers_group in network_groups.items():
            # Vérifier les superpositions entre éléments de type ligne (canalisations)
            line_layers = [layer for layer in layers_group if layer.geometryType() == QgsWkbTypes.LineGeometry]
            
            for i, layer1 in enumerate(line_layers):
                # Créer un index spatial pour cette couche si nécessaire
                if not layer1.name() in self.spatial_indexes:
                    self.spatial_indexes[layer1.name()] = QgsSpatialIndex(layer1.getFeatures())
                
                # Vérifier les superpositions au sein de la même couche
                features_dict = {f.id(): f for f in layer1.getFeatures()}
                
                for feature_id, feature in features_dict.items():
                    line_geom = feature.geometry()
                    
                    # Rechercher les entités qui peuvent se superposer
                    bbox = line_geom.boundingBox()
                    candidate_ids = self.spatial_indexes[layer1.name()].intersects(bbox)
                    
                    for candidate_id in candidate_ids:
                        # Ne pas comparer une entité avec elle-même
                        if candidate_id == feature_id:
                            continue
                        
                        candidate_feature = features_dict[candidate_id]
                        candidate_geom = candidate_feature.geometry()
                        
                        # Vérifier si les géométries se superposent (pas seulement les intersections aux extrémités)
                        if line_geom.overlaps(candidate_geom):
                            self.error_id += 1
                            errors.append({
                                'id': self.error_id,
                                'type': 'Superposition d\'entités',
                                'description': f"Canalisation {network_type.upper()} (ID:{feature_id}) superposée avec canalisation (ID:{candidate_id})",
                                'layer': layer1.name(),
                                'feature_id': feature_id,
                                'geometry': line_geom.intersection(candidate_geom)
                            })
                
                # Vérifier les superpositions avec les autres couches de ligne du même groupe
                for j in range(i + 1, len(line_layers)):
                    layer2 = line_layers[j]
                    
                    # Créer un index spatial pour la deuxième couche si nécessaire
                    if not layer2.name() in self.spatial_indexes:
                        self.spatial_indexes[layer2.name()] = QgsSpatialIndex(layer2.getFeatures())
                    
                    # Pour chaque entité de la première couche
                    for feature in layer1.getFeatures():
                        feature_id = feature.id()
                        line_geom = feature.geometry()
                        
                        # Rechercher les entités de la deuxième couche qui peuvent se superposer
                        bbox = line_geom.boundingBox()
                        request = QgsFeatureRequest().setFilterRect(bbox)
                        
                        for candidate_feature in layer2.getFeatures(request):
                            candidate_id = candidate_feature.id()
                            candidate_geom = candidate_feature.geometry()
                            
                            # Vérifier si les géométries se superposent
                            if line_geom.overlaps(candidate_geom):
                                self.error_id += 1
                                errors.append({
                                    'id': self.error_id,
                                    'type': 'Superposition d\'entités',
                                    'description': f"Canalisation {network_type.upper()} de {layer1.name()} (ID:{feature_id}) "
                                                   f"superposée avec canalisation de {layer2.name()} (ID:{candidate_id})",
                                    'layer': layer1.name(),
                                    'feature_id': feature_id,
                                    'geometry': line_geom.intersection(candidate_geom)
                                })
            
            # Vérifier les superpositions entre éléments de type point (regards, boîtes)
            point_layers = [layer for layer in layers_group if layer.geometryType() == QgsWkbTypes.PointGeometry]
            
            for i, layer1 in enumerate(point_layers):
                # Créer un index spatial pour cette couche si nécessaire
                if not layer1.name() in self.spatial_indexes:
                    self.spatial_indexes[layer1.name()] = QgsSpatialIndex(layer1.getFeatures())
                
                # Vérifier les superpositions au sein de la même couche
                features_dict = {f.id(): f for f in layer1.getFeatures()}
                
                for feature_id, feature in features_dict.items():
                    point_geom = feature.geometry()
                    
                    # Créer un buffer pour la détection de superposition
                    buffer_geom = point_geom.buffer(self.connection_tolerance, 5)
                    bbox = buffer_geom.boundingBox()
                    
                    # Rechercher les entités qui peuvent se superposer
                    candidate_ids = self.spatial_indexes[layer1.name()].intersects(bbox)
                    
                    for candidate_id in candidate_ids:
                        # Ne pas comparer une entité avec elle-même
                        if candidate_id == feature_id:
                            continue
                        
                        candidate_feature = features_dict[candidate_id]
                        candidate_geom = candidate_feature.geometry()
                        
                        # Vérifier si les géométries sont trop proches
                        if point_geom.distance(candidate_geom) < self.connection_tolerance:
                            self.error_id += 1
                            errors.append({
                                'id': self.error_id,
                                'type': 'Superposition d\'entités',
                                'description': f"Point {network_type.upper()} (ID:{feature_id}) superposé avec point (ID:{candidate_id})",
                                'layer': layer1.name(),
                                'feature_id': feature_id,
                                'geometry': point_geom
                            })
                
                # Vérifier les superpositions avec les autres couches de point du même groupe
                for j in range(i + 1, len(point_layers)):
                    layer2 = point_layers[j]
                    
                    # Créer un index spatial pour la deuxième couche si nécessaire
                    if not layer2.name() in self.spatial_indexes:
                        self.spatial_indexes[layer2.name()] = QgsSpatialIndex(layer2.getFeatures())
                    
                    # Pour chaque entité de la première couche
                    for feature in layer1.getFeatures():
                        feature_id = feature.id()
                        point_geom = feature.geometry()
                        
                        # Créer un buffer pour la détection de superposition
                        buffer_geom = point_geom.buffer(self.connection_tolerance, 5)
                        
                        # Rechercher les entités de la deuxième couche qui peuvent se superposer
                        request = QgsFeatureRequest().setFilterRect(buffer_geom.boundingBox())
                        
                        for candidate_feature in layer2.getFeatures(request):
                            candidate_id = candidate_feature.id()
                            candidate_geom = candidate_feature.geometry()
                            
                            # Vérifier si les géométries sont trop proches
                            if point_geom.distance(candidate_geom) < self.connection_tolerance:
                                self.error_id += 1
                                errors.append({
                                    'id': self.error_id,
                                    'type': 'Superposition d\'entités',
                                    'description': f"Point {network_type.upper()} de {layer1.name()} (ID:{feature_id}) "
                                                   f"superposé avec point de {layer2.name()} (ID:{candidate_id})",
                                    'layer': layer1.name(),
                                    'feature_id': feature_id,
                                    'geometry': point_geom
                                })
        
        return errors
    
    def check_flow_direction(self):
        """Vérifie le sens d'écoulement des canalisations en fonction de la géométrie.
        
        Règle : La direction de numérisation de la polyligne de canalisation doit suivre le sens d'écoulement.
        """
        errors = []
        
        # Pour chaque type de réseau
        for network_type in ['network_eu', 'network_ep', 'network_uni']:
            network_layer = self.layers.get(network_type)
            if not network_layer:
                continue
            
            # Parcourir toutes les canalisations
            for pipe_feature in network_layer.getFeatures():
                pipe_id = pipe_feature.id()
                pipe_geom = pipe_feature.geometry()
                
                if pipe_geom.type() != QgsWkbTypes.LineGeometry:
                    continue
                
                # Obtenir les points de la ligne
                pipe_line = pipe_geom.asPolyline()
                if len(pipe_line) < 2:
                    continue
                
                # Points de départ et d'arrivée
                start_point = pipe_line[0]
                end_point = pipe_line[-1]
                
                # Vérifier le sens d'écoulement en créant une zone tampon autour du point de départ
                # et en cherchant des regards ou DO
                start_point_geom = QgsGeometry.fromPointXY(start_point)
                buffer_geom = start_point_geom.buffer(self.connection_tolerance, 5)
                
                # Trouver les regards ou DO connectés au point de départ
                connected_element_found = False
                
                # Types d'éléments qui peuvent être en amont
                upstream_element_types = ['manhole_eu', 'manhole_ep', 'manhole_uni', 'overflow', 'gully', 'grate', 'pump']
                
                for element_type in upstream_element_types:
                    element_layer = self.layers.get(element_type)
                    if not element_layer:
                        continue
                    
                    request = QgsFeatureRequest().setFilterRect(buffer_geom.boundingBox())
                    for element_feature in element_layer.getFeatures(request):
                        element_geom = element_feature.geometry()
                        
                        if element_geom.intersects(buffer_geom):
                            connected_element_found = True
                            break
                    
                    if connected_element_found:
                        break
                
                # Si aucun élément n'est connecté au point de départ,
                # vérifier si le point de départ est connecté à une autre canalisation
                if not connected_element_found:
                    for net_type in ['network_eu', 'network_ep', 'network_uni']:
                        if net_type == network_type:
                            continue  # Éviter de vérifier la même couche
                        
                        other_layer = self.layers.get(net_type)
                        if not other_layer:
                            continue
                        
                        request = QgsFeatureRequest().setFilterRect(buffer_geom.boundingBox())
                        for other_pipe in other_layer.getFeatures(request):
                            other_geom = other_pipe.geometry()
                            
                            if other_geom.intersects(buffer_geom):
                                connected_element_found = True
                                break
                        
                        if connected_element_found:
                            break
                
                # Si toujours aucun élément connecté au point de départ, cela peut indiquer
                # une canalisation dans le mauvais sens ou orpheline
                if not connected_element_found:
                    # Vérifier si le point final est connecté à un regard/élément amont
                    end_point_geom = QgsGeometry.fromPointXY(end_point)
                    end_buffer = end_point_geom.buffer(self.connection_tolerance, 5)
                    
                    end_connected_to_upstream = False
                    for element_type in upstream_element_types:
                        element_layer = self.layers.get(element_type)
                        if not element_layer:
                            continue
                        
                        request = QgsFeatureRequest().setFilterRect(end_buffer.boundingBox())
                        for element_feature in element_layer.getFeatures(request):
                            if element_feature.geometry().intersects(end_buffer):
                                end_connected_to_upstream = True
                                break
                        
                        if end_connected_to_upstream:
                            break
                    
                    # Si le point final est connecté à un élément amont, c'est probablement un problème de sens
                    if end_connected_to_upstream:
                        self.error_id += 1
                        errors.append({
                            'id': self.error_id,
                            'type': 'Sens d\'écoulement',
                            'description': f"Canalisation {network_type.split('_')[1].upper()} (ID:{pipe_id}) probablement numérisée dans le mauvais sens",
                            'layer': network_layer.name(),
                            'feature_id': pipe_id,
                            'geometry': pipe_geom
                        })
        
        return errors