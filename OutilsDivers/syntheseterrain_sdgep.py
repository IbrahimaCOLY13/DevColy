"""
Model exported as python.
Name : SyntheseTerrain_SDGEP_v3
Group : 
With QGIS : 34007
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterFile
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsCoordinateReferenceSystem
from qgis.core import QgsExpression
import processing


class Syntheseterrain_sdgep_v3(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('couche_des_communes', 'couche des communes', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('couche_des_conduites', 'couche des conduites', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('couche_des_noeuds', 'couche des noeuds', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterFile('slectionnez_un_dossier_de_sortie', 'Sélectionnez un dossier de sortie', behavior=QgsProcessingParameterFile.Folder, fileFilter='Tous les fichiers (*.*)', defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Statsnoeud', 'statsNoeud', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Statsfosse', 'statsFosse', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Statsreseau', 'statsReseau', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(30, model_feedback)
        results = {}
        outputs = {}

        # Extraire par attribut
        alg_params = {
            'FIELD': 'code_insee',
            'INPUT': parameters['couche_des_communes'],
            'OPERATOR': 9,  # n'est pas null
            'VALUE': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParAttribut'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ nom_offici noeud
        alg_params = {
            'FIELD_LENGTH': 30,
            'FIELD_NAME': 'Nom_Commune',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': 'to_string(array_to_string(overlay_within(  @Extraire_par_attribut_OUTPUT  , nom_offici)))',
            'INPUT': parameters['couche_des_noeuds'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampNom_officiNoeud'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Statistiques par catégories noeuds
        alg_params = {
            'CATEGORIES_FIELD_NAME': ['Nom_Commune','date'],
            'INPUT': outputs['CalculatriceDeChampNom_officiNoeud']['OUTPUT'],
            'VALUES_FIELD_NAME': None,
            'OUTPUT': parameters['Statsnoeud']
        }
        outputs['StatistiquesParCatgoriesNoeuds'] = processing.run('qgis:statisticsbycategories', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Statsnoeud'] = outputs['StatistiquesParCatgoriesNoeuds']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ nom_offici conduites
        alg_params = {
            'FIELD_LENGTH': 30,
            'FIELD_NAME': 'Nom_Commune',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': 'to_string(array_to_string(overlay_within(  @Extraire_par_attribut_OUTPUT  , nom_offici)))',
            'INPUT': parameters['couche_des_conduites'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampNom_officiConduites'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Renommer le champ nb_noeud
        alg_params = {
            'FIELD': 'count',
            'INPUT': outputs['StatistiquesParCatgoriesNoeuds']['OUTPUT'],
            'NEW_NAME': 'nb_noeud',
            'OUTPUT': QgsExpression("'StatsNoeud'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenommerLeChampNb_noeud'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ longueur
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Longueur',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Décimal (double)
            'FORMULA': '$length',
            'INPUT': outputs['CalculatriceDeChampNom_officiConduites']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampLongueur'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Extraire par attribut Fossé
        alg_params = {
            'FIELD': 'Type_Res',
            'INPUT': outputs['CalculatriceDeChampLongueur']['OUTPUT'],
            'OPERATOR': 0,  # =
            'VALUE': 'Fossé',
            'FAIL_OUTPUT': QgsProcessing.TEMPORARY_OUTPUT,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParAttributFoss'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Statistiques par catégories Reseau
        alg_params = {
            'CATEGORIES_FIELD_NAME': ['Nom_Commune','date'],
            'INPUT': outputs['ExtraireParAttributFoss']['FAIL_OUTPUT'],
            'VALUES_FIELD_NAME': 'longueur',
            'OUTPUT': parameters['Statsreseau']
        }
        outputs['StatistiquesParCatgoriesReseau'] = processing.run('qgis:statisticsbycategories', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Statsreseau'] = outputs['StatistiquesParCatgoriesReseau']['OUTPUT']

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ cleNoeud
        alg_params = {
            'FIELD_LENGTH': 250,
            'FIELD_NAME': 'cleNoeud',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': '"Nom_Commune"||\'_\'||"date"',
            'INPUT': outputs['RenommerLeChampNb_noeud']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampClenoeud'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Conserver les champs reseau
        alg_params = {
            'FIELDS': ['Nom_Commune','date','sum'],
            'INPUT': outputs['StatistiquesParCatgoriesReseau']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ConserverLesChampsReseau'] = processing.run('native:retainfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Statistiques par catégories fossé
        alg_params = {
            'CATEGORIES_FIELD_NAME': ['Nom_Commune','date'],
            'INPUT': outputs['ExtraireParAttributFoss']['OUTPUT'],
            'VALUES_FIELD_NAME': 'longueur',
            'OUTPUT': parameters['Statsfosse']
        }
        outputs['StatistiquesParCatgoriesFoss'] = processing.run('qgis:statisticsbycategories', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Statsfosse'] = outputs['StatistiquesParCatgoriesFoss']['OUTPUT']

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Renommer le champ lineaire_reseau
        alg_params = {
            'FIELD': 'sum',
            'INPUT': outputs['ConserverLesChampsReseau']['OUTPUT'],
            'NEW_NAME': 'lineaire_reseau',
            'OUTPUT': QgsExpression("'StastReseau'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenommerLeChampLineaire_reseau'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Conserver les champs Fosse
        alg_params = {
            'FIELDS': ['Nom_Commune','date','sum'],
            'INPUT': outputs['StatistiquesParCatgoriesFoss']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ConserverLesChampsFosse'] = processing.run('native:retainfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ cleReseau
        alg_params = {
            'FIELD_LENGTH': 250,
            'FIELD_NAME': 'cleReseau',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': '"Nom_Commune"||\'_\'||"date"',
            'INPUT': outputs['RenommerLeChampLineaire_reseau']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampClereseau'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Joindre les attributs par valeur de champ ReseauNoeud
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'cleReseau',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'cleNoeud',
            'INPUT': outputs['CalculatriceDeChampClereseau']['OUTPUT'],
            'INPUT_2': outputs['CalculatriceDeChampClenoeud']['OUTPUT'],
            'METHOD': 1,  # Prendre uniquement les attributs de la première entité correspondante (un à un)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoindreLesAttributsParValeurDeChampReseaunoeud'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Renommer le champ lineaire_fosse
        alg_params = {
            'FIELD': 'sum',
            'INPUT': outputs['ConserverLesChampsFosse']['OUTPUT'],
            'NEW_NAME': 'lineaire_fosse',
            'OUTPUT': QgsExpression("'StatsFosse'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenommerLeChampLineaire_fosse'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ cleFosse
        alg_params = {
            'FIELD_LENGTH': 250,
            'FIELD_NAME': 'cleFosse',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': '"Nom_Commune"||\'_\'||"date"',
            'INPUT': outputs['RenommerLeChampLineaire_fosse']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampClefosse'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # Joindre les attributs par valeur de champ NoeudFosse
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'cleNoeud',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'cleFosse',
            'INPUT': outputs['CalculatriceDeChampClenoeud']['OUTPUT'],
            'INPUT_2': outputs['CalculatriceDeChampClefosse']['OUTPUT'],
            'METHOD': 1,  # Prendre uniquement les attributs de la première entité correspondante (un à un)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoindreLesAttributsParValeurDeChampNoeudfosse'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # Joindre les attributs par valeur de champ FosseNoeud
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'cleFosse',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'cleNoeud',
            'INPUT': outputs['CalculatriceDeChampClefosse']['OUTPUT'],
            'INPUT_2': outputs['CalculatriceDeChampClenoeud']['OUTPUT'],
            'METHOD': 1,  # Prendre uniquement les attributs de la première entité correspondante (un à un)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoindreLesAttributsParValeurDeChampFossenoeud'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # Joindre les attributs par valeur de champ ReseauNoeudFosse
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'cleReseau',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'cleFosse',
            'INPUT': outputs['JoindreLesAttributsParValeurDeChampReseaunoeud']['OUTPUT'],
            'INPUT_2': outputs['CalculatriceDeChampClefosse']['OUTPUT'],
            'METHOD': 1,  # Prendre uniquement les attributs de la première entité correspondante (un à un)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoindreLesAttributsParValeurDeChampReseaunoeudfosse'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        # Joindre les attributs par valeur de champ FosseNoeudReseau
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'cleFosse',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'cleReseau',
            'INPUT': outputs['JoindreLesAttributsParValeurDeChampFossenoeud']['OUTPUT'],
            'INPUT_2': outputs['CalculatriceDeChampClereseau']['OUTPUT'],
            'METHOD': 1,  # Prendre uniquement les attributs de la première entité correspondante (un à un)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoindreLesAttributsParValeurDeChampFossenoeudreseau'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(21)
        if feedback.isCanceled():
            return {}

        # Joindre les attributs par valeur de champ NoeudFosseReseau
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'cleNoeud',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'cleReseau',
            'INPUT': outputs['JoindreLesAttributsParValeurDeChampNoeudfosse']['OUTPUT'],
            'INPUT_2': outputs['CalculatriceDeChampClereseau']['OUTPUT'],
            'METHOD': 1,  # Prendre uniquement les attributs de la première entité correspondante (un à un)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoindreLesAttributsParValeurDeChampNoeudfossereseau'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(22)
        if feedback.isCanceled():
            return {}

        # Fusionner des couches vecteur
        alg_params = {
            'CRS': QgsCoordinateReferenceSystem('EPSG:2154'),
            'LAYERS': [outputs['JoindreLesAttributsParValeurDeChampNoeudfossereseau']['OUTPUT'],outputs['JoindreLesAttributsParValeurDeChampFossenoeudreseau']['OUTPUT'],outputs['JoindreLesAttributsParValeurDeChampReseaunoeudfosse']['OUTPUT']],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FusionnerDesCouchesVecteur'] = processing.run('native:mergevectorlayers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(23)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ nb_noeud
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'nb_noeud',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Entier (32bit)
            'FORMULA': 'CASE\r\nWHEN "nb_noeud" IS NULL THEN 0\r\nELSE "nb_noeud"\r\nEND',
            'INPUT': outputs['FusionnerDesCouchesVecteur']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampNb_noeud'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(24)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ lin fosse
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'lineaire_fosse',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Décimal (double)
            'FORMULA': 'CASE\r\nWHEN "lineaire_fosse" IS NULL THEN 0\r\nELSE "lineaire_fosse"\r\nEND',
            'INPUT': outputs['CalculatriceDeChampNb_noeud']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampLinFosse'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(25)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ lin reseau
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'lineaire_reseau',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Décimal (double)
            'FORMULA': 'CASE\r\nWHEN "lineaire_reseau" IS NULL THEN 0\r\nELSE "lineaire_reseau"\r\nEND',
            'INPUT': outputs['CalculatriceDeChampLinFosse']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampLinReseau'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(26)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ discriminant
        alg_params = {
            'FIELD_LENGTH': 255,
            'FIELD_NAME': 'discriminant',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': '"nb_noeud"  || "lineaire_fosse"  || "lineaire_reseau"',
            'INPUT': outputs['CalculatriceDeChampLinReseau']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampDiscriminant'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(27)
        if feedback.isCanceled():
            return {}

        # Supprimer les doublons par attribut
        alg_params = {
            'FIELDS': ['discriminant'],
            'INPUT': outputs['CalculatriceDeChampDiscriminant']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SupprimerLesDoublonsParAttribut'] = processing.run('native:removeduplicatesbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(28)
        if feedback.isCanceled():
            return {}

        # Conserver les champs Jointure finale
        alg_params = {
            'FIELDS': ['Nom_Commune','date','nb_noeud','lineaire_fosse','lineaire_reseau'],
            'INPUT': outputs['SupprimerLesDoublonsParAttribut']['OUTPUT'],
            'OUTPUT': QgsExpression("'StatistiquesGenerales'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ConserverLesChampsJointureFinale'] = processing.run('native:retainfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(29)
        if feedback.isCanceled():
            return {}

        # Exporter vers un tableur
        alg_params = {
            'FORMATTED_VALUES': False,
            'LAYERS': [outputs['RenommerLeChampLineaire_reseau']['OUTPUT'],outputs['RenommerLeChampLineaire_fosse']['OUTPUT'],outputs['RenommerLeChampNb_noeud']['OUTPUT'],outputs['ConserverLesChampsJointureFinale']['OUTPUT']],
            'OUTPUT': QgsExpression(" @slectionnez_un_dossier_de_sortie  || '\\\\tableur_statistiques.xlsx'").evaluate(),
            'OVERWRITE': True,
            'USE_ALIAS': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExporterVersUnTableur'] = processing.run('native:exporttospreadsheet', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results

    def name(self):
        return 'SyntheseTerrain_SDGEP_v3'

    def displayName(self):
        return 'SyntheseTerrain_SDGEP_v3'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Syntheseterrain_sdgep_v3()
