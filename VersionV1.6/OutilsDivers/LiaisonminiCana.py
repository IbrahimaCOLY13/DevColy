"""
Model exported as python.
Name : Liaison minicana
Group : _reconstruction des cana
With QGIS : 34007
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterField
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsProperty
import processing
from qgis.core import QgsVectorLayer
from qgis.core import QgsProcessingException


class LiaisonMinicana(QgsProcessingAlgorithm):
    def __init__(self):
        super().__init__()  # Obligatoire pour QGIS

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('couche_de_cana', 'couche de cana', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('couche_de_regard', 'couche de regard', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterField('identifiant_unique_cana', 'Identifiant unique cana', type=QgsProcessingParameterField.Any, parentLayerParameterName='couche_de_cana', allowMultiple=False, defaultValue='OBJ_MATRIC'))
        self.addParameter(QgsProcessingParameterField('identifiant_unique_regard', 'Identifiant unique regard', type=QgsProcessingParameterField.Any, parentLayerParameterName='couche_de_regard', allowMultiple=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Output_attention_croisement', 'OUTPUT_Attention_croisement', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Couche_regard_complte_avec_croisement', 'Couche_regard_complétée_avec_croisement', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue='TEMPORARY_OUTPUT'))
        self.addParameter(QgsProcessingParameterFeatureSink('Relation_canaregard_sans_croisement', 'Relation_cana-regard_sans_croisement', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue='TEMPORARY_OUTPUT'))
        self.addParameter(QgsProcessingParameterFeatureSink('CanaEnDouble', 'Cana en double', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(26, model_feedback)
        results = {}
        outputs = {}

        # Renommer le champ id regard
        alg_params = {
            'FIELD': parameters['identifiant_unique_regard'],
            'INPUT': parameters['couche_de_regard'],
            'NEW_NAME': 'idUnique_regard',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenommerLeChampIdRegard'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Renommer le champ id cana
        alg_params = {
            'FIELD': parameters['identifiant_unique_cana'],
            'INPUT': parameters['couche_de_cana'],
            'NEW_NAME': 'idUnique_cana',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenommerLeChampIdCana'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Extraire des sommets spécifiques
        alg_params = {
            'INPUT': parameters['couche_de_cana'],
            'VERTICES': '0,-1',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireDesSommetsSpcifiques'] = processing.run('native:extractspecificvertices', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Refactoriser les champs couches d'entrée pour fusion
        alg_params = {
            'FIELDS_MAPPING': [{'expression': 'idUnique_regard','length': 0,'name': 'idUnique_regard','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'expression': None,'length': 0,'name': 'Croisement','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'}],
            'INPUT': outputs['RenommerLeChampIdRegard']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RefactoriserLesChampsCouchesDentrePourFusion'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Point centrale des lignes
        alg_params = {
            'DISTANCE': QgsProperty.fromExpression('$length/2'),
            'INPUT': outputs['RenommerLeChampIdCana']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['PointCentraleDesLignes'] = processing.run('native:interpolatepoint', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Différence sommet-regard
        alg_params = {
            'GRID_SIZE': None,
            'INPUT': outputs['ExtraireDesSommetsSpcifiques']['OUTPUT'],
            'OVERLAY': parameters['couche_de_regard'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DiffrenceSommetregard'] = processing.run('native:difference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Tampon point centrale
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 0.1,
            'END_CAP_STYLE': 0,  # Rond
            'INPUT': outputs['PointCentraleDesLignes']['OUTPUT'],
            'JOIN_STYLE': 0,  # Rond
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['TamponPointCentrale'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Tampon
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 0.1,
            'END_CAP_STYLE': 0,  # Rond
            'INPUT': outputs['DiffrenceSommetregard']['OUTPUT'],
            'JOIN_STYLE': 0,  # Rond
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Tampon'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Lste des canas qui intercsete le point central
        #cana_layer = outputs['RenommerLeChampIdCana']['OUTPUT']  # couche temporaire valide
        #cana_layer_path = outputs['RenommerLeChampIdCana']['OUTPUT']  # c'est une str
        #cana_layer = QgsVectorLayer(cana_layer_path, "cana_temp", "ogr")
        #if not cana_layer.isValid():
        #    raise QgsProcessingException("La couche idCana n'est pas valide.")
        alg_params = {
            'FIELD_LENGTH': 250,
            'FIELD_NAME': 'Liste_cana',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 8,  # Liste de chaîne de caractères
            'FORMULA': 'overlay_crosses(  @Renommer_le_champ_id_cana_OUTPUT  , "idUnique_cana"  )', # FORMULA': f'overlay_crosses("{cana_layer.name()}", "idUnique_cana")', #
            'INPUT': outputs['TamponPointCentrale']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['LsteDesCanasQuiIntercseteLePointCentral'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        # 

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Supprime les géométries nulles
        alg_params = {
            'INPUT': outputs['Tampon']['OUTPUT'],
            'REMOVE_EMPTY': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SupprimeLesGomtriesNulles'] = processing.run('native:removenullgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Supprimer les sommets en double
        alg_params = {
            'INPUT': outputs['SupprimeLesGomtriesNulles']['OUTPUT'],
            'TOLERANCE': 1e-06,
            'USE_Z_VALUE': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SupprimerLesSommetsEnDouble'] = processing.run('native:removeduplicatevertices', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Ajout du champs Rang
        alg_params = {
            'FIELD_NAME': 'Rang',
            'GROUP_FIELDS': [''],
            'INPUT': outputs['SupprimerLesSommetsEnDouble']['OUTPUT'],
            'MODULUS': 0,
            'SORT_ASCENDING': True,
            'SORT_EXPRESSION': None,
            'SORT_NULLS_FIRST': False,
            'START': 0,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AjoutDuChampsRang'] = processing.run('native:addautoincrementalfield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Filtre sur les liste pour récupérer ceux à plus de 2
        alg_params = {
            'INPUT': outputs['LsteDesCanasQuiIntercseteLePointCentral']['OUTPUT'],
            'OUTPUT_': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FiltreSurLesListePourRcuprerCeuxPlusDe2'] = processing.run('native:filter', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Conserver le champs Rang
        alg_params = {
            'FIELDS': ['Rang'],
            'INPUT': outputs['AjoutDuChampsRang']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ConserverLeChampsRang'] = processing.run('native:retainfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Supprimer les doublons par attribut
        alg_params = {
            'FIELDS': ['Liste_cana'],
            'INPUT': outputs['FiltreSurLesListePourRcuprerCeuxPlusDe2']['OUTPUT_'],
            'OUTPUT': parameters['CanaEnDouble']
        }
        outputs['SupprimerLesDoublonsParAttribut'] = processing.run('native:removeduplicatesbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['CanaEnDouble'] = outputs['SupprimerLesDoublonsParAttribut']['OUTPUT']

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Calcul champs Liste_paire
        alg_params = {
            'FIELD_LENGTH': 80,
            'FIELD_NAME': 'Liste_paire',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': 'array_to_string( overlay_crosses(  @Renommer_le_champ_id_cana_OUTPUT  , "idUnique_cana"  ) ,\';\')',
            'INPUT': outputs['ConserverLeChampsRang']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculChampsListe_paire'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Calcul champs Croisement
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Croisement',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': ' Case\r\n\twhen  array_length( string_to_array( "Liste_paire",\';\'))>2 then \'oui\'\r\n\telse \'non\'\r\n end',
            'INPUT': outputs['CalculChampsListe_paire']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculChampsCroisement'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # Filtre d'entité
        alg_params = {
            'INPUT': outputs['CalculChampsCroisement']['OUTPUT'],
            'OUTPUT_Attention_croisement': parameters['Output_attention_croisement'],
            'OUTPUT_Relation_cana-regard': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FiltreDentit'] = processing.run('native:filter', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Output_attention_croisement'] = outputs['FiltreDentit']['OUTPUT_Attention_croisement']

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # Supprimer les doublons par attribut
        alg_params = {
            'FIELDS': ['Liste_paire'],
            'INPUT': outputs['FiltreDentit']['OUTPUT_Attention_croisement'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SupprimerLesDoublonsParAttribut'] = processing.run('native:removeduplicatesbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # Différence avec croisement
        alg_params = {
            'GRID_SIZE': None,
            'INPUT': outputs['CalculChampsCroisement']['OUTPUT'],
            'OVERLAY': outputs['FiltreDentit']['OUTPUT_Attention_croisement'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DiffrenceAvecCroisement'] = processing.run('native:difference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        # Refactoriser les champs de la couche croisement pour fusion
        alg_params = {
            'FIELDS_MAPPING': [{'expression': 'Rang','length': 0,'name': 'idUnique_regard','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'expression': 'Croisement','length': 0,'name': 'Croisement','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'}],
            'INPUT': outputs['SupprimerLesDoublonsParAttribut']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RefactoriserLesChampsDeLaCoucheCroisementPourFusion'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(21)
        if feedback.isCanceled():
            return {}

        # transformation polygone en point pour fusionner
        alg_params = {
            'ALL_PARTS': False,
            'INPUT': outputs['RefactoriserLesChampsDeLaCoucheCroisementPourFusion']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['TransformationPolygoneEnPointPourFusionner'] = processing.run('native:centroids', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(22)
        if feedback.isCanceled():
            return {}

        # Calcul champs Cana1
        alg_params = {
            'FIELD_LENGTH': 50,
            'FIELD_NAME': 'Cana1',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': ' array_first(  string_to_array( "Cana" , \';\' ))',
            'INPUT': outputs['DiffrenceAvecCroisement']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculChampsCana1'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(23)
        if feedback.isCanceled():
            return {}

        # Fusionner des couches vecteur
        alg_params = {
            'CRS': None,
            'LAYERS': [outputs['TransformationPolygoneEnPointPourFusionner']['OUTPUT'],outputs['RefactoriserLesChampsCouchesDentrePourFusion']['OUTPUT']],
            'OUTPUT': parameters['Couche_regard_complte_avec_croisement']
        }
        outputs['FusionnerDesCouchesVecteur'] = processing.run('native:mergevectorlayers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Couche_regard_complte_avec_croisement'] = outputs['FusionnerDesCouchesVecteur']['OUTPUT']

        feedback.setCurrentStep(24)
        if feedback.isCanceled():
            return {}

        # Calcul champs Cana2
        alg_params = {
            'FIELD_LENGTH': 50,
            'FIELD_NAME': 'Cana2',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': ' array_last(  string_to_array( "Cana",\';\'))',
            'INPUT': outputs['CalculChampsCana1']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculChampsCana2'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(25)
        if feedback.isCanceled():
            return {}

        # Supprimer les doublons de point intermediaire avec le champ Liste_paire
        alg_params = {
            'FIELDS': ['Liste_paire'],
            'INPUT': outputs['CalculChampsCana2']['OUTPUT'],
            'OUTPUT': parameters['Relation_canaregard_sans_croisement']
        }
        outputs['SupprimerLesDoublonsDePointIntermediaireAvecLeChampListe_paire'] = processing.run('native:removeduplicatesbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Relation_canaregard_sans_croisement'] = outputs['SupprimerLesDoublonsDePointIntermediaireAvecLeChampListe_paire']['OUTPUT']
        return results
        
    def id(self):
        return 'LiaisonMinicana'

    def name(self):
        return 'LiaisonMinicana'

    def displayName(self):
        return 'Liaison minicana'

    def group(self):
        return 'Reconstruction des cana'

    def groupId(self):
        return 'liaisonminicana'

    def createInstance(self):
        return LiaisonMinicana()
