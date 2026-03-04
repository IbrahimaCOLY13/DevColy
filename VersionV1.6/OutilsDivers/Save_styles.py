from qgis.core import QgsProcessingAlgorithm, QgsProcessingParameterMultipleLayers, QgsProcessingParameterFolderDestination, QgsProcessing, QgsProcessingException
from qgis.PyQt.QtCore import QCoreApplication
import os

class EnregistrerStylesCouches(QgsProcessingAlgorithm):
    """
       Permet de sauvegarder tous les styles contenu dans les couches sélectionnées
    """
    def __init__(self):
        super().__init__()  # Obligatoire pour QGIS

    INPUT_LAYERS = 'INPUT_LAYERS'
    OUTPUT_FOLDER = 'OUTPUT_FOLDER'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return EnregistrerStylesCouches()
        
    def id(self):
        return 'enregistrerstyles'

    def name(self):
        return 'enregistrerstyles'

    def displayName(self):
        return self.tr('Enregistrer tous les styles des couches')

    def group(self):
        return 'EnregistrerStyles'

    def groupId(self):
        return 'enregistrerstyle'

    def shortHelpString(self):
        return self.tr('Enregistre tous les styles QML (y compris les styles nommés) de toutes les couches sélectionnées dans un dossier')

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_LAYERS,
                self.tr('Couches sélectionnées'),
                QgsProcessing.TypeMapLayer
            )
        )
        
        self.addParameter(
            QgsProcessingParameterFolderDestination(
                self.OUTPUT_FOLDER,
                self.tr('Dossier de destination')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        layers = self.parameterAsLayerList(parameters, self.INPUT_LAYERS, context)
        output_folder = self.parameterAsString(parameters, self.OUTPUT_FOLDER, context)

        if not layers:
            raise QgsProcessingException(self.tr('Aucune couche sélectionnée'))

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        total_styles = 0
        current_progress = 0
        
        # Compter le nombre total de styles
        for layer in layers:
            style_manager = layer.styleManager()
            total_styles += len(style_manager.styles())
        
        total = 100.0 / total_styles if total_styles > 0 else 0
        
        for layer in layers:
            if feedback.isCanceled():
                break

            layer_name = layer.name()
            safe_layer_name = "".join([c for c in layer_name if c.isalnum() or c in (' ', '-', '_')]).rstrip()
            
            style_manager = layer.styleManager()
            style_names = style_manager.styles()
            current_style = style_manager.currentStyle()
            
            feedback.pushInfo(self.tr(f'\n=== Couche : {layer_name} ({len(style_names)} style(s)) ==='))
            
            for style_name in style_names:
                if feedback.isCanceled():
                    break
                
                # Changer vers le style à enregistrer
                style_manager.setCurrentStyle(style_name)
                
                # Créer un nom de fichier sécurisé
                safe_style_name = "".join([c for c in style_name if c.isalnum() or c in (' ', '-', '_')]).rstrip()
                
                if safe_style_name:
                    output_file = os.path.join(output_folder, f"{safe_layer_name}_{safe_style_name}.qml")
                else:
                    output_file = os.path.join(output_folder, f"{safe_layer_name}_default.qml")
                
                feedback.pushInfo(self.tr(f'  → Enregistrement du style "{style_name}"...'))
                
                # Enregistrer le style
                layer.saveNamedStyle(output_file)
                feedback.pushInfo(self.tr(f'    Style enregistré : {output_file}'))
                
                current_progress += 1
                feedback.setProgress(int(current_progress * total))
            
            # Restaurer le style original
            style_manager.setCurrentStyle(current_style)

        feedback.pushInfo(self.tr(f'\n✓ {total_styles} style(s) enregistré(s) avec succès dans {output_folder}'))
        
        return {self.OUTPUT_FOLDER: output_folder}