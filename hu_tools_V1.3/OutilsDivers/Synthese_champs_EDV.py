# -*- coding: utf-8 -*-
"""
Script pour générer un tableau Excel de synthèse des champs présents dans différentes couches QGIS
"""
from qgis.core import (QgsProcessing, QgsProcessingAlgorithm, QgsProcessingParameterMultipleLayers, 
                      QgsProcessingParameterFileDestination, QgsProcessingParameterFile)
import os

class Synthese_champs_EDV(QgsProcessingAlgorithm):
    def __init__(self):
            super().__init__()  # Obligatoire pour QGIS
            
    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                'INPUT',
                'Couches en entrée',
                layerType=QgsProcessing.TypeVector
            )
        )
        self.addParameter(
            QgsProcessingParameterFile(
                'OUTPUT_FOLDER',
                'Dossier de sortie',
                behavior=QgsProcessingParameterFile.Folder
            )
        )

    def generate_unique_filename(self, folder, base_name='synthese_champs_couches', extension='.xlsx'):
        file_path = os.path.join(folder, f"{base_name}{extension}")
        counter = 1
        while os.path.exists(file_path):
            file_path = os.path.join(folder, f"{base_name}_{counter}{extension}")
            counter += 1
        return file_path


    def processAlgorithm(self, parameters, context, feedback):
        try:
            try:
                import pandas as pd
            except Exception as e:
                feedback.reportError("Le module Python 'pandas' est introuvable dans l'environnement de QGIS. "
                                     "Installez pandas ou activez l'environnement Python contenant pandas.")
                return {}
    
            input_layers = self.parameterAsLayerList(parameters, 'INPUT', context)
            output_folder = self.parameterAsString(parameters, 'OUTPUT_FOLDER', context)
            output_file = self.generate_unique_filename(output_folder)

            #output_file = self.parameterAsString(parameters, 'OUTPUT', context)
            
            # Dictionnaire qui stockera les informations sur tous les champs
            field_info = {}
            layer_names = []
            
            total_layers = len(input_layers)
            
            # Parcours de toutes les couches
            for idx, layer in enumerate(input_layers):
                feedback.setProgress(int(idx * 100 / total_layers))
                layer_name = layer.name()
                layer_names.append(layer_name)
                
                feedback.pushInfo(f"Traitement de la couche: {layer_name}")
                
                # Parcourir tous les champs de la couche
                fields = layer.fields()
                for field in fields:
                    field_name = field.name()
                    field_type = field.typeName()
                    field_length = field.length()
                    field_precision = field.precision()
                    
                    # Si le champ n'existe pas encore dans notre dictionnaire
                    if field_name not in field_info:
                        field_info[field_name] = {
                            'type': field_type,
                            'length': field_length,
                            'precision': field_precision,
                            'layers': {layer_name: 'X'}
                        }
                    else:
                        # Mise à jour du dictionnaire existant
                        field_info[field_name]['layers'][layer_name] = 'X'
            
            # Création du dataframe pour l'export Excel
            rows = []
            for field_name, info in field_info.items():
                row = {
                    'Nom du champ': field_name,
                    'Type': info['type'],
                    'Longueur': info['length'],
                    'Précision': info['precision']
                }
                # Ajouter une colonne pour chaque couche
                for layer_name in layer_names:
                    row[layer_name] = info['layers'].get(layer_name, '')
                
                rows.append(row)
            
            import pandas as pd
            # Création du dataframe et export
            df = pd.DataFrame(rows)
            
            # Réorganiser les colonnes pour avoir le format demandé
            columns = ['Nom du champ', 'Type', 'Longueur', 'Précision'] + layer_names
            df = df[columns]
            
            # Export vers Excel
            try:
                df.to_excel(output_file, index=False)
                feedback.pushInfo(f"Fichier Excel créé avec succès: {output_file}")
                return {'OUTPUT': output_file}
            except Exception as e:
                feedback.reportError(f"Erreur lors de l'export Excel: {str(e)}")
                return {}
            
        except Exception as e:
            feedback.reportError(f"Erreur générale : {str(e)}")
            return {}
            
            
        
    def id(self):
        return 'synthesedeschamps'

    def name(self):
        return 'synthesedeschamps'

    def displayName(self):
        return 'Synthèse des champs'

    def group(self):
        return 'EDV'

    def groupId(self):
        return 'edv2'

    def createInstance(self):
        return Synthese_champs_EDV()

    def shortHelpString(self):
        return """
        Cet algorithme crée un tableau Excel de synthèse des champs présents dans différentes couches.
        
        Le tableau contient:
        - Les noms des champs
        - Leurs types
        - Leur longueur
        - Leur précision
        - Pour chaque couche, une croix (X) si le champ est présent
        
        Le résultat est un fichier Excel qui peut être utilisé pour comparer la structure des couches.
        """