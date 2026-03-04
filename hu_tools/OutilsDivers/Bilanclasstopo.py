"""
Model exported as python.
Name : statistiques_SDAEU_v4
Group : 
With QGIS : 34005
"""

from qgis.core import (QgsProcessing, QgsProcessingAlgorithm, QgsProcessingParameterMultipleLayers, QgsProcessingParameterFile)
import os

class Statistiques_SDAEU_v4(QgsProcessingAlgorithm):
    def __init__(self):
        super().__init__()  # Obligatoire pour QGIS
        
    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                'INPUT',
                'Couches d’entrée',
                layerType=QgsProcessing.TypeVectorPoint
            )
        )
        self.addParameter(
            QgsProcessingParameterFile(
                'OUTPUT_FOLDER',
                'Dossier de sortie',
                behavior=QgsProcessingParameterFile.Folder
            )
        )

    def safe_convert_to_float(self, value):
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return float(value)
        
        # Pour les chaînes de caractères
        if isinstance(value, str):
            # Supprimer les espaces
            value = value.strip()
            # Si chaîne vide, retourner None
            if value == "":
                return None
            try:
                # Remplacer la virgule par un point pour la conversion
                return float(value.replace(',', '.'))
            except ValueError:
                # Si conversion impossible, retourner None
                return None
        return None

    def analyze_layer(self, layer, feedback):
        try:
            # Récupérer le chemin du fichier source
            source_path = layer.source()
            file_name = os.path.basename(source_path) if source_path else "Non disponible"
            
            stats = {
                'nom_couche': layer.name(),
                'fichier_source': file_name,
                'nbTotal': layer.featureCount(),
                'nbClasseA': 0,
                'nbClasAok': 0,
                'nbAIncomplet': 0,
                'nbAIncompletCoorlamf': 0,
                'nbAIncompletProfond': 0,
                'nbClasAutr': 0,
                'nbClasNull': 0,
                'champs_manquants': []
            }
            
            # Vérifier les champs requis
            fields = layer.fields()
            field_names = [field.name() for field in fields]
            required_fields = ['CLASSE', 'COORLAMF', 'PROFOND', 'COORLAMZ', 'E_HRMS']
            
            for field in required_fields:
                if field not in field_names:
                    stats['champs_manquants'].append(field)
                    feedback.pushInfo(f"Champ '{field}' manquant dans la couche {layer.name()}")
            
            # Regrouper les champs manquants en une seule chaîne pour l'export Excel
            if stats['champs_manquants']:
                stats['champs_manquants'] = ", ".join(stats['champs_manquants'])
            else:
                stats['champs_manquants'] = "Aucun"
            
            # Vérifier si on peut faire les calculs basés sur les champs requis
            has_classe = 'CLASSE' in field_names
            has_coorlamf = 'COORLAMF' in field_names
            has_profond = 'PROFOND' in field_names
            
            for feature in layer.getFeatures():
                # Récupérer les attributs avec gestion des champs manquants
                classe = feature.attribute('CLASSE') if 'CLASSE' in field_names else None
                coorlamf = feature.attribute('COORLAMF') if 'COORLAMF' in field_names else None
                profond = feature.attribute('PROFOND') if 'PROFOND' in field_names else None
                
                # Convertir les valeurs en nombres (gérant les , et . comme séparateurs)
                coorlamf_num = self.safe_convert_to_float(coorlamf)
                profond_num = self.safe_convert_to_float(profond)
                
                # Vérifications pour les erreurs
                error_coorlamf = coorlamf_num is None or coorlamf_num <= 0
                error_profond = profond_num is None or profond_num <= 0
                
                if has_classe and (classe == '01' or classe == 1):
                    stats['nbClasseA'] += 1
                    
                    if error_coorlamf or error_profond:
                        stats['nbAIncomplet'] += 1
                        
                        if error_coorlamf:
                            stats['nbAIncompletCoorlamf'] += 1
                        
                        if error_profond:
                            stats['nbAIncompletProfond'] += 1

                    # nbClasAok: CLASSE = 1, COORLAMF >0 et PROFOND >0
                    elif coorlamf_num is not None and coorlamf_num > 0 and profond_num is not None and profond_num > 0:
                        stats['nbClasAok'] += 1

                # nbClasAutr: CLASSE différent de 1 et différent de NULL
                elif has_classe and classe != '01' and classe is not None:
                    stats['nbClasAutr'] += 1

            return stats
        except Exception as e:
            feedback.reportError(str(e))
            return None

    def generate_unique_filename(self, base_path, base_name='statistiques_globales', extension='.xlsx'):
        """
        Génère un nom de fichier unique en ajoutant un incrément si le fichier existe déjà.
        """
        file_path = os.path.join(base_path, f"{base_name}{extension}")
        counter = 1
        
        while os.path.exists(file_path):
            file_path = os.path.join(base_path, f"{base_name}_{counter}{extension}")
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
            
            all_stats = []
            total_layers = len(input_layers)
            
            for i, layer in enumerate(input_layers):
                feedback.setProgress(int((i/total_layers) * 100))
                
                if feedback.isCanceled():
                    return {}
                    
                feedback.pushInfo(f"Traitement de la couche : {layer.name()}")
                stats = self.analyze_layer(layer, feedback)
                
                if stats:
                    all_stats.append(stats)
                else:
                    feedback.reportError(f"Échec de l'analyse pour la couche {layer.name()}")

            if not all_stats:
                feedback.reportError("Aucune statistique n'a pu être calculée")
                return {}

            import pandas as pd

            # Générer un nom de fichier unique en .xlsx
            output_file = self.generate_unique_filename(output_folder, extension='.xlsx')
            df = pd.DataFrame(all_stats)
            try:
                # Export Excel avec xlsxwriter
                df.to_excel(output_file, index=False, engine='xlsxwriter')
                feedback.pushInfo(f"Fichier Excel créé : {output_file}")
                return {'OUTPUT': output_file}
            except Exception as e:
                feedback.reportError(f"Erreur lors de l'export Excel : {str(e)}")
                return {}

        except Exception as e:
            feedback.reportError(f"Erreur générale : {str(e)}")
            return {}

    def id(self):
        return 'statistiques_SDAEU_v4'

    def name(self):
        return 'statistiques_SDAEU_v4'

    def displayName(self):
        return 'Statistiques SDAEU v4'

    def group(self):
        return 'EDV'

    def groupId(self):
        return 'edv'

    def createInstance(self):
        return Statistiques_SDAEU_v4()

    def shortHelpString(self):
        return """<html><body><p><!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><style type="text/css">
p, li { white-space: pre-wrap; }
</style></head><body style=" font-family:'MS Shell Dlg 2'; font-size:8.3pt; font-weight:400; font-style:normal;">
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">Cet outil permet de générer un tableur Excel statistique avec le décompte des entités suivant :</p>
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"> - Nombre d'entités annoncées par le MO en classe A </p>
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">-  Nombre d'entités annoncées en classe A mais pour lesquelles il manque des données</p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">   * Détail des erreurs liées à COORLAMF</p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">   * Détail des erreurs liées à PROFOND</p>
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">-  Nombre d'entités en classe autre que A</p>
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">-  Nombre total d'entités</p>
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p></body></html></p>
<br></body></html>"""