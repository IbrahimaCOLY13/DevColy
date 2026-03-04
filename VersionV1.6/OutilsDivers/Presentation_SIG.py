"""
Model exported as python.
Name : Présentation SIG
Group : 
With QGIS : 34007
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFile
from qgis.core import QgsProcessingParameterString
import processing


class PresentationSig(QgsProcessingAlgorithm):
    def __init__(self):
        super().__init__()  # Obligatoire pour QGIS

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFile('chemin_du_logo', 'Chemin du Logo', behavior=QgsProcessingParameterFile.File, fileFilter='Tous les fichiers (*.*)', defaultValue='R:\\SIG\\06_Elements_de_legende\\Logos'))
        self.addParameter(QgsProcessingParameterString('commune_de_', 'Commune de ...', multiLine=False, defaultValue='Commune de '))
        self.addParameter(QgsProcessingParameterString('maitre_douvrage', "Maitre d'ouvrage", multiLine=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterString('titre', 'Titre', multiLine=False, defaultValue="Étude de diagnostic des systèmes d'assainissement collectif"))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(4, model_feedback)
        results = {}
        outputs = {}

        # Définir une variable projet
        alg_params = {
            'NAME': "Chemin vers le logo maitre d'ouvrage",
            'VALUE': parameters['chemin_du_logo']
        }
        outputs['DefinirUneVariableProjet'] = processing.run('native:setprojectvariable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Définir une variable projet
        alg_params = {
            'NAME': 'Commune',
            'VALUE': parameters['commune_de_']
        }
        outputs['DefinirUneVariableProjet'] = processing.run('native:setprojectvariable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Définir une variable projet
        alg_params = {
            'NAME': 'MO',
            'VALUE': parameters['maitre_douvrage']
        }
        outputs['DefinirUneVariableProjet'] = processing.run('native:setprojectvariable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Définir une variable projet
        alg_params = {
            'NAME': 'Commune',
            'VALUE': parameters['titre']
        }
        outputs['DefinirUneVariableProjet'] = processing.run('native:setprojectvariable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results
        
    def id(self):
        return 'PresentationSIG'

    def name(self):
        return 'PresentationSIG'

    def displayName(self):
        return 'Présentation SIG'

    def group(self):
        return 'PrésentationSIG'

    def groupId(self):
        return 'presentationSig'

    def createInstance(self):
        return PresentationSig()
        
    def shortHelpString(self):
        return """
        Cet algorithme permet d'importer le modèle PrésentationSIG qui ajoute des variables au projet pour harmoniser les rendus.
        
        Variables :
        - le logo
        - La commune
        - Le MO
        - Le titre
        """