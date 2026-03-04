import math
from qgis.core import (
    QgsFeature, QgsGeometry, QgsWkbTypes, QgsPointXY, QgsFeatureRequest, 
    QgsProject, QgsDistanceArea, QgsSpatialIndex, NULL
)

class ProfileGenerator:
    """Classe pour extraire et préparer les données du profil en long."""
    
    def __init__(self, cana_layer, regard_layer, settings):
        """Initialise le générateur de profil.
        
        Args:
            cana_layer: Couche des canalisations
            regard_layer: Couche des regards
            settings: Dictionnaire des paramètres du profil
        """
        self.cana_layer = cana_layer
        self.regard_layer = regard_layer
        self.settings = settings
        self.distance_area = QgsDistanceArea()
        self.distance_area.setEllipsoid(QgsProject.instance().ellipsoid())
        
        # Création d'un index spatial pour les regards
        self.regard_index = QgsSpatialIndex(regard_layer.getFeatures())
        
        # Données de sortie
        self.profile_data = {
            'canalisations': [],
            'regards': [],
            'cumulative_distance': 0,
            'min_z': float('inf'),
            'max_z': float('-inf')
        }
    
    def generate_profile_from_selection(self):
        """Génère les données du profil à partir des canalisations sélectionnées."""
        selected_canas = list(self.cana_layer.selectedFeatures())
        
        if not selected_canas:
            return None
        
        # Trier les canalisations pour former un chemin
        ordered_canas = self._order_canalisations(selected_canas)
        
        # Récupérer les données pour chaque canalisation
        cumulative_distance = 0
        for cana in ordered_canas:
            # Traiter la canalisation
            cana_data = self._process_canalisation(cana, cumulative_distance)
            
            # Mettre à jour la distance cumulée
            cumulative_distance += cana_data['length']
            
            # Ajouter les données de la canalisation au profil
            self.profile_data['canalisations'].append(cana_data)
            
            # Traiter les regards aux extrémités
            if cana_data['regard_amont'] and cana_data['regard_amont']['id'] not in [r['id'] for r in self.profile_data['regards']]:
                self.profile_data['regards'].append(cana_data['regard_amont'])
            
            if cana_data['regard_aval'] and cana_data['regard_aval']['id'] not in [r['id'] for r in self.profile_data['regards']]:
                self.profile_data['regards'].append(cana_data['regard_aval'])
        
        # Après avoir traité les canalisations, vérifiez et corrigez les regards
        for regard in self.profile_data['regards']:
            # Vérifier si la distance est valide
            if regard.get('distance') is None or math.isnan(regard['distance']) or math.isinf(regard['distance']):
                print(f"Correction de la distance du regard {regard.get('id')}")
                
                # Chercher si c'est un regard amont ou aval d'une canalisation
                for i, cana in enumerate(self.profile_data['canalisations']):
                    if cana['regard_amont'] and cana['regard_amont']['id'] == regard['id']:
                        regard['distance'] = cana['start_distance']
                        print(f"  → distance définie à {regard['distance']} (début de canalisation)")
                        break
                    elif cana['regard_aval'] and cana['regard_aval']['id'] == regard['id']:
                        regard['distance'] = cana['end_distance']
                        print(f"  → distance définie à {regard['distance']} (fin de canalisation)")
                        break
                
                # Si toujours pas de distance valide, utiliser une valeur basée sur la position
                if regard.get('distance') is None or math.isnan(regard['distance']) or math.isinf(regard['distance']):
                    # Utiliser l'index du regard * 10 comme distance approximative
                    index = self.profile_data['regards'].index(regard)
                    regard['distance'] = index * 10.0
                    print(f"  → distance définie par défaut à {regard['distance']}")
    


        # Mettre à jour la distance cumulée totale
        self.profile_data['cumulative_distance'] = cumulative_distance
        
        print("\n--- Données du profil générées ---")
        for cana in self.profile_data['canalisations']:
            print(f"Canalisation {cana['id']}: z_amont={cana['z_amont']}, z_aval={cana['z_aval']}, "
                f"start={cana['start_distance']}, end={cana['end_distance']}")
        
        for regard in self.profile_data['regards']:
            print(f"Regard {regard.get('id', 'inconnu')}: distance={regard.get('distance')}, fe={regard.get('fe')}, "
                f"tn={regard.get('tn')}")

        return self.profile_data
    
    def generate_profile_between_points(self, start_point, end_point):
        """Génère les données du profil entre deux points.
        
        Args:
            start_point: Point de départ (QgsPointXY)
            end_point: Point d'arrivée (QgsPointXY)
        """
        # Trouver les regards les plus proches des points
        start_regard = self._find_nearest_regard(start_point)
        end_regard = self._find_nearest_regard(end_point)
        
        if not start_regard or not end_regard:
            return None
        
        # Trouver le chemin le plus court
        canas_path = self._find_shortest_path(start_regard, end_regard)
        
        if not canas_path:
            return None
        
        # Générer le profil à partir de ce chemin
        ordered_canas = canas_path
        
        # Récupérer les données pour chaque canalisation
        cumulative_distance = 0
        for cana in ordered_canas:
            # Traiter la canalisation
            cana_data = self._process_canalisation(cana, cumulative_distance)
            
            # Mettre à jour la distance cumulée
            cumulative_distance += cana_data['length']
            
            # Ajouter les données de la canalisation au profil
            self.profile_data['canalisations'].append(cana_data)
            
            # Traiter les regards aux extrémités
            if cana_data['regard_amont'] and cana_data['regard_amont']['id'] not in [r['id'] for r in self.profile_data['regards']]:
                self.profile_data['regards'].append(cana_data['regard_amont'])
            
            if cana_data['regard_aval'] and cana_data['regard_aval']['id'] not in [r['id'] for r in self.profile_data['regards']]:
                self.profile_data['regards'].append(cana_data['regard_aval'])
        
        # Mettre à jour la distance cumulée totale
        self.profile_data['cumulative_distance'] = cumulative_distance
        
        return self.profile_data
    
    def _process_canalisation(self, cana, start_distance):
        """Traite une canalisation et extrait ses données pour le profil."""
        # Calculer la longueur de manière plus robuste
        try:
            # Essayer d'abord la méthode standard
            length = self.distance_area.measureLength(cana.geometry())
            
            # Si la longueur est invalide, calculer manuellement
            if math.isnan(length) or math.isinf(length) or length <= 0:
                # Calculer manuellement à partir des points
                geom = cana.geometry()
                if geom.isMultipart():
                    multi_polyline = geom.asMultiPolyline()
                    length = 0
                    for polyline in multi_polyline:
                        for i in range(len(polyline) - 1):
                            length += polyline[i].distance(polyline[i+1])
                else:
                    polyline = geom.asPolyline()
                    length = 0
                    for i in range(len(polyline) - 1):
                        length += polyline[i].distance(polyline[i+1])
                        
            # Si toujours invalide, utiliser la valeur par défaut
            if math.isnan(length) or math.isinf(length) or length <= 0:
                print(f"Longueur invalide pour canalisation {cana.id()}, utilisation valeur par défaut")
                length = 10.0  # Valeur par défaut de 10 mètres
            
        except Exception as e:
            print(f"Erreur lors du calcul de la longueur pour canalisation {cana.id()}: {e}")
            length = 10.0  # Valeur par défaut en cas d'erreur
        
        # Récupérer les attributs de base de la canalisation
        cana_data = {
            'id': cana.id(),
            'geom': cana.geometry(),
            'start_distance': start_distance,
            'length': length,
            'end_distance': start_distance + length,
            'dn': self._get_numeric_attribute(cana, self.settings['dn_cana_field']),
            'z_amont': self._get_numeric_attribute(cana, self.settings['zamont_field']),
            'z_aval': self._get_numeric_attribute(cana, self.settings['zaval_field']),
            'regard_amont': None,
            'regard_aval': None,
            'pente': None
        }
        
        # Convertir le diamètre en m si nécessaire (supposé en mm)
        if cana_data['dn'] is not None:
            cana_data['dn'] = float(cana_data['dn']) / 1000  # mm vers m
        
        # Trouver les regards aux extrémités
        # Gérer différents types de géométrie (LineString et MultiLineString)
        geom = cana.geometry()
        if geom.isMultipart():
            # Pour une MultiLineString, extraire les points du premier et du dernier segment
            multi_polyline = geom.asMultiPolyline()
            if not multi_polyline:
                return None  # Géométrie vide ou invalide
                
            start_point = QgsPointXY(multi_polyline[0][0])
            end_point = QgsPointXY(multi_polyline[-1][-1])
        else:
            # Pour une simple LineString
            polyline = geom.asPolyline()
            if not polyline:
                return None  # Géométrie vide ou invalide
                
            start_point = QgsPointXY(polyline[0])
            end_point = QgsPointXY(polyline[-1])
        
        # Regard amont
        amont_regard = self._find_nearest_regard(start_point)
        if amont_regard:
            cana_data['regard_amont'] = self._process_regard(amont_regard, start_distance)
            
            # Si z_amont manquant, utiliser FE du regard
            if (cana_data['z_amont'] is None or math.isnan(cana_data['z_amont']) or math.isinf(cana_data['z_amont'])) and cana_data['regard_amont']['fe'] is not None:
                cana_data['z_amont'] = cana_data['regard_amont']['fe']
                print(f"Utilisation du FE du regard amont ({cana_data['regard_amont']['id']}) pour la cote amont: {cana_data['z_amont']}")
        
        # Regard aval
        aval_regard = self._find_nearest_regard(end_point)
        if aval_regard:
            cana_data['regard_aval'] = self._process_regard(aval_regard, cana_data['end_distance'])
            
            # Si z_aval manquant, utiliser FE du regard
            if (cana_data['z_aval'] is None or math.isnan(cana_data['z_aval']) or math.isinf(cana_data['z_aval'])) and cana_data['regard_aval']['fe'] is not None:
                cana_data['z_aval'] = cana_data['regard_aval']['fe']
                print(f"Utilisation du FE du regard aval ({cana_data['regard_aval']['id']}) pour la cote aval: {cana_data['z_aval']}")
        
        # APRÈS avoir essayé d'utiliser les FE des regards, utiliser des valeurs par défaut si toujours nécessaire
        if cana_data['z_amont'] is None or math.isnan(cana_data['z_amont']) or math.isinf(cana_data['z_amont']):
            print(f"Cote amont manquante pour canalisation {cana_data['id']}, utilisation valeur par défaut")
            cana_data['z_amont'] = 100.0  # Valeur arbitraire
            
        if cana_data['z_aval'] is None or math.isnan(cana_data['z_aval']) or math.isinf(cana_data['z_aval']):
            print(f"Cote aval manquante pour canalisation {cana_data['id']}, utilisation valeur par défaut")
            cana_data['z_aval'] = cana_data['z_amont'] - 0.01 * cana_data['length']  # Pente de 1%
        
        # Calculer la pente si possible
        if cana_data['z_amont'] is not None and cana_data['z_aval'] is not None and cana_data['length'] > 0:
            cana_data['pente'] = 100 * (cana_data['z_amont'] - cana_data['z_aval']) / cana_data['length']
        else:
            cana_data['pente'] = None
        
        # Mettre à jour min et max Z
        if cana_data['z_amont'] is not None:
            self.profile_data['min_z'] = min(self.profile_data['min_z'], cana_data['z_amont'])
            self.profile_data['max_z'] = max(self.profile_data['max_z'], cana_data['z_amont'])
        if cana_data['z_aval'] is not None:
            self.profile_data['min_z'] = min(self.profile_data['min_z'], cana_data['z_aval'])
            self.profile_data['max_z'] = max(self.profile_data['max_z'], cana_data['z_aval'])
        
        return cana_data


    def _process_regard(self, regard, distance):
        """Traite un regard et extrait ses données pour le profil."""
        # Vérifier que la distance fournie est valide
        if distance is None or math.isnan(distance) or math.isinf(distance):
            distance = 0.0  # Valeur par défaut si la distance fournie est invalide
            print(f"Distance fournie invalide pour regard {regard.id()}, utilisation valeur par défaut 0.0")
        
        # Obtenir le diamètre du regard
        dn = None
        if self.settings['use_dn_field']:
            dn = self._get_numeric_attribute(regard, self.settings['dn_regard_field'])
        else:
            # Utiliser la valeur par défaut (convertir mm en m)
            dn = float(self.settings['default_dn']) / 1000
        
        # Lire les valeurs TN et profondeur
        tn_value = self._get_numeric_attribute(regard, self.settings['tn_field'])
        print(f"Lecture du champ TN '{self.settings['tn_field']}' pour regard {regard.id()}: {tn_value}")
        
        prof_value = self._get_numeric_attribute(regard, self.settings['prof_field'])
        print(f"Lecture du champ profondeur '{self.settings['prof_field']}' pour regard {regard.id()}: {prof_value}(converti en float)")
        
        # CORRECTION: Vérifier explicitement les types et calculer correctement FE
        fe_value = None
        if tn_value is not None and prof_value is not None:
            # Assurer que les valeurs sont des nombres flottants
            try:
                tn_float = float(tn_value)
                prof_float = float(prof_value)
                fe_value = tn_float - prof_float
                print(f"FE calculé à partir de TN et profondeur pour regard {regard.id()}: TN ({tn_float}) - PROF ({prof_float}) = {fe_value}")
            except (ValueError, TypeError) as e:
                print(f"Erreur de conversion pour le calcul de FE: {e}")
        
        # Créer regard_data avec les valeurs
        regard_data = {
            'id': regard.id(),
            'geom': regard.geometry(),
            'distance': distance,
            'dn': dn,
            'fe': fe_value,
            'tn': tn_value
        }
        
        # Si FE n'a pas pu être calculé, chercher dans les canalisations connectées
        if regard_data['fe'] is None or math.isnan(regard_data['fe']) or math.isinf(regard_data['fe']):
            print(f"Impossible de calculer FE à partir de TN et profondeur pour regard {regard_data['id']}")
            print(f"Impossible de calculer FE à partir de TN et profondeur pour regard {regard_data['id']}")
            connected_cana = next((c for c in self.profile_data['canalisations'] 
                                if c['regard_amont'] and c['regard_amont']['id'] == regard_data['id']), None)
            if connected_cana:
                regard_data['fe'] = connected_cana['z_amont']
                print(f"  → FE obtenu depuis la canalisation amont: {regard_data['fe']}")
            else:
                connected_cana = next((c for c in self.profile_data['canalisations'] 
                                    if c['regard_aval'] and c['regard_aval']['id'] == regard_data['id']), None)
                if connected_cana:
                    regard_data['fe'] = connected_cana['z_aval']
                    print(f"  → FE obtenu depuis la canalisation aval: {regard_data['fe']}")
                else:
                    regard_data['fe'] = 100.0  # Valeur par défaut arbitraire
                    print(f"  → FE non calculable, valeur par défaut: {regard_data['fe']}")
        
        # Si TN manquant mais qu'on a FE et profondeur, calculer TN
        if (regard_data['tn'] is None or math.isnan(regard_data['tn']) or math.isinf(regard_data['tn'])) and regard_data['fe'] is not None:
            print(f"Cote TN manquante pour regard {regard_data['id']}, calcul à partir de FE")
            if prof_value is not None:
                regard_data['tn'] = regard_data['fe'] + prof_value
                print(f"  → TN = FE + profondeur = {regard_data['tn']}")
            else:
                regard_data['tn'] = regard_data['fe'] + 1.5  # TN par défaut = FE + 1.5m
                print(f"  → TN = FE + 1.5 (par défaut) = {regard_data['tn']}")
        
        # Mettre à jour min et max Z
        if regard_data['fe'] is not None:
            self.profile_data['min_z'] = min(self.profile_data['min_z'], regard_data['fe'])
        if regard_data['tn'] is not None:
            self.profile_data['max_z'] = max(self.profile_data['max_z'], regard_data['tn'])
        
        return regard_data
    
    def _find_nearest_regard(self, point, max_distance=5):
        """Trouve le regard le plus proche d'un point.
        
        Args:
            point: Point à rechercher (QgsPointXY)
            max_distance: Distance maximale de recherche (m)
        """
        # Utiliser l'index spatial pour trouver les candidats
        nearest_ids = self.regard_index.nearestNeighbor(point, 5, max_distance)
        
        if not nearest_ids:
            return None
        
        # Trouver le plus proche
        min_distance = float('inf')
        nearest_regard = None
        
        for id in nearest_ids:
            request = QgsFeatureRequest().setFilterFid(id)
            regard = next(self.regard_layer.getFeatures(request))
            
            distance = point.distance(regard.geometry().asPoint())
            if distance < min_distance:
                min_distance = distance
                nearest_regard = regard
        
        return nearest_regard
    
    def _order_canalisations(self, canalisations):
        """Ordonne les canalisations pour former un chemin continu en respectant le sens de tracé."""
        if not canalisations:
            return []
        
        # Si une seule canalisation, pas besoin de trier
        if len(canalisations) == 1:
            return canalisations
        
        # Créer un graphe orienté des canalisations (respectant le sens de tracé)
        graph = {}
        start_regards = {}  # Dictionnaire des regards amont
        end_regards = {}    # Dictionnaire des regards aval
        
        # Pour chaque canalisation, trouver les regards à ses extrémités
        for cana in canalisations:
            # Gérer différents types de géométrie (LineString et MultiLineString)
            geom = cana.geometry()
            if geom.isMultipart():
                # Pour une MultiLineString, extraire les points du premier et du dernier segment
                multi_polyline = geom.asMultiPolyline()
                if not multi_polyline:
                    continue  # Géométrie vide ou invalide
                    
                # Prendre les points extrêmes (premier point du premier segment et dernier point du dernier segment)
                start_point = QgsPointXY(multi_polyline[0][0])
                end_point = QgsPointXY(multi_polyline[-1][-1])
            else:
                # Pour une simple LineString
                polyline = geom.asPolyline()
                if not polyline:
                    continue  # Géométrie vide ou invalide
                    
                start_point = QgsPointXY(polyline[0])
                end_point = QgsPointXY(polyline[-1])
            
            # Trouver les regards aux extrémités
            start_regard = self._find_nearest_regard(start_point)
            end_regard = self._find_nearest_regard(end_point)
            
            if not start_regard or not end_regard:
                continue
            
            start_id = start_regard.id()
            end_id = end_regard.id()
            
            # Enregistrer les regards de début et de fin pour cette canalisation
            start_regards[cana.id()] = start_id
            end_regards[cana.id()] = end_id
            
            # Ajouter au graphe (orienté selon le sens de tracé)
            if start_id not in graph:
                graph[start_id] = []
            
            # Ajouter seulement dans le sens de la géométrie (start_id -> end_id)
            graph[start_id].append((end_id, cana))
            
            # S'assurer que le nœud d'arrivée existe aussi dans le graphe
            if end_id not in graph:
                graph[end_id] = []
        
        # Trouver les regards qui sont uniquement des points de départ (sans arrivée)
        potential_starts = set()
        for node_id, neighbors in graph.items():
            # Si le nœud a des voisins sortants mais n'est pas une destination
            if neighbors and node_id not in [end for node, neighbors in graph.items() for end, _ in neighbors]:
                potential_starts.add(node_id)
        
        # S'il n'y a pas de point de départ évident, chercher un nœud avec peu de connexions entrantes
        if not potential_starts:
            # Compter les connexions entrantes pour chaque nœud
            incoming = {node_id: 0 for node_id in graph}
            for node_id, neighbors in graph.items():
                for end_id, _ in neighbors:
                    incoming[end_id] = incoming.get(end_id, 0) + 1
            
            # Trouver les nœuds avec le moins de connexions entrantes
            min_incoming = min(incoming.values()) if incoming else 0
            potential_starts = {node_id for node_id, count in incoming.items() if count == min_incoming and graph.get(node_id)}
        
        # Prendre le premier nœud de départ potentiel
        start_id = next(iter(potential_starts)) if potential_starts else None
        
        # Si toujours pas de nœud de départ, prendre le premier nœud qui a des voisins
        if start_id is None:
            for node_id, neighbors in graph.items():
                if neighbors:
                    start_id = node_id
                    break
        
        # Si toujours pas de nœud de départ, retourner les canalisations non triées
        if start_id is None:
            print("Impossible de déterminer un point de départ, canalisations non triées")
            return canalisations
        
        # Parcours en profondeur pour trouver un chemin en suivant le sens des canalisations
        visited_nodes = set()
        visited_canas = set()
        ordered_canas = []
        
        def dfs(node_id):
            visited_nodes.add(node_id)
            
            for neighbor_id, cana in graph.get(node_id, []):
                if cana.id() not in visited_canas:
                    ordered_canas.append(cana)
                    visited_canas.add(cana.id())
                    
                    if neighbor_id not in visited_nodes:
                        dfs(neighbor_id)
        
        dfs(start_id)
        
        # Si toutes les canalisations ne sont pas dans le chemin, essayer d'autres points de départ
        while len(ordered_canas) < len(canalisations) and potential_starts:
            potential_starts.discard(start_id)
            if potential_starts:
                start_id = next(iter(potential_starts))
                if start_id not in visited_nodes:
                    dfs(start_id)
        
        # Si toujours des canalisations manquantes, les ajouter à la fin
        remaining_canas = [cana for cana in canalisations if cana.id() not in visited_canas]
        ordered_canas.extend(remaining_canas)
        
        # Afficher les informations sur l'ordre des canalisations
        print(f"Ordonnancement des canalisations: {len(ordered_canas)}/{len(canalisations)} ordonnées selon le sens de tracé")
        for i, cana in enumerate(ordered_canas):
            start_id = start_regards.get(cana.id(), "?")
            end_id = end_regards.get(cana.id(), "?")
            print(f"  {i+1}. Cana {cana.id()}: regard {start_id} → regard {end_id}")
        
        return ordered_canas

    def _find_shortest_path(self, start_regard, end_regard):
        """Trouve le chemin le plus court entre deux regards.
        
        Args:
            start_regard: Regard de départ
            end_regard: Regard d'arrivée
        """
        # Créer un graphe orienté des canalisations
        graph = {}
        
        # Charger toutes les canalisations et créer le graphe
        for cana in self.cana_layer.getFeatures():
            line_geom = cana.geometry().asPolyline()
            start_point = QgsPointXY(line_geom[0])
            end_point = QgsPointXY(line_geom[-1])
            
            cana_start_regard = self._find_nearest_regard(start_point)
            cana_end_regard = self._find_nearest_regard(end_point)
            
            if not cana_start_regard or not cana_end_regard:
                continue
            
            start_id = cana_start_regard.id()
            end_id = cana_end_regard.id()
            
            # Ajouter au graphe (orientation selon sens d'écoulement)
            if start_id not in graph:
                graph[start_id] = []
            
            # Poids = longueur de la canalisation
            weight = self.distance_area.measureLength(cana.geometry())
            graph[start_id].append((end_id, weight, cana))
        
        # Algorithme de Dijkstra pour trouver le chemin le plus court
        start_id = start_regard.id()
        end_id = end_regard.id()
        
        if start_id not in graph or end_id not in graph:
            return None
        
        # Initialisation
        distances = {node: float('inf') for node in graph}
        distances[start_id] = 0
        previous = {node: None for node in graph}
        previous_cana = {node: None for node in graph}
        unvisited = set(graph.keys())
        
        while unvisited:
            # Trouver le nœud non visité avec la plus petite distance
            current = min(unvisited, key=lambda node: distances[node])
            
            # Si le nœud actuel est le nœud cible, on a trouvé le chemin
            if current == end_id:
                break
            
            # Si la distance est infinie, il n'y a plus de chemin
            if distances[current] == float('inf'):
                break
            
            unvisited.remove(current)
            
            # Mettre à jour les distances des voisins
            for neighbor, weight, cana in graph.get(current, []):
                alt_distance = distances[current] + weight
                if alt_distance < distances[neighbor]:
                    distances[neighbor] = alt_distance
                    previous[neighbor] = current
                    previous_cana[neighbor] = cana
        
        # Reconstituer le chemin
        if previous[end_id] is None:
            return None  # Pas de chemin trouvé
        
        path = []
        current = end_id
        
        while current != start_id:
            cana = previous_cana[current]
            path.insert(0, cana)  # Insérer au début pour avoir le bon ordre
            current = previous[current]
        
        return path
    
    def _get_numeric_attribute(self, feature, field_name):
        """Récupère un attribut numérique d'une entité.
        
        Args:
            feature: Entité QGIS
            field_name: Nom du champ
        """
        if not field_name:
            return None
            
        # Vérifier si le champ existe dans la couche
        if field_name not in feature.fields().names():
            print(f"Le champ '{field_name}' n'existe pas dans la couche")
            return None
        
        # Récupérer la valeur brute et ajouter un débogage
        value = feature[field_name]
        print(f"Valeur brute du champ '{field_name}' pour l'entité {feature.id()}: {value} (type: {type(value).__name__})")
        
        # Gérer les valeurs NULL ou vides
        if value == NULL or value == '' or value is None:
            return None
        
        # Essayer de convertir en float
        try:
            # Si c'est une chaîne, nettoyer d'abord (remplacer virgule par point, etc.)
            if isinstance(value, str):
                value = value.replace(',', '.').strip()
                # Si la chaîne est vide après nettoyage
                if not value:
                    return None
            return float(value)
        except (ValueError, TypeError) as e:
            print(f"Erreur lors de la conversion en float pour '{field_name}': {e}, valeur: {value}")
            return None