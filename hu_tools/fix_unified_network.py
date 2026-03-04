# -*- coding: utf-8 -*-
"""
Script pour remplacer complètement la section du check_flow_direction
afin de traiter tous les réseaux gravitaires ensemble au lieu de séparément
"""

import re

file_path = r"c:\Users\m.vincent\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\hu_tools\modules\Topologycheckers.py"

# Lire le fichier
with open(file_path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Définir le code de remplacement pour toute la section après les vérifications initiales
new_section = '''        # Préparer un cache unifié de TOUTES les canalisations gravitaires
        # Cela permet de gérer les connexions entre différents types de réseaux (EU→UNI, EP→UNI, etc.)
        self.log(f"\\nPréparation du cache unifié des canalisations gravitaires...")
        QApplication.processEvents()
        
        unified_pipe_cache = {}
        network_layers_map = {}  # Pour retrouver la couche source de chaque canalisation
        
        for network_type in ['network_eu', 'network_uni', 'network_ep']:
            network_layer = self.layers.get(network_type)
            if not network_layer:
                self.log(f"   Réseau {network_type.upper()} : ✖ Non défini, ignoré")
                continue
            
            # Préparer le cache pour ce réseau
            pipe_cache = self._prepare_pipe_cache(network_layer)
            self.log(f"   Réseau {network_type.upper()} ({network_layer.name()}) : {len(pipe_cache)} canalisations")
            QApplication.processEvents()
            
            # Ajouter au cache unifié avec préfixe pour éviter les collisions d'ID
            for pipe_id, pipe_data in pipe_cache.items():
                unified_key = f"{network_type}_{pipe_id}"
                unified_pipe_cache[unified_key] = pipe_data
                network_layers_map[unified_key] = (network_layer, pipe_id)
        
        if not unified_pipe_cache:
            self.log(f"\\n✖✖ Aucune canalisation gravitaire trouvée")
            QApplication.processEvents()
            return errors
        
        self.log(f"\\n✓✓ Total : {len(unified_pipe_cache)} canalisations gravitaires chargées")
        QApplication.processEvents()
        
        # Récupérer toutes les couches de points (regards/boîtes) pour tous les réseaux
        self.log(f"\\nChargement des couches de points...")
        QApplication.processEvents()
        
        all_point_layers = []
        all_point_indexes = []
        point_layer_names = ['manhole_eu', 'box_eu', 'manhole_uni', 'box_uni', 'manhole_ep', 'box_ep']
        
        for pt_name in point_layer_names:
            pt_layer = self.layers.get(pt_name)
            if pt_layer:
                all_point_layers.append(pt_layer)
                all_point_indexes.append(self.ensure_index(pt_layer))
                self.log(f"   ✓ {pt_layer.name()}")
        
        # Trouver tous les exutoires (canalisations connectées aux PR/STEU)
        self.log(f"\\nRecherche des exutoires (PR/STEU)...")
        QApplication.processEvents()
        
        outlets = []
        search_tolerance = self.connection_tolerance
        
        # Chercher les connexions aux PR
        if pr_layer:
            for pr_feat in pr_layer.getFeatures():
                pr_geom = pr_feat.geometry()
                if not pr_geom or pr_geom.isEmpty():
                    continue
                
                # Vérifier toutes les canalisations
                for unified_key, pipe_data in unified_pipe_cache.items():
                    end_pt = pipe_data['end_point']
                    end_buf = QgsGeometry.fromPointXY(end_pt).buffer(search_tolerance, 5)
                    
                    if pr_geom.intersects(end_buf):
                        outlets.append((unified_key, 'PR'))
        
        # Chercher les connexions aux STEU
        if steu_layer:
            for steu_feat in steu_layer.getFeatures():
                steu_geom = steu_feat.geometry()
                if not steu_geom or steu_geom.isEmpty():
                    continue
                
                # Vérifier toutes les canalisations
                for unified_key, pipe_data in unified_pipe_cache.items():
                    end_pt = pipe_data['end_point']
                    end_buf = QgsGeometry.fromPointXY(end_pt).buffer(search_tolerance, 5)
                    
                    if steu_geom.intersects(end_buf):
                        outlets.append((unified_key, 'STEU'))
        
        self.log(f"   ✓ {len(outlets)} exutoire(s) trouvé(s)")
        QApplication.processEvents()
        
        if not outlets:
            self.log(f"   ✖✖ ATTENTION : Aucun exutoire trouvé - tous les tronçons sont isolés")
            QApplication.processEvents()
            for unified_key, pipe_data in unified_pipe_cache.items():
                network_layer, original_id = network_layers_map[unified_key]
                errors.append(self.add_error(
                    "Sens d'écoulement",
                    f"Tronçon non connecté aux exutoires : ID {original_id} ({network_layer.name()}). Aucun exutoire (PR/STEU) trouvé.",
                    network_layer.name(),
                    original_id,
                    pipe_data['geometry']
                ))
            self.log(f"\\n=== FIN VÉRIFICATION SENS D'ÉCOULEMENT ===")
            self.log(f"✖✖ TOTAL : {len(errors)} erreur(s) détectée(s)")
            QApplication.processEvents()
            return errors
        
        # Remonter le réseau depuis chaque exutoire
        self.log(f"\\nParcours du réseau unifié depuis les exutoires...")
        QApplication.processEvents()
        processed_global = set()
        all_reversed = []
        
        for unified_key, outlet_type in outlets:
            network_layer, original_id = network_layers_map[unified_key]
            self.log(f"   Analyse depuis {outlet_type} - ID {original_id} ({network_layer.name()})...")
            
            visited, reversed_pipes = self._trace_unified_network(
                unified_key, unified_pipe_cache, None,
                all_point_indexes, all_point_layers, processed_global
            )
            
            all_reversed.extend(reversed_pipes)
        
        # Enregistrer les erreurs d'inversion
        if all_reversed:
            self.log(f"\\n✖ {len(all_reversed)} tronçon(s) INVERSÉ(S) détecté(s)")
            QApplication.processEvents()
            
        for rev_key in all_reversed:
            network_layer, original_id = network_layers_map[rev_key]
            pipe_data = unified_pipe_cache[rev_key]
            self.log(f"   ID {original_id} ({network_layer.name()}) : INVERSÉ")
            errors.append(self.add_error(
                "Sens d'écoulement",
                f"Sens d'écoulement inversé détecté : ID {original_id} ({network_layer.name()}). Le tronçon est tracé dans le sens inverse de l'écoulement.",
                network_layer.name(),
                original_id,
                pipe_data['geometry']
            ))
        
        # Détecter les tronçons isolés (non atteignables depuis les exutoires)
        unvisited = set(unified_pipe_cache.keys()) - processed_global
        if unvisited:
            self.log(f"\\n✖✖ {len(unvisited)} tronçon(s) NON connecté(s) aux exutoires")
            QApplication.processEvents()
            
        for unified_key in unvisited:
            network_layer, original_id = network_layers_map[unified_key]
            pipe_data = unified_pipe_cache[unified_key]
            self.log(f"   ID {original_id} ({network_layer.name()}) : NON connecté aux exutoires")
            errors.append(self.add_error(
                "Sens d'écoulement",
                f"Tronçon non connecté aux exutoires : ID {original_id} ({network_layer.name()}). Ne converge pas vers un PR ou une STEU.",
                network_layer.name(),
                original_id,
                pipe_data['geometry']
            ))
        
        # Résumé global
        self.log(f"\\n✓✓ RÉSUMÉ GLOBAL :")
        self.log(f"   Total canalisations analysées : {len(unified_pipe_cache)}")
        self.log(f"   Canalisations connectées : {len(processed_global)}")
        self.log(f"   Canalisations isolées : {len(unvisited)}")
        self.log(f"   Canalisations inversées : {len(all_reversed)}")
        QApplication.processEvents()
'''

# Trouver le début et la fin de la section à remplacer
start_marker = "        # Préparer un cache unifié de TOUTES les canalisations gravitaires"
end_marker = "            QApplication.processEvents()\n        \n        self.log(f\"\\n=== FIN VÉRIFICATION SENS D'ÉCOULEMENT ===\")"

start_pos = content.find(start_marker)
end_pos = content.find(end_marker)

if start_pos == -1:
    print("ERREUR : Impossible de trouver le début de la section")
elif end_pos == -1:
    print("ERREUR : Impossible de trouver la fin de la section")
else:
    # Remplacer la section
    new_content = content[:start_pos] + new_section + "\n        \n        self.log(f\"\\n=== FIN VÉRIFICATION SENS D'ÉCOULEMENT ===\")" + content[end_pos + len(end_marker):]
    
    # Écrire le nouveau contenu
    with open(file_path, 'w', encoding='utf-8-sig') as f:
        f.write(new_content)
    
    print("✓ Section remplacée avec succès !")
    print(f"  Position début : {start_pos}")
    print(f"  Position fin : {end_pos}")
