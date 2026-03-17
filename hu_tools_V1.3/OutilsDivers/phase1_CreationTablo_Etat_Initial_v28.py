"""
Model exported as python.
Name : phase1_CréationTablo_Etat_Initial_v28
Group : 
With QGIS : 34004
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterString
from qgis.core import QgsProcessingParameterFile
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterEnum
from qgis.core import QgsProcessingParameterDefinition
from qgis.core import QgsCoordinateReferenceSystem
from qgis.core import QgsExpression
from qgis.core import QgsProcessingFeatureSourceDefinition
import processing


class Phase1_creationtablo_etat_initial_v28(QgsProcessingAlgorithm):
    def __init__(self):
        super().__init__()  # Obligatoire pour QGIS

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterString('quelestlenomduprojet', 'Quel est le nom du projet ?', multiLine=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterString('quelestlenomdumatredouvrage', "Quel est le nom du Maître d'ouvrage ?", multiLine=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterFile('veuillezlocaliserlelogoduclient', 'Veuillez localiser le logo du client : ', behavior=QgsProcessingParameterFile.File, fileFilter='Tous les fichiers (*.*)', defaultValue=None))
        self.addParameter(QgsProcessingParameterFile('localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_', 'Localisez le dossier de sortie pour les couches SIG et tableurs :', behavior=QgsProcessingParameterFile.Folder, fileFilter='Tous les fichiers (*.*)', defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('quelle_est_la_valeur_du_tampon_pour_laer_en_km_', "Quelle est la valeur du tampon pour l'AER (en km) ?", type=QgsProcessingParameterNumber.Integer, minValue=0, maxValue=50, defaultValue=5))
        self.addParameter(QgsProcessingParameterNumber('quelle_est_la_valeur_du_tampon_pour_laee_en_km_', "Quelle est la valeur du tampon pour l'AEE (en km) ?", type=QgsProcessingParameterNumber.Integer, minValue=0, maxValue=100, defaultValue=10))
        self.addParameter(QgsProcessingParameterNumber('valeurdutamponderecherchepourlesstationsqualitetdbitenmtres', 'Valeur du tampon de recherche pour les stations Qualité et Débit (en mètres) :', type=QgsProcessingParameterNumber.Integer, minValue=1, maxValue=100000, defaultValue=20000))
        self.addParameter(QgsProcessingParameterVectorLayer('veuillez_slectionner_la_couche_de_la_zone_dtude_', "Veuillez sélectionner la couche de la zone d'étude : ", types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        param = QgsProcessingParameterEnum('utiliser_la_couche_climat_', 'Utiliser la couche Climat ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_la_couche_des_stations_meteo_', 'Utiliser la couche des stations Meteo ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_la_couche_monuments_historiques_', 'Utiliser la couche Monuments Historiques ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_la_couche_prescriptions_archeologiques_', 'Utiliser la couche Prescriptions Archeologiques ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_la_couche_rose_des_vents_iowa_2', 'Utiliser la couche rose des vents IOWA ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_la_couche_sites_classes_inscrits_', 'Utiliser la couche Sites Classes Inscrits ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_la_couche_sites_patrimoniaux_remarquables_', 'Utiliser la couche Sites Patrimoniaux Remarquables ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_alea_inondation_frequent_', 'Utiliser le flux Alea Inondation Frequent ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_alea_inondation_moyen', 'Utiliser le flux Alea Inondation Moyen', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_alea_inondation_rare_', 'Utiliser le flux Alea Inondation Rare ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_ap_habitats_', 'Utiliser le flux AP Habitats ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_appb_', 'Utiliser le flux APPB ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_clc_', 'Utiliser le flux CLC ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_communes_', 'Utiliser le flux communes ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_communes_tampon_', 'Utiliser le flux communes Tampon ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_contexte_piscicole_', 'Utiliser le flux contexte piscicole ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_couches_gologiques_', 'Utiliser le flux couches géologiques ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_des_sage_', 'Utiliser le flux des SAGE ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_des_sdage_', 'Utiliser le flux des SDAGE ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_epci_', 'Utiliser le flux EPCI ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_hydroecoregions_', 'Utiliser le flux Hydroecoregions ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_masses_do_souterraines_', 'Utiliser le flux Masses Do Souterraines ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_masses_do_superficielles_', 'Utiliser le flux Masses Do Superficielles ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_parcs_nationaux_', 'Utiliser le flux Parcs Nationaux ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_pnr_', 'Utiliser le flux PNR ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_ppr_seismes_', 'Utiliser le flux PPR Seismes ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_ppri_', 'Utiliser le flux PPRI ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_pprtechnologique_', 'Utiliser le flux PPRTechnologique ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_pprterrain_', 'Utiliser le flux PPRTerrain ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_ramsar_', 'Utiliser le flux RAMSAR ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_reserve_biologique_', 'Utiliser le flux Reserve Biologique ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_reserve_biosphre_', 'Utiliser le flux Reserve Biosphère ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_rn_nat_', 'Utiliser le flux RN NAT ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_rnr_', 'Utiliser le flux RNR ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_sic_', 'Utiliser le flux SIC ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_stations_dbit_', 'Utiliser le flux Stations débit ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_stations_qualit_', 'Utiliser le flux Stations qualité ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_zico_', 'Utiliser le flux ZICO ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_znieff1_', 'Utiliser le flux ZNIEFF1 ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_znieff2_', 'Utiliser le flux ZNIEFF2 ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_zonages_cartes_communales_', 'Utiliser le flux Zonages Cartes Communales ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_zonages_plu_', 'Utiliser le flux Zonages PLU ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_zones_repartition_des_eaux_', 'Utiliser le flux Zones Repartition des Eaux ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_zones_sensibles_eutrophisation_', 'Utiliser le flux Zones Sensibles Eutrophisation ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_zones_vulnerables_nitrates_', 'Utiliser le flux Zones Vulnerables Nitrates ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_zps_', 'Utiliser le flux ZPS ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        self.addParameter(QgsProcessingParameterEnum('voulezvous_crer_un_geopackage_englobant_toutes_les_couches_sig_extraites__temps_de_traitement_plus_long', '/\\/\\/\\/\\Voulez-vous créer un Geopackage englobant toutes les couches SIG extraites ? (temps de traitement plus long)/\\/\\/\\', options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[1]))
        self.addParameter(QgsProcessingParameterNumber('quelle_est_la_valeur_du_tampon_de_recherche_que_vous_souhaitez_en_km_pour_les_zonages_despaces_naturels__peut_tre_diffrent_des_aee_et_aer', "Quelle est la valeur du tampon de recherche que vous souhaitez (en km) pour les zonages d'espaces naturels ? (peut être différent des AEE et AER)", type=QgsProcessingParameterNumber.Integer, minValue=0, maxValue=100, defaultValue=0))
        param = QgsProcessingParameterEnum('utiliser_la_couche_des_points_bss_', 'Utiliser la couche des points BSS ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_la_couche_ensoleillement_2', 'Utiliser la couche Ensoleillement ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=None)
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_la_couche_potentiel_radon_', 'Utiliser la couche Potentiel radon ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_la_couche_rpg_', 'Utiliser la couche RPG ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_la_couche_sismicit_2', 'Utiliser la couche Sismicité ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_cavits_souterraines_abandonnes_non_minires_', 'Utiliser le flux Cavités souterraines abandonnées (non minières) ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_continuit_cologique_liste_1_', 'Utiliser le flux Continuité écologique Liste 1 ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterEnum('utiliser_le_flux_continuit_cologique_liste_2__', 'Utiliser le flux Continuité écologique Liste 2  ?', optional=True, options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        self.addParameter(QgsProcessingParameterEnum('voulezvous_exporter_les_cartes_standards_automatiquement_en_fin_de_traitement_', 'Voulez-vous exporter les cartes standards automatiquement en fin de traitement ?', options=['Oui','Non'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0]))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(323, model_feedback)
        results = {}
        outputs = {}

        # Sauvegarder les entités vectorielles dans un fichier SCAN25_vide
        alg_params = {
            'ACTION_ON_EXISTING_FILE': 0,  # Créer ou écraser le fichier
            'DATASOURCE_OPTIONS': None,
            'INPUT': QgsExpression("'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\scan25_vide.gpkg'").evaluate(),
            'LAYER_NAME': 'rr',
            'LAYER_OPTIONS': None,
            'OUTPUT': QgsExpression("@localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\scan25_vide.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SauvegarderLesEntitsVectoriellesDansUnFichierScan25_vide'] = processing.run('native:savefeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Statistiques de zone MNT raster
        alg_params = {
            'COLUMN_PREFIX': '_',
            'INPUT': parameters['veuillez_slectionner_la_couche_de_la_zone_dtude_'],
            'INPUT_RASTER': 'R:/SIG/02_Raster/BD_ALTI/France_MNT.tif',
            'RASTER_BAND': 1,
            'STATISTICS': [2,5,6],  # Moyenne,Minimum,Maximum
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['StatistiquesDeZoneMntRaster'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation radon
        alg_params = {
            'INPUT': QgsExpression("if (     @utiliser_la_couche_potentiel_radon_=0,\r\n'R:\\\\SIG\\\\01_Vecteur\\\\Milieu_physique\\\\Radon\\\\irsn_radon_metropole.shp',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\commune_radon_vide.gpkg')").evaluate(),
            'INTERSECT': parameters['veuillez_slectionner_la_couche_de_la_zone_dtude_'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationRadon'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation Zones de répartition des eaux sans verif geom
        alg_params = {
            'INPUT': QgsProcessingFeatureSourceDefinition(" pagingEnabled='true' preferCoordinatesForWfsT11='false' restrictToRequestBBOX='1' srsname='EPSG:4326' typename='sa:ZRE' url='https://services.sandre.eaufrance.fr/geo/sandre' version='auto'", selectedFeaturesOnly=False, featureLimit=-1, flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck, geometryCheck=QgsFeatureRequest.GeometryNoCheck),
            'INTERSECT': parameters['veuillez_slectionner_la_couche_de_la_zone_dtude_'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationZonesDeRpartitionDesEauxSansVerifGeom'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation Aléa inondation moyen sans verif geom
        alg_params = {
            'INPUT': QgsProcessingFeatureSourceDefinition(" pagingEnabled='true' preferCoordinatesForWfsT11='false' restrictToRequestBBOX='1' srsname='EPSG:4326' typename='ms:ISO_HT_01_02MOY_FXX' url='http://georisques.gouv.fr/services' version='auto'", selectedFeaturesOnly=False, featureLimit=-1, flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck, geometryCheck=QgsFeatureRequest.GeometryNoCheck),
            'INTERSECT': parameters['veuillez_slectionner_la_couche_de_la_zone_dtude_'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationAlaInondationMoyenSansVerifGeom'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Reprojeter couche zone etude en 4326
        alg_params = {
            'CONVERT_CURVED_GEOMETRIES': False,
            'INPUT': parameters['veuillez_slectionner_la_couche_de_la_zone_dtude_'],
            'OPERATION': None,
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:4326'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojeterCoucheZoneEtudeEn4326'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation continuité écologique Liste 2
        alg_params = {
            'INPUT': QgsExpression("if (    @utiliser_le_flux_continuit_cologique_liste_2__ =0,\n'WFS:// pagingEnabled=\\'true\\' preferCoordinatesForWfsT11=\\'false\\' restrictToRequestBBOX=\\'1\\' srsname=\\'EPSG:4326\\' typename=\\'sa:SegClassContinuiteEcoListe2_FXX\\' url=\\'https://services.sandre.eaufrance.fr/geo/sandre\\' version=\\'auto\\'',\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\continuiteEcologique_Liste1_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['ReprojeterCoucheZoneEtudeEn4326']['OUTPUT'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationContinuitCologiqueListe2'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation Agence de l'eau dans zone etude
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_des_sdage_  =0,\r\n'WFS:// pagingEnabled=\\'true\\' preferCoordinatesForWfsT11=\\'false\\' restrictToRequestBBOX=\\'1\\' srsname=\\'EPSG:4326\\' typename=\\'sa:BassinHydrographique_FXX_Topage2022\\' url=\\'https://services.sandre.eaufrance.fr/geo/sandre\\' version=\\'auto\\'',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\agenceDeLEau_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['ReprojeterCoucheZoneEtudeEn4326']['OUTPUT'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationAgenceDeLeauDansZoneEtude'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation Zones sensibles sans verif geom
        alg_params = {
            'INPUT': QgsProcessingFeatureSourceDefinition(" pagingEnabled='true' preferCoordinatesForWfsT11='false' restrictToRequestBBOX='1' srsname='EPSG:4326' typename='sa:ZoneSensible_Eutrophe_FXX' url='https://services.sandre.eaufrance.fr/geo/sandre' version='auto'", selectedFeaturesOnly=False, featureLimit=-1, flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck, geometryCheck=QgsFeatureRequest.GeometryNoCheck),
            'INTERSECT': parameters['veuillez_slectionner_la_couche_de_la_zone_dtude_'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationZonesSensiblesSansVerifGeom'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source continuite ecologique Liste 2
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN    @utiliser_le_flux_continuit_cologique_liste_2__  =0 THEN 'https://services.sandre.eaufrance.fr/geo/sandre  - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN  @utiliser_le_flux_continuit_cologique_liste_2__ =1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND",
            'INPUT': outputs['ExtraireParLocalisationContinuitCologiqueListe2']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\continuiteEco_Liste2_intersect.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceContinuiteEcologiqueListe2'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Tampon AEE
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': QgsExpression(' @quelle_est_la_valeur_du_tampon_pour_laee_en_km_ *1000').evaluate(),
            'END_CAP_STYLE': 0,  # Rond
            'INPUT': parameters['veuillez_slectionner_la_couche_de_la_zone_dtude_'],
            'JOIN_STYLE': 0,  # Rond
            'MITER_LIMIT': 2,
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\AEE.gpkg'").evaluate(),
            'SEGMENTS': 5,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['TamponAee'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation contexte piscicole sans verif geom
        alg_params = {
            'INPUT': QgsProcessingFeatureSourceDefinition(" pagingEnabled='true' preferCoordinatesForWfsT11='false' restrictToRequestBBOX='1' srsname='EPSG:4326' typename='sa:ContextePiscicole_FXX' url='https://services.sandre.eaufrance.fr/geo/sandre' version='auto'", selectedFeaturesOnly=False, featureLimit=-1, flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck, geometryCheck=QgsFeatureRequest.GeometryNoCheck),
            'INTERSECT': parameters['veuillez_slectionner_la_couche_de_la_zone_dtude_'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationContextePiscicoleSansVerifGeom'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation communes concernées par PPR Technologique
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_pprtechnologique_=0,\r\n'WFS:// pagingEnabled=\\'true\\' preferCoordinatesForWfsT11=\\'false\\' restrictToRequestBBOX=\\'1\\' srsname=\\'EPSG:4326\\' typename=\\'ms:PPRT_COMMUNE_RISQIND_APPROUV\\' url=\\'http://georisques.gouv.fr/services\\' version=\\'auto\\'',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\communesPPRTechnologique_vide.gpkg')").evaluate(),
            'INTERSECT': parameters['veuillez_slectionner_la_couche_de_la_zone_dtude_'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationCommunesConcernesParPprTechnologique'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle Cartes
        alg_params = {
        }
        outputs['BrancheConditionnelleCartes'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation Aléa inondation rare sans verif geom
        alg_params = {
            'INPUT': QgsProcessingFeatureSourceDefinition(" pagingEnabled='true' preferCoordinatesForWfsT11='false' restrictToRequestBBOX='1' srsname='EPSG:4326' typename='ms:ISO_HT_01_04FAI_FXX' url='http://georisques.gouv.fr/services' version='auto'", selectedFeaturesOnly=False, featureLimit=-1, flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck, geometryCheck=QgsFeatureRequest.GeometryNoCheck),
            'INTERSECT': parameters['veuillez_slectionner_la_couche_de_la_zone_dtude_'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationAlaInondationRareSansVerifGeom'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle geopackage
        alg_params = {
        }
        outputs['BrancheConditionnelleGeopackage'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Réparer les géométries Zones sensibles eutrophisation INI
        alg_params = {
            'INPUT': outputs['ExtraireParLocalisationZonesSensiblesSansVerifGeom']['OUTPUT'],
            'METHOD': 1,  # Structure
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RparerLesGomtriesZonesSensiblesEutrophisationIni'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # Tampon AER
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': QgsExpression(' @quelle_est_la_valeur_du_tampon_pour_laer_en_km_ *1000').evaluate(),
            'END_CAP_STYLE': 0,  # Rond
            'INPUT': parameters['veuillez_slectionner_la_couche_de_la_zone_dtude_'],
            'JOIN_STYLE': 0,  # Rond
            'MITER_LIMIT': 2,
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\AER.gpkg'").evaluate(),
            'SEGMENTS': 5,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['TamponAer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation SAGE dans zone etude
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_des_sage_  =0,\r\n'WFS:// pagingEnabled=\\'true\\' preferCoordinatesForWfsT11=\\'false\\' restrictToRequestBBOX=\\'1\\' srsname=\\'EPSG:4326\\' typename=\\'sa:Sage_FXX\\' url=\\'https://services.sandre.eaufrance.fr/geo/sandre\\' version=\\'auto\\'',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\sage_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['ReprojeterCoucheZoneEtudeEn4326']['OUTPUT'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationSageDansZoneEtude'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation Zones vulnerables sans verif geom
        alg_params = {
            'INPUT': QgsProcessingFeatureSourceDefinition(" pagingEnabled='true' preferCoordinatesForWfsT11='false' restrictToRequestBBOX='1' srsname='EPSG:4326' typename='sa:ZoneVuln' url='https://services.sandre.eaufrance.fr/geo/sandre' version='auto'", selectedFeaturesOnly=False, featureLimit=-1, flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck, geometryCheck=QgsFeatureRequest.GeometryNoCheck),
            'INTERSECT': parameters['veuillez_slectionner_la_couche_de_la_zone_dtude_'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationZonesVulnerablesSansVerifGeom'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        # Réparer les géométries Contexte piscicole
        alg_params = {
            'INPUT': outputs['ExtraireParLocalisationContextePiscicoleSansVerifGeom']['OUTPUT'],
            'METHOD': 1,  # Structure
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RparerLesGomtriesContextePiscicole'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(21)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation sismicité
        alg_params = {
            'INPUT': QgsExpression("if (    @utiliser_la_couche_sismicit_2  =0,\r\n'R:\\\\SIG\\\\01_Vecteur\\\\Milieu_physique\\\\Sismicite\\\\France_zonage_sismique.shp',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\commune_sismicite_vide.gpkg')").evaluate(),
            'INTERSECT': parameters['veuillez_slectionner_la_couche_de_la_zone_dtude_'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationSismicit'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(22)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation HydroEcoRegions sans verif geom
        alg_params = {
            'INPUT': "WFS:// pagingEnabled='true' preferCoordinatesForWfsT11='false' restrictToRequestBBOX='1' srsname='EPSG:4326' typename='sa:Hydroecoregion2_FXX' url='https://services.sandre.eaufrance.fr/geo/sandre' version='auto'",
            'INTERSECT': parameters['veuillez_slectionner_la_couche_de_la_zone_dtude_'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationHydroecoregionsSansVerifGeom'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(23)
        if feedback.isCanceled():
            return {}

        # Renommer le champ _mean en Alt_moy
        alg_params = {
            'FIELD': '_mean',
            'INPUT': outputs['StatistiquesDeZoneMntRaster']['OUTPUT'],
            'NEW_NAME': 'Alt_moy',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenommerLeChamp_meanEnAlt_moy'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(24)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation Masse d'eau souterraine sans verif geom
        alg_params = {
            'INPUT': QgsProcessingFeatureSourceDefinition(" pagingEnabled='true' preferCoordinatesForWfsT11='false' restrictToRequestBBOX='1' srsname='EPSG:4326' typename='sa:PolygMasseDEauSouterraine_VEDL2019' url='https://services.sandre.eaufrance.fr/geo/sandre' version='auto'", selectedFeaturesOnly=False, featureLimit=-1, flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck, geometryCheck=QgsFeatureRequest.GeometryNoCheck),
            'INTERSECT': parameters['veuillez_slectionner_la_couche_de_la_zone_dtude_'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationMasseDeauSouterraineSansVerifGeom'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(25)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation Zones sensibles eutrophisation
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_zones_sensibles_eutrophisation_=0, @Réparer_les_géométries_Zones_sensibles_eutrophisation_INI_OUTPUT \r\n,\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\zonesSensibles_vide.gpkg')").evaluate(),
            'INTERSECT': parameters['veuillez_slectionner_la_couche_de_la_zone_dtude_'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationZonesSensiblesEutrophisation'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(26)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source radon
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN      @utiliser_la_couche_potentiel_radon_=0 THEN ' https://www.data.gouv.fr/datasets/connaitre-le-potentiel-radon-de-ma-commune/ - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN  @utiliser_la_couche_potentiel_radon_=1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND\r\n\r\n",
            'INPUT': outputs['ExtraireParLocalisationRadon']['OUTPUT'],
            'OUTPUT': QgsExpression("@localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\Commune_radon.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceRadon'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(27)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation climat
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_la_couche_climat_  =0,\r\n'R:\\\\SIG\\\\01_Vecteur\\\\Milieu_physique\\\\Climats\\\\communes_climats.shp',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\climat_vide.gpkg')").evaluate(),
            'INTERSECT': parameters['veuillez_slectionner_la_couche_de_la_zone_dtude_'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationClimat'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(28)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source PPR Technologique
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_pprtechnologique_ =0 THEN 'http://georisques.gouv.fr/services  - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_pprtechnologique_ =1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND\r\n\r\n",
            'INPUT': outputs['ExtraireParLocalisationCommunesConcernesParPprTechnologique']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\Communes_PPRTechnologique.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourcePprTechnologique'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(29)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation Ensoleillement
        alg_params = {
            'INPUT': QgsExpression("if (   @utiliser_la_couche_ensoleillement_2 =0,\r\n'R:\\\\SIG\\\\01_Vecteur\\\\Milieu_physique\\\\Ensoleillement\\\\Ensoleillement_France_Metropole.gpkg',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\ensoleillement_vide.gpkg')").evaluate(),
            'INTERSECT': parameters['veuillez_slectionner_la_couche_de_la_zone_dtude_'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationEnsoleillement'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(30)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation Aléa inondation frequent sans verif geom
        alg_params = {
            'INPUT': "WFS:// pagingEnabled='true' preferCoordinatesForWfsT11='false' restrictToRequestBBOX='1' srsname='EPSG:4326' typename='ms:ISO_HT_01_01FOR_FXX' url='http://georisques.gouv.fr/services' version='auto'",
            'INTERSECT': parameters['veuillez_slectionner_la_couche_de_la_zone_dtude_'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationAlaInondationFrequentSansVerifGeom'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(31)
        if feedback.isCanceled():
            return {}

        # Reprojeter couche zone etude en 2154
        alg_params = {
            'CONVERT_CURVED_GEOMETRIES': False,
            'INPUT': parameters['veuillez_slectionner_la_couche_de_la_zone_dtude_'],
            'OPERATION': None,
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:2154'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojeterCoucheZoneEtudeEn2154'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(32)
        if feedback.isCanceled():
            return {}

        # Tampon 100m Zonages cartes Communales
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 100,
            'END_CAP_STYLE': 0,  # Rond
            'INPUT': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'JOIN_STYLE': 0,  # Rond
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Tampon100mZonagesCartesCommunales'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(33)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source Agence de l'eau
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_des_sdage_ =0 THEN 'https://services.sandre.eaufrance.fr/geo/sandre - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_des_sdage_ =1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND\r\n\r\n",
            'INPUT': outputs['ExtraireParLocalisationAgenceDeLeauDansZoneEtude']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\AgenceDeLEau_intersect.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceAgenceDeLeau'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(34)
        if feedback.isCanceled():
            return {}

        # Reprojeter une couche climat en 2154
        alg_params = {
            'CONVERT_CURVED_GEOMETRIES': False,
            'INPUT': outputs['ExtraireParLocalisationClimat']['OUTPUT'],
            'OPERATION': None,
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:2154'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojeterUneCoucheClimatEn2154'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(35)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ x Zone etude 4326
        alg_params = {
            'FIELD_LENGTH': 20,
            'FIELD_NAME': 'X',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,  # Décimal (double)
            'FORMULA': 'x(@geometry)',
            'INPUT': outputs['ReprojeterCoucheZoneEtudeEn4326']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampXZoneEtude4326'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(36)
        if feedback.isCanceled():
            return {}

        # Réparer les géométries Masse d'eau souterraine
        alg_params = {
            'INPUT': outputs['ExtraireParLocalisationMasseDeauSouterraineSansVerifGeom']['OUTPUT'],
            'METHOD': 1,  # Structure
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RparerLesGomtriesMasseDeauSouterraine'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(37)
        if feedback.isCanceled():
            return {}

        # Réparer les géométries Aléa inondation moyen
        alg_params = {
            'INPUT': outputs['ExtraireParLocalisationAlaInondationMoyenSansVerifGeom']['OUTPUT'],
            'METHOD': 1,  # Structure
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RparerLesGomtriesAlaInondationMoyen'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(38)
        if feedback.isCanceled():
            return {}

        # Réparer les géométries Zones des répartition des eaux INI
        alg_params = {
            'INPUT': outputs['ExtraireParLocalisationZonesDeRpartitionDesEauxSansVerifGeom']['OUTPUT'],
            'METHOD': 1,  # Structure
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RparerLesGomtriesZonesDesRpartitionDesEauxIni'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(39)
        if feedback.isCanceled():
            return {}

        # Réparer les géométries Aléa inondation rare
        alg_params = {
            'INPUT': outputs['ExtraireParLocalisationAlaInondationRareSansVerifGeom']['OUTPUT'],
            'METHOD': 1,  # Structure
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RparerLesGomtriesAlaInondationRare'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(40)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation communes concernees par PPRTerrain
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_pprterrain_=0,\r\n'WFS:// pagingEnabled=\\'true\\' preferCoordinatesForWfsT11=\\'false\\' restrictToRequestBBOX=\\'1\\' srsname=\\'EPSG:4326\\' typename=\\'ms:PPRN_COMMUNE_MVT_APPROUV\\' url=\\'http://georisques.gouv.fr/services\\' version=\\'auto\\'',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\communesPPRTerrain_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['ReprojeterCoucheZoneEtudeEn4326']['OUTPUT'],
            'PREDICATE': [0,4],  # intersecte,touche
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationCommunesConcerneesParPprterrain'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(41)
        if feedback.isCanceled():
            return {}

        # Créer un répertoire Images
        alg_params = {
            'PATH': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\Images'").evaluate()
        }
        outputs['CrerUnRpertoireImages'] = processing.run('native:createdirectory', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(42)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation continuité écologique Liste 1
        alg_params = {
            'INPUT': QgsExpression("if (   @utiliser_le_flux_continuit_cologique_liste_1_  =0,\n'WFS:// pagingEnabled=\\'true\\' preferCoordinatesForWfsT11=\\'false\\' restrictToRequestBBOX=\\'1\\' srsname=\\'EPSG:4326\\' typename=\\'sa:SegClassContinuiteEcoListe1_FXX\\' url=\\'https://services.sandre.eaufrance.fr/geo/sandre\\' version=\\'auto\\'',\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\continuiteEcologique_Liste1_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['ReprojeterCoucheZoneEtudeEn4326']['OUTPUT'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationContinuitCologiqueListe1'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(43)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation communes concernees par PPRSeismes
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_ppr_seismes_=0,\r\n'WFS:// pagingEnabled=\\'true\\' preferCoordinatesForWfsT11=\\'false\\' restrictToRequestBBOX=\\'1\\' srsname=\\'EPSG:4326\\' typename=\\'ms:PPRN_COMMUNE_SEISME_APPROUV\\' url=\\'http://georisques.gouv.fr/services\\' version=\\'auto\\'',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\communesPPRSeismes_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['ReprojeterCoucheZoneEtudeEn4326']['OUTPUT'],
            'PREDICATE': [0,4],  # intersecte,touche
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationCommunesConcerneesParPprseismes'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(44)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation Aléa inondations moyen
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_alea_inondation_moyen=0,\r\n @Réparer_les_géométries_Aléa_inondation_moyen_OUTPUT ,\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\aleaInondationMoyen_vide.gpkg')").evaluate(),
            'INTERSECT': parameters['veuillez_slectionner_la_couche_de_la_zone_dtude_'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationAlaInondationsMoyen'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(45)
        if feedback.isCanceled():
            return {}

        # Tampon commune
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': parameters['valeurdutamponderecherchepourlesstationsqualitetdbitenmtres'],
            'END_CAP_STYLE': 0,  # Rond
            'INPUT': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'JOIN_STYLE': 0,  # Rond
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['TamponCommune'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(46)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation communes concernees par PPRI
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_ppri_=0,\r\n'WFS:// pagingEnabled=\\'true\\' preferCoordinatesForWfsT11=\\'false\\' restrictToRequestBBOX=\\'1\\' srsname=\\'EPSG:4326\\' typename=\\'ms:PPRN_COMMUNE_RISQINOND_APPROUV\\' url=\\'http://georisques.gouv.fr/services\\' version=\\'auto\\'',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\communesPPRI_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['ReprojeterCoucheZoneEtudeEn4326']['OUTPUT'],
            'PREDICATE': [0,4],  # intersecte,touche
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationCommunesConcerneesParPpri'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(47)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ Y zone etude 4326
        alg_params = {
            'FIELD_LENGTH': 20,
            'FIELD_NAME': 'Y',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,  # Décimal (double)
            'FORMULA': 'y(@geometry)',
            'INPUT': outputs['CalculatriceDeChampXZoneEtude4326']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampYZoneEtude4326'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(48)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation masse d'eau dans zone etude
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_masses_do_superficielles_  =0,\r\n'WFS:// pagingEnabled=\\'true\\' preferCoordinatesForWfsT11=\\'false\\' restrictToRequestBBOX=\\'1\\' srsname=\\'EPSG:4326\\' typename=\\'sa:MasseDEauRiviere_VEDL2019_FXX\\' url=\\'https://services.sandre.eaufrance.fr/geo/sandre\\' version=\\'auto\\'',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\masseDo_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationMasseDeauDansZoneEtude'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(49)
        if feedback.isCanceled():
            return {}

        # Réparer les géométries  HydroEcoRegions INI
        alg_params = {
            'INPUT': outputs['ExtraireParLocalisationHydroecoregionsSansVerifGeom']['OUTPUT'],
            'METHOD': 1,  # Structure
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RparerLesGomtriesHydroecoregionsIni'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(50)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation masse d'eau souterraine dans zone etude
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_masses_do_souterraines_  =0,\r\n @Réparer_les_géométries_Masse_d_eau_souterraine_OUTPUT ,\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\masseDoSoutNiv1_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['ReprojeterCoucheZoneEtudeEn4326']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\masseDoSout_intersect.gpkg'").evaluate(),
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationMasseDeauSouterraineDansZoneEtude'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(51)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation Aléa inondations rare
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_alea_inondation_rare_=0,\r\n  @Réparer_les_géométries_Aléa_inondation_rare_OUTPUT  ,\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\aleaInondationRare_vide.gpkg')").evaluate(),
            'INTERSECT': parameters['veuillez_slectionner_la_couche_de_la_zone_dtude_'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationAlaInondationsRare'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(52)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source MasseDOsuperficielle
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_masses_do_superficielles_ =0 THEN 'https://services.sandre.eaufrance.fr/geo/sandre - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_masses_do_superficielles_ =1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND\r\n\r\n",
            'INPUT': outputs['ExtraireParLocalisationMasseDeauDansZoneEtude']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\masseDo_intersect.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceMassedosuperficielle'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(53)
        if feedback.isCanceled():
            return {}

        # Couper Zones Sensibles eutrophisation
        alg_params = {
            'INPUT': outputs['ExtraireParLocalisationZonesSensiblesEutrophisation']['OUTPUT'],
            'OVERLAY': parameters['veuillez_slectionner_la_couche_de_la_zone_dtude_'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CouperZonesSensiblesEutrophisation'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(54)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source continuite ecologique Liste 1
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN    @utiliser_le_flux_continuit_cologique_liste_1_ =0 THEN 'https://services.sandre.eaufrance.fr/geo/sandre  - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_continuit_cologique_liste_1_ =1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND",
            'INPUT': outputs['ExtraireParLocalisationContinuitCologiqueListe1']['OUTPUT'],
            'OUTPUT': QgsExpression("@localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\continuiteEco_Liste1_intersect.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceContinuiteEcologiqueListe1'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(55)
        if feedback.isCanceled():
            return {}

        # Conserver les champs climat
        alg_params = {
            'FIELDS': ['code_insee','nom_offici','climat'],
            'INPUT': outputs['ReprojeterUneCoucheClimatEn2154']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ConserverLesChampsClimat'] = processing.run('native:retainfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(56)
        if feedback.isCanceled():
            return {}

        # Ajouter un champ SDAGE
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'sdage',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'INPUT': outputs['ExtraireParLocalisationSageDansZoneEtude']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AjouterUnChampSdage'] = processing.run('native:addfieldtoattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(57)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation contexte pisciole dans zone etude
        alg_params = {
            'INPUT': QgsExpression("if (  @utiliser_le_flux_contexte_piscicole_ =0,\r\n  @Réparer_les_géométries_Contexte_piscicole_OUTPUT ,\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\contextePiscicole_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'OUTPUT': QgsExpression("@localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\contextePiscicole_intersect.gpkg'").evaluate(),
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationContextePiscioleDansZoneEtude'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(58)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source Aléa inondations rare
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_alea_inondation_rare_ =0 THEN 'http://georisques.gouv.fr/services - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_alea_inondation_rare_=1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND\r\n",
            'INPUT': outputs['ExtraireParLocalisationAlaInondationsRare']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\AleaInondationRare_intersect.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceAlaInondationsRare'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(59)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation Zone de réparition des eaux
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_zones_repartition_des_eaux_=0,\r\n  @Réparer_les_géométries_Zones_des_répartition_des_eaux_INI_OUTPUT  ,\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\zre_vide.gpkg')").evaluate(),
            'INTERSECT': parameters['veuillez_slectionner_la_couche_de_la_zone_dtude_'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationZoneDeRparitionDesEaux'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(60)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation CLC dans Zone etude
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_clc_=0,\r\n'WFS:// pagingEnabled=\\'true\\' preferCoordinatesForWfsT11=\\'false\\' restrictToRequestBBOX=\\'1\\' srsname=\\'EPSG:2154\\' typename=\\'LANDCOVER.CLC18_FR:clc18_fr\\' url=\\'https://data.geopf.fr/wfs/ows\\' url=\\'https://data.geopf.fr/wfs/ows?VERSION=2.0.0\\' version=\\'auto\\'',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\clc_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationClcDansZoneEtude'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(61)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source Ensoleillement
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN    @utiliser_la_couche_ensoleillement_2=0 THEN 'https://www.data.gouv.fr/datasets/donnees-du-temps-densoleillement-par-departements-en-france - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN  @utiliser_la_couche_ensoleillement_2=1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND\r\n\r\n",
            'INPUT': outputs['ExtraireParLocalisationEnsoleillement']['OUTPUT'],
            'OUTPUT': QgsExpression("@localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\Ensoleillement.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceEnsoleillement'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(62)
        if feedback.isCanceled():
            return {}

        # Réparer les géométries Aléa inondation frequent
        alg_params = {
            'INPUT': outputs['ExtraireParLocalisationAlaInondationFrequentSansVerifGeom']['OUTPUT'],
            'METHOD': 1,  # Structure
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RparerLesGomtriesAlaInondationFrequent'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(63)
        if feedback.isCanceled():
            return {}

        # Reprojeter Tampon en 4326
        alg_params = {
            'CONVERT_CURVED_GEOMETRIES': False,
            'INPUT': outputs['TamponCommune']['OUTPUT'],
            'OPERATION': None,
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\tampon4326.shp'").evaluate(),
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:4326'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojeterTamponEn4326'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(64)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source Aléa inondations moyen
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_alea_inondation_moyen =0 THEN 'http://georisques.gouv.fr/services - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_alea_inondation_moyen=1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND\r\n",
            'INPUT': outputs['ExtraireParLocalisationAlaInondationsMoyen']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\AleaInondationMoyen_intersect.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceAlaInondationsMoyen'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(65)
        if feedback.isCanceled():
            return {}

        # Géométrie d'emprise minimale ZoneEtude
        alg_params = {
            'FIELD': None,
            'INPUT': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'TYPE': 3,  # Enveloppe convexe
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['GomtrieDempriseMinimaleZoneetude'] = processing.run('qgis:minimumboundinggeometry', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(66)
        if feedback.isCanceled():
            return {}

        # Réparer les géométries Zones vulnérables INI
        alg_params = {
            'INPUT': outputs['ExtraireParLocalisationZonesVulnerablesSansVerifGeom']['OUTPUT'],
            'METHOD': 1,  # Structure
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RparerLesGomtriesZonesVulnrablesIni'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(67)
        if feedback.isCanceled():
            return {}

        # Tampon 100m zonages PLU
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 100,
            'END_CAP_STYLE': 0,  # Rond
            'INPUT': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'JOIN_STYLE': 0,  # Rond
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Tampon100mZonagesPlu'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(68)
        if feedback.isCanceled():
            return {}

        # Renommer le champ _min en Alt_min
        alg_params = {
            'FIELD': '_min',
            'INPUT': outputs['RenommerLeChamp_meanEnAlt_moy']['OUTPUT'],
            'NEW_NAME': 'Alt_min',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenommerLeChamp_minEnAlt_min'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(69)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ surface climat
        alg_params = {
            'FIELD_LENGTH': 25,
            'FIELD_NAME': 'surface',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Décimal (double)
            'FORMULA': '$area',
            'INPUT': outputs['ConserverLesChampsClimat']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSurfaceClimat'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(70)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source PPRTerrain
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_pprterrain_ =0 THEN 'http://georisques.gouv.fr/services  - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_pprterrain_ =1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND\r\n\r\n",
            'INPUT': outputs['ExtraireParLocalisationCommunesConcerneesParPprterrain']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\Communes_PPRTerrain.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourcePprterrain'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(71)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source PPRI
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_ppri_ =0 THEN 'http://georisques.gouv.fr/services  - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_ppri_ =1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND\r\n\r\n",
            'INPUT': outputs['ExtraireParLocalisationCommunesConcerneesParPpri']['OUTPUT'],
            'OUTPUT': QgsExpression("@localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\Communes_PPRI.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourcePpri'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(72)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source sismicité
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN     @utiliser_la_couche_sismicit_=0 THEN 'https://www.data.gouv.fr/datasets/zonage-sismique-de-la-france-1/ - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN  @utiliser_la_couche_sismicit_=1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND\r\n\r\n",
            'INPUT': outputs['ExtraireParLocalisationSismicit']['OUTPUT'],
            'OUTPUT': QgsExpression("@localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\Commune_sismicite.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceSismicit'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(73)
        if feedback.isCanceled():
            return {}

        # Ajouter un champ surface_ha à la couche zone etude
        alg_params = {
            'FIELD_ALIAS': None,
            'FIELD_COMMENT': None,
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'surface_ha',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,  # Décimal (double)
            'INPUT': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AjouterUnChampSurface_haLaCoucheZoneEtude'] = processing.run('native:addfieldtoattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(74)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ cheminLogo_ZoneEtude emprise
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'cheminLogo',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': ' @veuillezlocaliserlelogoduclient ',
            'INPUT': outputs['GomtrieDempriseMinimaleZoneetude']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampCheminlogo_zoneetudeEmprise'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(75)
        if feedback.isCanceled():
            return {}

        # Extraire dans un rayon 50 km roses des vents IOWA
        alg_params = {
            'DISTANCE': 50000,
            'INPUT': QgsExpression("if (  @utiliser_la_couche_rose_des_vents_iowa_2 =0,\r\n'R:\\\\SIG\\\\01_Vecteur\\\\Milieu_humain\\\\Rose_des_Vents\\\\stationsIOWAroseDesVents2.geojson',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\stationsIOWAroseDesVents2_vide.gpkg')").evaluate(),
            'REFERENCE': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireDansUnRayon50KmRosesDesVentsIowa'] = processing.run('native:extractwithindistance', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(76)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation Zonages Cartes Communales sans verif geom
        alg_params = {
            'INPUT': QgsProcessingFeatureSourceDefinition(" pagingEnabled='true' preferCoordinatesForWfsT11='false' restrictToRequestBBOX='1' srsname='EPSG:4326' typename='wfs_du:secteur_cc' url='https://data.geopf.fr/wfs/ows' url='https://data.geopf.fr/wfs/ows?VERSION=2.0.0' version='auto'", selectedFeaturesOnly=False, featureLimit=-1, flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck, geometryCheck=QgsFeatureRequest.GeometryNoCheck),
            'INTERSECT': outputs['Tampon100mZonagesCartesCommunales']['OUTPUT'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationZonagesCartesCommunalesSansVerifGeom'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(77)
        if feedback.isCanceled():
            return {}

        # Tampon espaces naturels
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': QgsExpression(' @quelle_est_la_valeur_du_tampon_de_recherche_que_vous_souhaitez_en_km_pour_les_zonages_despaces_naturels__peut_tre_diffrent_des_aee_et_aer *1000').evaluate(),
            'END_CAP_STYLE': 0,  # Rond
            'INPUT': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'JOIN_STYLE': 0,  # Rond
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['TamponEspacesNaturels'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(78)
        if feedback.isCanceled():
            return {}

        # Calculatrice champ sdage
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'sdage',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': 'CASE \r\n\r\nWHEN "cdComiteBassin"= \'FR000001\' THEN \'Artois Picardie\'\r\nWHEN "cdComiteBassin"= \'FR000002\' THEN \'Rhin Meuse\'\r\nWHEN "cdComiteBassin"= \'FR000003\' THEN \'Seine Normandie\'\r\nWHEN "cdComiteBassin"= \'FR000004\' THEN \'Loire Bretagne\'\r\nWHEN "cdComiteBassin"= \'FR000005\' THEN \'Adour Garonne\'\r\nWHEN "cdComiteBassin"= \'FR000005\' THEN \'Rhône Méditérannée Corse\'\r\nEND',
            'INPUT': outputs['AjouterUnChampSdage']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceChampSdage'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(79)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation SIC dans zone etude
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_sic_ =0,\r\n'WFS:// pagingEnabled=\\'true\\' preferCoordinatesForWfsT11=\\'false\\' restrictToRequestBBOX=\\'1\\' srsname=\\'EPSG:2154\\' typename=\\'ms:Sites_d_importance_communautaire_JOUE__ZSC_SIC_\\' url=\\'https://ws.carmencarto.fr/WFS/119/fxx_inpn\\' version=\\'auto\\'',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\sic_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['TamponEspacesNaturels']['OUTPUT'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationSicDansZoneEtude'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(80)
        if feedback.isCanceled():
            return {}

        # Couper par zone RPG
        alg_params = {
            'INPUT': QgsExpression("if (    @utiliser_la_couche_rpg_ =0,\r\n'R:\\\\SIG\\\\01_Vecteur\\\\Occupation_des_sols\\\\RPG\\\\RPG_2024\\\\PARCELLES_GRAPHIQUES_rpg2024_repare.gpkg',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\PARCELLES_GRAPHIQUES_rpg_vide.gpkg')").evaluate(),
            'OVERLAY': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CouperParZoneRpg'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(81)
        if feedback.isCanceled():
            return {}

        # Couper Zones de Répartition des Eaux
        alg_params = {
            'INPUT': outputs['ExtraireParLocalisationZoneDeRparitionDesEaux']['OUTPUT'],
            'OVERLAY': parameters['veuillez_slectionner_la_couche_de_la_zone_dtude_'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CouperZonesDeRpartitionDesEaux'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(82)
        if feedback.isCanceled():
            return {}

        # Tampon zone etude 40km 
        alg_params = {
            'DISSOLVE': True,
            'DISTANCE': 40000,
            'END_CAP_STYLE': 0,  # Rond
            'INPUT': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'JOIN_STYLE': 0,  # Rond
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['TamponZoneEtude40km'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(83)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation stations qualité dans Tampon
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_stations_qualit_=0,\r\n'WFS:// pagingEnabled=\\'true\\' preferCoordinatesForWfsT11=\\'false\\' restrictToRequestBBOX=\\'1\\' srsname=\\'EPSG:4326\\' typename=\\'sa:StationMesureEauxSurface\\' url=\\'https://services.sandre.eaufrance.fr/geo/sandre\\' version=\\'auto\\'',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\stationsQualite_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['ReprojeterTamponEn4326']['OUTPUT'],
            'PREDICATE': [6,0],  # est à l'intérieur,intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationStationsQualitDansTampon'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(84)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation stations débit dans Tampon
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_stations_dbit_=0,\r\n'WFS:// pagingEnabled=\\'true\\' preferCoordinatesForWfsT11=\\'false\\' restrictToRequestBBOX=\\'1\\' srsname=\\'EPSG:4326\\' typename=\\'sa:StationHydro_FXX\\' url=\\'https://services.sandre.eaufrance.fr/geo/hyd\\' version=\\'auto\\'',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\stationsDebit_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['ReprojeterTamponEn4326']['OUTPUT'],
            'PREDICATE': [6,0],  # est à l'intérieur,intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationStationsDbitDansTampon'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(85)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation RN dans zoneEtude
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_rn_nat_=0,\r\n'WFS:// pagingEnabled=\\'true\\' preferCoordinatesForWfsT11=\\'false\\' restrictToRequestBBOX=\\'1\\' srsname=\\'EPSG:2154\\' typename=\\'ms:Reserves_Naturelles_Nationales\\' url=\\'https://ws.carmencarto.fr/WFS/119/fxx_inpn\\' version=\\'auto\\'',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\reservesNationales_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['TamponEspacesNaturels']['OUTPUT'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationRnDansZoneetude'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(86)
        if feedback.isCanceled():
            return {}

        # Extraire dans un rayon 50km stationsMeteo
        alg_params = {
            'DISTANCE': 50000,
            'INPUT': QgsExpression("if ( @utiliser_la_couche_des_stations_meteo_=0,\r\n'R:\\\\SIG\\\\01_Vecteur\\\\Milieu_humain\\\\Stations_Meteorologiques\\\\stationsMeteoFranceMetropolitaine.geojson',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\stationsMeteo_vide.gpkg')").evaluate(),
            'REFERENCE': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireDansUnRayon50kmStationsmeteo'] = processing.run('native:extractwithindistance', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(87)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ SURF_PARC RPG
        alg_params = {
            'FIELD_LENGTH': 20,
            'FIELD_NAME': 'SURF_PARC',
            'FIELD_PRECISION': 7,
            'FIELD_TYPE': 0,  # Décimal (double)
            'FORMULA': ' $area /10000',
            'INPUT': outputs['CouperParZoneRpg']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSurf_parcRpg'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(88)
        if feedback.isCanceled():
            return {}

        # Extraire dans un rayon 1km BSS
        alg_params = {
            'DISTANCE': 1000,
            'INPUT': QgsExpression("if (   @utiliser_la_couche_des_points_bss_ =0,\r\n'R:\\\\SIG\\\\01_Vecteur\\\\Eau\\\\Ouvrages_BSS\\\\pointsBSS_FranceMetropolitaine_exportLatest.gpkg',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\pointsBSS_FranceMetropolitaine_vide.gpkg')").evaluate(),
            'REFERENCE': outputs['GomtrieDempriseMinimaleZoneetude']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireDansUnRayon1kmBss'] = processing.run('native:extractwithindistance', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(89)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation APHabitatsNaturels dans zoneEtude
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_ap_habitats_ =0,\r\n'WFS:// pagingEnabled=\\'true\\' preferCoordinatesForWfsT11=\\'false\\' restrictToRequestBBOX=\\'1\\' srsname=\\'EPSG:2154\\' typename=\\'ms:Arretes_de_protection_d_habitats_naturels\\' url=\\'https://ws.carmencarto.fr/WFS/119/fxx_inpn\\' version=\\'auto\\'',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\APHabitatsNaturels_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['TamponEspacesNaturels']['OUTPUT'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationAphabitatsnaturelsDansZoneetude'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(90)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ idUnique Zone etude 4326
        alg_params = {
            'FIELD_LENGTH': 1,
            'FIELD_NAME': 'idUnique',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Entier (32bit)
            'FORMULA': '1',
            'INPUT': outputs['CalculatriceDeChampYZoneEtude4326']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampIduniqueZoneEtude4326'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(91)
        if feedback.isCanceled():
            return {}

        # Réparer les géométries RN
        alg_params = {
            'INPUT': outputs['ExtraireParLocalisationRnDansZoneetude']['OUTPUT'],
            'METHOD': 1,  # Structure
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RparerLesGomtriesRn'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(92)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation HydroEcoRegions
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_hydroecoregions_=0,\r\n  @Réparer_les_géométries__HydroEcoRegions_INI_OUTPUT  ,\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\hydroecoregions_vide.gpkg')").evaluate(),
            'INTERSECT': parameters['veuillez_slectionner_la_couche_de_la_zone_dtude_'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationHydroecoregions'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(93)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ cheminLogo_SAGE
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'cheminLogo',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': ' @veuillezlocaliserlelogoduclient ',
            'INPUT': outputs['CalculatriceChampSdage']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampCheminlogo_sage'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(94)
        if feedback.isCanceled():
            return {}

        # Extraire par attribut Horizon =1
        alg_params = {
            'FIELD': 'horizon',
            'INPUT': outputs['ExtraireParLocalisationMasseDeauSouterraineDansZoneEtude']['OUTPUT'],
            'OPERATOR': 0,  # =
            'VALUE': '1',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParAttributHorizon1'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(95)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source PPR Seismes
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_ppr_seismes_ =0 THEN 'http://georisques.gouv.fr/services  - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_ppr_seismes_ =1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND\r\n\r\n",
            'INPUT': outputs['ExtraireParLocalisationCommunesConcerneesParPprseismes']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\Communes_PPRSeismes.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourcePprSeismes'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(96)
        if feedback.isCanceled():
            return {}

        # Extraire dans un rayon 500m RPG
        alg_params = {
            'DISTANCE': 500,
            'INPUT': QgsExpression("if (    @utiliser_la_couche_rpg_ =0,\r\n'R:\\\\SIG\\\\01_Vecteur\\\\Occupation_des_sols\\\\RPG\\\\RPG_2024\\\\PARCELLES_GRAPHIQUES_rpg2024_repare.gpkg',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\PARCELLES_GRAPHIQUES_rpg_vide.gpkg')").evaluate(),
            'REFERENCE': outputs['GomtrieDempriseMinimaleZoneetude']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireDansUnRayon500mRpg'] = processing.run('native:extractwithindistance', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(97)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation Ramsar dans zoneEtude
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_ramsar_ =0,\r\n'WFS:// pagingEnabled=\\'true\\' preferCoordinatesForWfsT11=\\'false\\' restrictToRequestBBOX=\\'1\\' srsname=\\'EPSG:2154\\' typename=\\'ms:Sites_Ramsar\\' url=\\'https://ws.carmencarto.fr/WFS/119/fxx_inpn\\' version=\\'auto\\'',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\ramsar_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['TamponEspacesNaturels']['OUTPUT'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationRamsarDansZoneetude'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(98)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source RPG
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN    @utiliser_la_couche_rpg_  =0 THEN 'https://geoservices.ign.fr/rpg  - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_la_couche_rpg_ =1 THEN '[refus de l\\'utilisateur]'\r\nEND\r\n\r\n\r\n",
            'INPUT': outputs['ExtraireDansUnRayon500mRpg']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\RPG_intersect.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceRpg'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(99)
        if feedback.isCanceled():
            return {}

        # Ligne la plus courte entre les entités RN
        alg_params = {
            'DESTINATION': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'DISTANCE': None,
            'METHOD': 0,  # Distance to Nearest Point on feature
            'NEIGHBORS': 1,
            'SOURCE': outputs['RparerLesGomtriesRn']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['LigneLaPlusCourteEntreLesEntitsRn'] = processing.run('native:shortestline', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(100)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation Zonages PLU sans verif geom
        alg_params = {
            'INPUT': QgsProcessingFeatureSourceDefinition(" pagingEnabled='true' preferCoordinatesForWfsT11='false' restrictToRequestBBOX='1' srsname='EPSG:4326' typename='wfs_du:zone_urba' url='https://data.geopf.fr/wfs/ows' url='https://data.geopf.fr/wfs/ows?VERSION=2.0.0' version='auto'", selectedFeaturesOnly=False, featureLimit=-1, flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck, geometryCheck=QgsFeatureRequest.GeometryNoCheck),
            'INTERSECT': outputs['Tampon100mZonagesPlu']['OUTPUT'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationZonagesPluSansVerifGeom'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(101)
        if feedback.isCanceled():
            return {}

        # Couper Contexte Piscicole  par zone etude
        alg_params = {
            'INPUT': outputs['ExtraireParLocalisationContextePiscioleDansZoneEtude']['OUTPUT'],
            'OVERLAY': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CouperContextePiscicoleParZoneEtude'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(102)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation ZNIEFF2 dans zone etude
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_znieff2_ =0,\r\n'WFS:// pagingEnabled=\\'true\\' preferCoordinatesForWfsT11=\\'false\\' restrictToRequestBBOX=\\'1\\' srsname=\\'EPSG:2154\\' typename=\\'ms:Znieff2\\' url=\\'https://ws.carmencarto.fr/WFS/119/fxx_inpn\\' version=\\'auto\\'',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\znieff2_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['TamponEspacesNaturels']['OUTPUT'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationZnieff2DansZoneEtude'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(103)
        if feedback.isCanceled():
            return {}

        # Réparer les géométries Ramsar
        alg_params = {
            'INPUT': outputs['ExtraireParLocalisationRamsarDansZoneetude']['OUTPUT'],
            'METHOD': 1,  # Structure
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RparerLesGomtriesRamsar'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(104)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation RNR dans zoneEtude
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_rnr_ =0,\r\n'WFS:// pagingEnabled=\\'true\\' preferCoordinatesForWfsT11=\\'false\\' restrictToRequestBBOX=\\'1\\' srsname=\\'EPSG:2154\\' typename=\\'ms:Reserves_naturelles_regionales\\' url=\\'https://ws.carmencarto.fr/WFS/119/fxx_inpn\\' version=\\'auto\\'',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\reservesRegionales_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['TamponEspacesNaturels']['OUTPUT'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationRnrDansZoneetude'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(105)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation Reserve Biologique dans zoneEtude
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_reserve_biologique_=0,\r\n'WFS:// pagingEnabled=\\'true\\' preferCoordinatesForWfsT11=\\'false\\' restrictToRequestBBOX=\\'1\\' srsname=\\'EPSG:2154\\' typename=\\'ms:Reserves_biologiques\\' url=\\'https://ws.carmencarto.fr/WFS/119/fxx_inpn\\' version=\\'auto\\'',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\reservesBiologiques_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['TamponEspacesNaturels']['OUTPUT'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationReserveBiologiqueDansZoneetude'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(106)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation Reserve de Biosphere dans zoneEtude
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_reserve_biosphre_=0,\r\n'WFS:// pagingEnabled=\\'true\\' preferCoordinatesForWfsT11=\\'false\\' restrictToRequestBBOX=\\'1\\' srsname=\\'EPSG:2154\\' typename=\\'ms:Reserves_de_la_biosphere\\' url=\\'https://ws.carmencarto.fr/WFS/119/fxx_inpn\\' version=\\'auto\\'',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\reservesBiosphere_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['TamponEspacesNaturels']['OUTPUT'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationReserveDeBiosphereDansZoneetude'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(107)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation Aléa inondations fréquent
        alg_params = {
            'INPUT': QgsExpression("if (  @utiliser_le_flux_alea_inondation_frequent_ =0,\r\n  @Réparer_les_géométries_Aléa_inondation_frequent_OUTPUT ,\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\aleaInondationFrequent_vide.gpkg')").evaluate(),
            'INTERSECT': parameters['veuillez_slectionner_la_couche_de_la_zone_dtude_'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationAlaInondationsFrquent'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(108)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation cavites souterraines
        alg_params = {
            'INPUT': QgsExpression("if (  @utiliser_le_flux_cavits_souterraines_abandonnes_non_minires_ =0,\n'WFS:// pagingEnabled=\\'true\\' preferCoordinatesForWfsT11=\\'false\\' restrictToRequestBBOX=\\'1\\' srsname=\\'EPSG:4326\\' typename=\\'ms:CAVITE_LOCALISEE\\' url=\\'http://geoservices.brgm.fr/risques\\' version=\\'auto\\'',\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\cavitesSouterraines_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['ReprojeterTamponEn4326']['OUTPUT'],
            'PREDICATE': [0,6],  # intersecte,est à l'intérieur
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationCavitesSouterraines'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(109)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ nomClient_SAGE
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'nomClient',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': ' @quelestlenomdumatredouvrage ',
            'INPUT': outputs['CalculatriceDeChampCheminlogo_sage']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampNomclient_sage'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(110)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ % climat
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': '%',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Décimal (double)
            'FORMULA': 'surface/(sum($area))*100',
            'INPUT': outputs['CalculatriceDeChampSurfaceClimat']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampClimat'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(111)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation ZPS dans zone etude
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_zps_ =0,\r\n'WFS:// pagingEnabled=\\'true\\' preferCoordinatesForWfsT11=\\'false\\' restrictToRequestBBOX=\\'1\\' srsname=\\'EPSG:2154\\' typename=\\'ms:Zones_de_protection_speciale\\' url=\\'https://ws.carmencarto.fr/WFS/119/fxx_inpn\\' version=\\'auto\\'',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\zps_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['TamponEspacesNaturels']['OUTPUT'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationZpsDansZoneEtude'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(112)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ tampon RN 
        alg_params = {
            'FIELD_LENGTH': 100,
            'FIELD_NAME': 'Tampon',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': " @quelle_est_la_valeur_du_tampon_de_recherche_que_vous_souhaitez_en_km_pour_les_zonages_despaces_naturels_ ||' km'\r\n",
            'INPUT': outputs['RparerLesGomtriesRn']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampTamponRn'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(113)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation ZICO
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_zico_ =0,\r\n'WFS:// pagingEnabled=\\'true\\' preferCoordinatesForWfsT11=\\'false\\' restrictToRequestBBOX=\\'1\\' srsname=\\'EPSG:2154\\' typename=\\'ms:ZICO\\' url=\\'https://ws.carmencarto.fr/WFS/119/fxx_inpn\\' version=\\'auto\\'',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\zico_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['TamponEspacesNaturels']['OUTPUT'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationZico'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(114)
        if feedback.isCanceled():
            return {}

        # Calculatrice du champ surface_ha  zone etude
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'surface_ha',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Décimal (double)
            'FORMULA': ' $area /10000',
            'INPUT': outputs['AjouterUnChampSurface_haLaCoucheZoneEtude']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDuChampSurface_haZoneEtude'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(115)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation pnr dans zoneEtude
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_pnr_ =0,\r\n'WFS:// pagingEnabled=\\'true\\' preferCoordinatesForWfsT11=\\'false\\' restrictToRequestBBOX=\\'1\\' srsname=\\'EPSG:2154\\' typename=\\'ms:Parcs_naturels_regionaux\\' url=\\'https://ws.carmencarto.fr/WFS/119/fxx_inpn\\' version=\\'auto\\'',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\PNR_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['TamponEspacesNaturels']['OUTPUT'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationPnrDansZoneetude'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(116)
        if feedback.isCanceled():
            return {}

        # Couper CLC par zone etude
        alg_params = {
            'INPUT': outputs['ExtraireParLocalisationClcDansZoneEtude']['OUTPUT'],
            'OVERLAY': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CouperClcParZoneEtude'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(117)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation zones vulnérables
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_zones_vulnerables_nitrates_=0,\r\n @Réparer_les_géométries_Zones_vulnérables_INI_OUTPUT ,\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\zonesVulnerables_vide.gpkg')").evaluate(),
            'INTERSECT': parameters['veuillez_slectionner_la_couche_de_la_zone_dtude_'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationZonesVulnrables'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(118)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ cheminLogo_site
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'cheminLogo',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': ' @veuillezlocaliserlelogoduclient ',
            'INPUT': outputs['CalculatriceDuChampSurface_haZoneEtude']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampCheminlogo_site'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(119)
        if feedback.isCanceled():
            return {}

        # Couper Zones Vulnérables
        alg_params = {
            'INPUT': outputs['ExtraireParLocalisationZonesVulnrables']['OUTPUT'],
            'OVERLAY': parameters['veuillez_slectionner_la_couche_de_la_zone_dtude_'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CouperZonesVulnrables'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(120)
        if feedback.isCanceled():
            return {}

        # Statistiques par catégories RPG
        alg_params = {
            'CATEGORIES_FIELD_NAME': ['CODE_CULTU'],
            'INPUT': outputs['CalculatriceDeChampSurf_parcRpg']['OUTPUT'],
            'VALUES_FIELD_NAME': 'SURF_PARC',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['StatistiquesParCatgoriesRpg'] = processing.run('qgis:statisticsbycategories', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(121)
        if feedback.isCanceled():
            return {}

        # Réparer les géométries ZPS
        alg_params = {
            'INPUT': outputs['ExtraireParLocalisationZpsDansZoneEtude']['OUTPUT'],
            'METHOD': 1,  # Structure
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RparerLesGomtriesZps'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(122)
        if feedback.isCanceled():
            return {}

        # Réparer les géométries Zonages Cartes Communales INI
        alg_params = {
            'INPUT': outputs['ExtraireParLocalisationZonagesCartesCommunalesSansVerifGeom']['OUTPUT'],
            'METHOD': 1,  # Structure
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RparerLesGomtriesZonagesCartesCommunalesIni'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(123)
        if feedback.isCanceled():
            return {}

        # Ligne la plus courte entre les entités ZPS
        alg_params = {
            'DESTINATION': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'DISTANCE': None,
            'METHOD': 0,  # Distance to Nearest Point on feature
            'NEIGHBORS': 1,
            'SOURCE': outputs['RparerLesGomtriesZps']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['LigneLaPlusCourteEntreLesEntitsZps'] = processing.run('native:shortestline', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(124)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation ZNIEFF1 dans zone etude
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_znieff1_ =0,\r\n'WFS:// pagingEnabled=\\'true\\' preferCoordinatesForWfsT11=\\'false\\' restrictToRequestBBOX=\\'1\\' srsname=\\'EPSG:2154\\' typename=\\'ms:Znieff1\\' url=\\'https://ws.carmencarto.fr/WFS/119/fxx_inpn\\' version=\\'auto\\'',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\znieff1_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['TamponEspacesNaturels']['OUTPUT'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationZnieff1DansZoneEtude'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(125)
        if feedback.isCanceled():
            return {}

        # Réparer les géométries Reserve de Biosphere
        alg_params = {
            'INPUT': outputs['ExtraireParLocalisationReserveDeBiosphereDansZoneetude']['OUTPUT'],
            'METHOD': 1,  # Structure
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RparerLesGomtriesReserveDeBiosphere'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(126)
        if feedback.isCanceled():
            return {}

        # Ligne la plus courte entre les entités zoneEttude rose des vents IOWA
        alg_params = {
            'DESTINATION': outputs['GomtrieDempriseMinimaleZoneetude']['OUTPUT'],
            'DISTANCE': None,
            'METHOD': 0,  # Distance to Nearest Point on feature
            'NEIGHBORS': 1,
            'SOURCE': outputs['ExtraireDansUnRayon50KmRosesDesVentsIowa']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['LigneLaPlusCourteEntreLesEntitsZoneettudeRoseDesVentsIowa'] = processing.run('native:shortestline', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(127)
        if feedback.isCanceled():
            return {}

        # Ligne la plus courte entre les entités ZoneEtude BSS
        alg_params = {
            'DESTINATION': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'DISTANCE': None,
            'METHOD': 0,  # Distance to Nearest Point on feature
            'NEIGHBORS': 1,
            'SOURCE': outputs['ExtraireDansUnRayon1kmBss']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['LigneLaPlusCourteEntreLesEntitsZoneetudeBss'] = processing.run('native:shortestline', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(128)
        if feedback.isCanceled():
            return {}

        # Ajouter un champ CdFrMasseDEau
        alg_params = {
            'FIELD_ALIAS': None,
            'FIELD_COMMENT': None,
            'FIELD_LENGTH': 20,
            'FIELD_NAME': 'CdFrMasseDEau',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'INPUT': outputs['ExtraireParAttributHorizon1']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AjouterUnChampCdfrmassedeau'] = processing.run('native:addfieldtoattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(129)
        if feedback.isCanceled():
            return {}

        # Réparer les géométries APHabitatsNaturels
        alg_params = {
            'INPUT': outputs['ExtraireParLocalisationAphabitatsnaturelsDansZoneetude']['OUTPUT'],
            'METHOD': 1,  # Structure
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RparerLesGomtriesAphabitatsnaturels'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(130)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ nomProjet_SAGE
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'nomProjet',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': ' @quelestlenomduprojet ',
            'INPUT': outputs['CalculatriceDeChampNomclient_sage']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampNomprojet_sage'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(131)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source climat
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_la_couche_climat_ =0 THEN 'https://www.assistancescolaire.com/enseignant/elementaire/ressources/base-documentaire-en-geographie/france_climates et NCA Environnement '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_la_couche_climat_ =1 THEN '[Refus de l\\'utilisateur]'\r\nEND\r\n\r\n\r\n\r\n\r\n\r\n",
            'INPUT': outputs['CalculatriceDeChampClimat']['OUTPUT'],
            'OUTPUT': QgsExpression("@localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\Climat_intersect.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceClimat'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(132)
        if feedback.isCanceled():
            return {}

        # Renommer le champ _max en Alt_max
        alg_params = {
            'FIELD': '_max',
            'INPUT': outputs['RenommerLeChamp_minEnAlt_min']['OUTPUT'],
            'NEW_NAME': 'Alt_max',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenommerLeChamp_maxEnAlt_max'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(133)
        if feedback.isCanceled():
            return {}

        # Réparer les géométries SIC
        alg_params = {
            'INPUT': outputs['ExtraireParLocalisationSicDansZoneEtude']['OUTPUT'],
            'METHOD': 1,  # Structure
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RparerLesGomtriesSic'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(134)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ nomClient_site
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'nomClient',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': ' @quelestlenomdumatredouvrage ',
            'INPUT': outputs['CalculatriceDeChampCheminlogo_site']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampNomclient_site'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(135)
        if feedback.isCanceled():
            return {}

        # Réparer les géométries RNR
        alg_params = {
            'INPUT': outputs['ExtraireParLocalisationRnrDansZoneetude']['OUTPUT'],
            'METHOD': 1,  # Structure
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RparerLesGomtriesRnr'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(136)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ nomClient_ZoneEtude emprise
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'nomClient',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': '@quelestlenomdumatredouvrage ',
            'INPUT': outputs['CalculatriceDeChampCheminlogo_zoneetudeEmprise']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampNomclient_zoneetudeEmprise'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(137)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source Aléa inondations fréquent
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_alea_inondation_frequent_ =0 THEN 'http://georisques.gouv.fr/services - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_alea_inondation_frequent_=1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND\r\n",
            'INPUT': outputs['ExtraireParLocalisationAlaInondationsFrquent']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\AleaInondationFrequent_intersect.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceAlaInondationsFrquent'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(138)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ tampon Reserves de Biosphere
        alg_params = {
            'FIELD_LENGTH': 100,
            'FIELD_NAME': 'Tampon',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': " @quelle_est_la_valeur_du_tampon_de_recherche_que_vous_souhaitez_en_km_pour_les_zonages_despaces_naturels_ ||' km'\r\n",
            'INPUT': outputs['RparerLesGomtriesReserveDeBiosphere']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampTamponReservesDeBiosphere'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(139)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation Parcs Nationaux dans zoneEtude
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_parcs_nationaux_ =0,\r\n'WFS:// pagingEnabled=\\'true\\' preferCoordinatesForWfsT11=\\'false\\' restrictToRequestBBOX=\\'1\\' srsname=\\'EPSG:2154\\' typename=\\'ms:Parcs_nationaux\\' url=\\'https://ws.carmencarto.fr/WFS/119/fxx_inpn\\' version=\\'auto\\'',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\parcsNationaux_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['TamponEspacesNaturels']['OUTPUT'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationParcsNationauxDansZoneetude'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(140)
        if feedback.isCanceled():
            return {}

        # Ligne la plus courte entre les entités RNR
        alg_params = {
            'DESTINATION': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'DISTANCE': None,
            'METHOD': 0,  # Distance to Nearest Point on feature
            'NEIGHBORS': 1,
            'SOURCE': outputs['RparerLesGomtriesRnr']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['LigneLaPlusCourteEntreLesEntitsRnr'] = processing.run('native:shortestline', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(141)
        if feedback.isCanceled():
            return {}

        # Réparer les géométries ZICO
        alg_params = {
            'INPUT': outputs['ExtraireParLocalisationZico']['OUTPUT'],
            'METHOD': 1,  # Structure
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RparerLesGomtriesZico'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(142)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ tampon ZPS
        alg_params = {
            'FIELD_LENGTH': 100,
            'FIELD_NAME': 'Tampon',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': " @quelle_est_la_valeur_du_tampon_de_recherche_que_vous_souhaitez_en_km_pour_les_zonages_despaces_naturels_ ||' km'",
            'INPUT': outputs['RparerLesGomtriesZps']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampTamponZps'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(143)
        if feedback.isCanceled():
            return {}

        # Conserver le champ CODE_CULTU et sum RPG
        alg_params = {
            'FIELDS': ['CODE_CULTU','CODE_GROUP','sum'],
            'INPUT': outputs['StatistiquesParCatgoriesRpg']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ConserverLeChampCode_cultuEtSumRpg'] = processing.run('native:retainfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(144)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation 40 km perimetres MH
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_la_couche_monuments_historiques_=0,\r\n'R:\\\\SIG\\\\01_Vecteur\\\\Milieu_humain\\\\ATLAS DU PATRIMOINE\\\\Atlas_FRANCE\\\\PerimetresMonumentsHistoriques_France.shp',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\perimetreMH_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['TamponZoneEtude40km']['OUTPUT'],
            'PREDICATE': [0,4],  # intersecte,touche
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisation40KmPerimetresMh'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(145)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation APPB dans zoneEtude
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_appb_ =0,\r\n'WFS:// pagingEnabled=\\'true\\' preferCoordinatesForWfsT11=\\'false\\' restrictToRequestBBOX=\\'1\\' srsname=\\'EPSG:2154\\' typename=\\'ms:Arretes_de_protection_de_biotope\\' url=\\'https://ws.carmencarto.fr/WFS/119/fxx_inpn\\' version=\\'auto\\'',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\APPB_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['TamponEspacesNaturels']['OUTPUT'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationAppbDansZoneetude'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(146)
        if feedback.isCanceled():
            return {}

        # Réparer les géométries Zonages PLU
        alg_params = {
            'INPUT': outputs['ExtraireParLocalisationZonagesPluSansVerifGeom']['OUTPUT'],
            'METHOD': 1,  # Structure
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RparerLesGomtriesZonagesPlu'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(147)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ lien4326
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'lien4326',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "'https://www.geoportail-urbanisme.gouv.fr/map/#tile=1&lon='||to_string(attribute( get_feature( @Calculatrice_de_champ_idUnique_Zone_etude_4326_OUTPUT  , 'idUnique', 1),'x'))||'&lat='||to_string(attribute( get_feature( @Calculatrice_de_champ_idUnique_Zone_etude_4326_OUTPUT  , 'idUnique', 1),'y'))||'&zoom=14'",
            'INPUT': outputs['CalculatriceDeChampIduniqueZoneEtude4326']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampLien4326'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(148)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ nomHER1
        alg_params = {
            'FIELD_LENGTH': 100,
            'FIELD_NAME': 'nomHER1',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': 'CASE \r\nWHEN "cdHER1"=1 THEN \'PYRENEES\'\r\nWHEN "CdHER1"=2 THEN \'ALPES INTERNES\'\r\nWHEN "CdHER1"=3 THEN \'MASSIF CENTRAL SUD\'\r\nWHEN "CdHER1"=4 THEN \'VOSGES\'\r\nWHEN "CdHER1"=5 THEN \'JURA-PREALPES DU NORD\'\r\nWHEN "CdHER1"=6 THEN \'MEDITERRANEEN\'\r\nWHEN "CdHER1"=7 THEN \'PREALPES DU SUD\'\r\nWHEN "CdHER1"=8 THEN \'CEVENNES\'\r\nWHEN "CdHER1"=9 THEN \'TABLES CALCAIRES\'\r\nWHEN "CdHER1"=10 THEN \'COTES CALCAIRES EST\'\r\nWHEN "CdHER1"=11 THEN \'CAUSSES AQUITAINS\'\r\nWHEN "CdHER1"=12 THEN \'ARMORICAIN\'\r\nWHEN "CdHER1"=13 THEN \'LANDES\'\r\nWHEN "CdHER1"=14 THEN \'COTEAUX AQUITAINS\'\r\nWHEN "CdHER1"=15 THEN \'PLAINE SAONE\'\r\nWHEN "CdHER1"=16 THEN \'CORSE\'\r\nWHEN "CdHER1"=17 THEN \'DEPRESSIONS SEDIMENTAIRES\'\r\nWHEN "CdHER1"=18 THEN \'ALSACE\'\r\nWHEN "CdHER1"=19 THEN \'GRANDS CAUSSES\'\r\nWHEN "CdHER1"=20 THEN \'DEPOTS ARGILEUX SABLEUX\'\r\nWHEN "CdHER1"=21 THEN \'MASSIF CENTRAL NORD\'\r\nWHEN "CdHER1"=22 THEN \'ARDENNES\'\r\nEND',
            'INPUT': outputs['ExtraireParLocalisationHydroecoregions']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampNomher1'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(149)
        if feedback.isCanceled():
            return {}

        # Ligne la plus courte entre les entités zoneEtude stationsMeteo
        alg_params = {
            'DESTINATION': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'DISTANCE': None,
            'METHOD': 0,  # Distance to Nearest Point on feature
            'NEIGHBORS': 1,
            'SOURCE': outputs['ExtraireDansUnRayon50kmStationsmeteo']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['LigneLaPlusCourteEntreLesEntitsZoneetudeStationsmeteo'] = processing.run('native:shortestline', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(150)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ tampon APHabitatsNaturels
        alg_params = {
            'FIELD_LENGTH': 100,
            'FIELD_NAME': 'Tampon',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': " @quelle_est_la_valeur_du_tampon_de_recherche_que_vous_souhaitez_en_km_pour_les_zonages_despaces_naturels_ ||' km'\r\n",
            'INPUT': outputs['RparerLesGomtriesAphabitatsnaturels']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampTamponAphabitatsnaturels'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(151)
        if feedback.isCanceled():
            return {}

        # Joindre les attributs par valeur de champ RN
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': QgsExpression("'ID_MNHN'").evaluate(),
            'FIELDS_TO_COPY': QgsExpression("'distance'").evaluate(),
            'FIELD_2': QgsExpression("'ID_MNHN'").evaluate(),
            'INPUT': outputs['CalculatriceDeChampTamponRn']['OUTPUT'],
            'INPUT_2': outputs['LigneLaPlusCourteEntreLesEntitsRn']['OUTPUT'],
            'METHOD': 1,  # Prendre uniquement les attributs de la première entité correspondante (un à un)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoindreLesAttributsParValeurDeChampRn'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(152)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ shape_area clc zone etude
        alg_params = {
            'FIELD_LENGTH': 20,
            'FIELD_NAME': 'shape_area',
            'FIELD_PRECISION': 7,
            'FIELD_TYPE': 0,  # Décimal (double)
            'FORMULA': ' $area /10000',
            'INPUT': outputs['CouperClcParZoneEtude']['OUTPUT'],
            'OUTPUT': QgsExpression("@localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\clc_clip.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampShape_areaClcZoneEtude'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(153)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ tampon Ramsar
        alg_params = {
            'FIELD_LENGTH': 100,
            'FIELD_NAME': 'Tampon',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': " @quelle_est_la_valeur_du_tampon_de_recherche_que_vous_souhaitez_en_km_pour_les_zonages_despaces_naturels_ ||' km'\r\n",
            'INPUT': outputs['RparerLesGomtriesRamsar']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampTamponRamsar'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(154)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation communes 40 km
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_communes_tampon_=0,\r\n'WFS:// pagingEnabled=\\'true\\' preferCoordinatesForWfsT11=\\'false\\' restrictToRequestBBOX=\\'1\\' srsname=\\'EPSG:4326\\' typename=\\'BDTOPO_V3:commune\\' url=\\'https://data.geopf.fr/wfs/ows\\' url=\\'https://data.geopf.fr/wfs/ows?VERSION=2.0.0\\' version=\\'auto\\'',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\communesTampon_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['TamponZoneEtude40km']['OUTPUT'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationCommunes40Km'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(155)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ tampon stations débit
        alg_params = {
            'FIELD_LENGTH': 100,
            'FIELD_NAME': 'Tampon',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': " @valeurdutamponderecherchepourlesstationsqualitetdbitenmtres ||' m'",
            'INPUT': outputs['ExtraireParLocalisationStationsDbitDansTampon']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampTamponStationsDbit'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(156)
        if feedback.isCanceled():
            return {}

        # Renommer le champ sum RPG
        alg_params = {
            'FIELD': 'sum',
            'INPUT': outputs['ConserverLeChampCode_cultuEtSumRpg']['OUTPUT'],
            'NEW_NAME': 'surface_ha',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenommerLeChampSumRpg'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(157)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ tampon stations qualité
        alg_params = {
            'FIELD_LENGTH': 100,
            'FIELD_NAME': 'Tampon',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': " @valeurdutamponderecherchepourlesstationsqualitetdbitenmtres ||' m'",
            'INPUT': outputs['ExtraireParLocalisationStationsQualitDansTampon']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampTamponStationsQualit'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(158)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation Zonages Cartes Communales
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_zonages_cartes_communales_=0,\r\n @Réparer_les_géométries_Zonages_Cartes_Communales_INI_OUTPUT ,\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\zonesCartesCommunales_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['Tampon100mZonagesCartesCommunales']['OUTPUT'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationZonagesCartesCommunales'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(159)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ tampon RNR
        alg_params = {
            'FIELD_LENGTH': 100,
            'FIELD_NAME': 'Tampon',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': " @quelle_est_la_valeur_du_tampon_de_recherche_que_vous_souhaitez_en_km_pour_les_zonages_despaces_naturels_ ||' km'",
            'INPUT': outputs['RparerLesGomtriesRnr']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampTamponRnr'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(160)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source SAGE
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_des_sage_ =0 THEN 'https://services.sandre.eaufrance.fr/geo/sandre - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_des_sage_ =1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND\r\n\r\n",
            'INPUT': outputs['CalculatriceDeChampNomprojet_sage']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\sage_intersect.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceSage'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(161)
        if feedback.isCanceled():
            return {}

        # Reprojeter une couche en 2154 stations qualité
        alg_params = {
            'CONVERT_CURVED_GEOMETRIES': False,
            'INPUT': outputs['CalculatriceDeChampTamponStationsQualit']['OUTPUT'],
            'OPERATION': None,
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:2154'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojeterUneCoucheEn2154StationsQualit'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(162)
        if feedback.isCanceled():
            return {}

        # Ligne la plus courte entre les entités APHabitatsNaturels
        alg_params = {
            'DESTINATION': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'DISTANCE': None,
            'METHOD': 0,  # Distance to Nearest Point on feature
            'NEIGHBORS': 1,
            'SOURCE': outputs['RparerLesGomtriesAphabitatsnaturels']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['LigneLaPlusCourteEntreLesEntitsAphabitatsnaturels'] = processing.run('native:shortestline', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(163)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ Tampon cavites souterraines
        alg_params = {
            'FIELD_LENGTH': 100,
            'FIELD_NAME': 'Tampon',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': " @valeurdutamponderecherchepourlesstationsqualitetdbitenmtres ||' m'",
            'INPUT': outputs['ExtraireParLocalisationCavitesSouterraines']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampTamponCavitesSouterraines'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(164)
        if feedback.isCanceled():
            return {}

        # Ajouter un champ area_ha à la couche contexte Piscicole
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'area_ha',
            'FIELD_PRECISION': 2,
            'FIELD_TYPE': 0,  # Entier (32bit)
            'INPUT': outputs['CouperContextePiscicoleParZoneEtude']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AjouterUnChampArea_haLaCoucheContextePiscicole'] = processing.run('native:addfieldtoattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(165)
        if feedback.isCanceled():
            return {}

        # Ligne la plus courte entre les entités SIC
        alg_params = {
            'DESTINATION': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'DISTANCE': None,
            'METHOD': 0,  # Distance to Nearest Point on feature
            'NEIGHBORS': 1,
            'SOURCE': outputs['RparerLesGomtriesSic']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['LigneLaPlusCourteEntreLesEntitsSic'] = processing.run('native:shortestline', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(166)
        if feedback.isCanceled():
            return {}

        # Ligne la plus courte entre les entités Ramsar
        alg_params = {
            'DESTINATION': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'DISTANCE': None,
            'METHOD': 0,  # Distance to Nearest Point on feature
            'NEIGHBORS': 1,
            'SOURCE': outputs['RparerLesGomtriesRamsar']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['LigneLaPlusCourteEntreLesEntitsRamsar'] = processing.run('native:shortestline', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(167)
        if feedback.isCanceled():
            return {}

        # Géométrie d'emprise minimale SAGE
        alg_params = {
            'FIELD': None,
            'INPUT': outputs['CalculatriceDeChampSourceSage']['OUTPUT'],
            'TYPE': 3,  # Enveloppe convexe
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['GomtrieDempriseMinimaleSage'] = processing.run('qgis:minimumboundinggeometry', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(168)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ nomProjet_ZoneEtude emprise
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'nomProjet',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': ' @quelestlenomduprojet ',
            'INPUT': outputs['CalculatriceDeChampNomclient_zoneetudeEmprise']['OUTPUT'],
            'OUTPUT': QgsExpression("@localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\ZoneEtude_emprise.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampNomprojet_zoneetudeEmprise'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(169)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ lienLocaGPU Zonages Cartes Communales
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'lienLocaGPU',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "to_string(attribute( get_feature(   @Calculatrice_de_champ_lien4326_OUTPUT   , 'idUnique', 1),'lien4326'))\r\n",
            'INPUT': outputs['ExtraireParLocalisationZonagesCartesCommunales']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampLienlocagpuZonagesCartesCommunales'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(170)
        if feedback.isCanceled():
            return {}

        # Réparer les géométries ZNIEFF2
        alg_params = {
            'INPUT': outputs['ExtraireParLocalisationZnieff2DansZoneEtude']['OUTPUT'],
            'METHOD': 1,  # Structure
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RparerLesGomtriesZnieff2'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(171)
        if feedback.isCanceled():
            return {}

        # Joindre les attributs par valeur de champ rose des vents IOWA
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'Station_Identifier',
            'FIELDS_TO_COPY': ['distance'],
            'FIELD_2': 'Station_Identifier',
            'INPUT': outputs['ExtraireDansUnRayon50KmRosesDesVentsIowa']['OUTPUT'],
            'INPUT_2': outputs['LigneLaPlusCourteEntreLesEntitsZoneettudeRoseDesVentsIowa']['OUTPUT'],
            'METHOD': 1,  # Prendre uniquement les attributs de la première entité correspondante (un à un)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoindreLesAttributsParValeurDeChampRoseDesVentsIowa'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(172)
        if feedback.isCanceled():
            return {}

        # Réparer les géométries ZNIEFF1
        alg_params = {
            'INPUT': outputs['ExtraireParLocalisationZnieff1DansZoneEtude']['OUTPUT'],
            'METHOD': 1,  # Structure
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RparerLesGomtriesZnieff1'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(173)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ fid MH
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'fid',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Entier (32bit)
            'FORMULA': '@id',
            'INPUT': outputs['ExtraireParLocalisation40KmPerimetresMh']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampFidMh'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(174)
        if feedback.isCanceled():
            return {}

        # Réparer les géométries Reserve Biologique
        alg_params = {
            'INPUT': outputs['ExtraireParLocalisationReserveBiologiqueDansZoneetude']['OUTPUT'],
            'METHOD': 1,  # Structure
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RparerLesGomtriesReserveBiologique'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(175)
        if feedback.isCanceled():
            return {}

        # Ajouter un champ LIB_CULTU RPG
        alg_params = {
            'FIELD_ALIAS': None,
            'FIELD_COMMENT': None,
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'LIB_CULTU',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'INPUT': outputs['RenommerLeChampSumRpg']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AjouterUnChampLib_cultuRpg'] = processing.run('native:addfieldtoattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(176)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ CdFrMasseDEau
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'CdFrMasseDEau',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': 'regexp_replace("CdEuMasseDEau",\'FR\',\'\')',
            'INPUT': outputs['AjouterUnChampCdfrmassedeau']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampCdfrmassedeau'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(177)
        if feedback.isCanceled():
            return {}

        # Reprojeter une couche en 2154 stations débit
        alg_params = {
            'CONVERT_CURVED_GEOMETRIES': False,
            'INPUT': outputs['CalculatriceDeChampTamponStationsDbit']['OUTPUT'],
            'OPERATION': None,
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:2154'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojeterUneCoucheEn2154StationsDbit'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(178)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ tampon SIC
        alg_params = {
            'FIELD_LENGTH': 100,
            'FIELD_NAME': 'Tampon',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': " @quelle_est_la_valeur_du_tampon_de_recherche_que_vous_souhaitez_en_km_pour_les_zonages_despaces_naturels_ ||' km'",
            'INPUT': outputs['RparerLesGomtriesSic']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampTamponSic'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(179)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ tampon Reserve Biologique
        alg_params = {
            'FIELD_LENGTH': 100,
            'FIELD_NAME': 'Tampon',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': " @quelle_est_la_valeur_du_tampon_de_recherche_que_vous_souhaitez_en_km_pour_les_zonages_despaces_naturels_ ||' km'\r\n",
            'INPUT': outputs['RparerLesGomtriesReserveBiologique']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampTamponReserveBiologique'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(180)
        if feedback.isCanceled():
            return {}

        # Joindre les attributs par valeur de champ SIC
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': QgsExpression("'SITECODE'").evaluate(),
            'FIELDS_TO_COPY': QgsExpression("'distance'").evaluate(),
            'FIELD_2': QgsExpression("'SITECODE'").evaluate(),
            'INPUT': outputs['CalculatriceDeChampTamponSic']['OUTPUT'],
            'INPUT_2': outputs['LigneLaPlusCourteEntreLesEntitsSic']['OUTPUT'],
            'METHOD': 1,  # Prendre uniquement les attributs de la première entité correspondante (un à un)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoindreLesAttributsParValeurDeChampSic'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(181)
        if feedback.isCanceled():
            return {}

        # Tampon 1km
        alg_params = {
            'DISSOLVE': True,
            'DISTANCE': 1000,
            'END_CAP_STYLE': 0,  # Rond
            'INPUT': outputs['CalculatriceDeChampNomprojet_zoneetudeEmprise']['OUTPUT'],
            'JOIN_STYLE': 0,  # Rond
            'MITER_LIMIT': 2,
            'OUTPUT': QgsExpression("@localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\Tampon_1km.gpkg'").evaluate(),
            'SEGMENTS': 5,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Tampon1km'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(182)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ tampon ZICO
        alg_params = {
            'FIELD_LENGTH': 100,
            'FIELD_NAME': 'Tampon',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': " @quelle_est_la_valeur_du_tampon_de_recherche_que_vous_souhaitez_en_km_pour_les_zonages_despaces_naturels_ ||' km'",
            'INPUT': outputs['RparerLesGomtriesZico']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampTamponZico'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(183)
        if feedback.isCanceled():
            return {}

        # Ligne la plus courte entre les entités ZICO
        alg_params = {
            'DESTINATION': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'DISTANCE': None,
            'METHOD': 0,  # Distance to Nearest Point on feature
            'NEIGHBORS': 1,
            'SOURCE': outputs['RparerLesGomtriesZico']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['LigneLaPlusCourteEntreLesEntitsZico'] = processing.run('native:shortestline', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(184)
        if feedback.isCanceled():
            return {}

        # Joindre les attributs par valeur de champ stationsMeteo
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'Indicatif',
            'FIELDS_TO_COPY': ['distance'],
            'FIELD_2': 'Indicatif',
            'INPUT': outputs['ExtraireDansUnRayon50kmStationsmeteo']['OUTPUT'],
            'INPUT_2': outputs['LigneLaPlusCourteEntreLesEntitsZoneetudeStationsmeteo']['OUTPUT'],
            'METHOD': 1,  # Prendre uniquement les attributs de la première entité correspondante (un à un)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoindreLesAttributsParValeurDeChampStationsmeteo'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(185)
        if feedback.isCanceled():
            return {}

        # Réparer les géométries APPB
        alg_params = {
            'INPUT': outputs['ExtraireParLocalisationAppbDansZoneetude']['OUTPUT'],
            'METHOD': 1,  # Structure
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RparerLesGomtriesAppb'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(186)
        if feedback.isCanceled():
            return {}

        # Ligne la plus courte entre les entités stations débit
        alg_params = {
            'DESTINATION': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'DISTANCE': None,
            'METHOD': 0,  # Distance to Nearest Point on feature
            'NEIGHBORS': 1,
            'SOURCE': outputs['ReprojeterUneCoucheEn2154StationsDbit']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['LigneLaPlusCourteEntreLesEntitsStationsDbit'] = processing.run('native:shortestline', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(187)
        if feedback.isCanceled():
            return {}

        # Conserver le champ code et area_ha clc_clip_zone etude
        alg_params = {
            'FIELDS': ['code_18','area_ha'],
            'INPUT': outputs['CouperClcParZoneEtude']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ConserverLeChampCodeEtArea_haClc_clip_zoneEtude'] = processing.run('native:retainfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(188)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ cheminLogo_SAGE emprise
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'cheminLogo',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': ' @veuillezlocaliserlelogoduclient ',
            'INPUT': outputs['GomtrieDempriseMinimaleSage']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampCheminlogo_sageEmprise'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(189)
        if feedback.isCanceled():
            return {}

        # Réparer les géométries Parcs Nationaux
        alg_params = {
            'INPUT': outputs['ExtraireParLocalisationParcsNationauxDansZoneetude']['OUTPUT'],
            'METHOD': 1,  # Structure
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RparerLesGomtriesParcsNationaux'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(190)
        if feedback.isCanceled():
            return {}

        # Ligne la plus courte entre les entités ZNIEFF1
        alg_params = {
            'DESTINATION': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'DISTANCE': None,
            'METHOD': 0,  # Distance to Nearest Point on feature
            'NEIGHBORS': 1,
            'SOURCE': outputs['RparerLesGomtriesZnieff1']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['LigneLaPlusCourteEntreLesEntitsZnieff1'] = processing.run('native:shortestline', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(191)
        if feedback.isCanceled():
            return {}

        # Joindre les attributs par valeur de champ RNR
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': QgsExpression("'ID_MNHN'").evaluate(),
            'FIELDS_TO_COPY': QgsExpression("'distance'").evaluate(),
            'FIELD_2': QgsExpression("'ID_MNHN'").evaluate(),
            'INPUT': outputs['CalculatriceDeChampTamponRnr']['OUTPUT'],
            'INPUT_2': outputs['LigneLaPlusCourteEntreLesEntitsRnr']['OUTPUT'],
            'METHOD': 1,  # Prendre uniquement les attributs de la première entité correspondante (un à un)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoindreLesAttributsParValeurDeChampRnr'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(192)
        if feedback.isCanceled():
            return {}

        # Joindre les attributs par valeur de champ ZPS
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': QgsExpression("'SITECODE'").evaluate(),
            'FIELDS_TO_COPY': QgsExpression("'distance'").evaluate(),
            'FIELD_2': QgsExpression("'SITECODE'").evaluate(),
            'INPUT': outputs['CalculatriceDeChampTamponZps']['OUTPUT'],
            'INPUT_2': outputs['LigneLaPlusCourteEntreLesEntitsZps']['OUTPUT'],
            'METHOD': 1,  # Prendre uniquement les attributs de la première entité correspondante (un à un)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoindreLesAttributsParValeurDeChampZps'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(193)
        if feedback.isCanceled():
            return {}

        # Réparer les géométries pnr
        alg_params = {
            'INPUT': outputs['ExtraireParLocalisationPnrDansZoneetude']['OUTPUT'],
            'METHOD': 1,  # Structure
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RparerLesGomtriesPnr'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(194)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ tampon Parcs Nationaux
        alg_params = {
            'FIELD_LENGTH': 100,
            'FIELD_NAME': 'Tampon',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': " @quelle_est_la_valeur_du_tampon_de_recherche_que_vous_souhaitez_en_km_pour_les_zonages_despaces_naturels_ ||' km'",
            'INPUT': outputs['RparerLesGomtriesParcsNationaux']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampTamponParcsNationaux'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(195)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source Masse d'eau souterraine
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_masses_do_souterraines_ =0 THEN 'https://services.sandre.eaufrance.fr/geo/sandre - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_masses_do_souterraines_ =1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND\r\n\r\n",
            'INPUT': outputs['CalculatriceDeChampCdfrmassedeau']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\masseDoSoutNiv1_intersect.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceMasseDeauSouterraine'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(196)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation Zonages PLU
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_zonages_plu_=0,\r\n @Réparer_les_géométries_Zonages_PLU_OUTPUT ,\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\zonagesPLU_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['Tampon100mZonagesPlu']['OUTPUT'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationZonagesPlu'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(197)
        if feedback.isCanceled():
            return {}

        # Tampon 5km
        alg_params = {
            'DISSOLVE': True,
            'DISTANCE': 5000,
            'END_CAP_STYLE': 0,  # Rond
            'INPUT': outputs['CalculatriceDeChampNomprojet_zoneetudeEmprise']['OUTPUT'],
            'JOIN_STYLE': 0,  # Rond
            'MITER_LIMIT': 2,
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\Tampon_5km.gpkg'").evaluate(),
            'SEGMENTS': 5,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Tampon5km'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(198)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source ZPS
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_zps_ =0 THEN 'https://ws.carmencarto.fr/WFS/119/fxx_inpn - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_zps_ =1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND",
            'INPUT': outputs['JoindreLesAttributsParValeurDeChampZps']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\zps_intersect.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceZps'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(199)
        if feedback.isCanceled():
            return {}

        # Statistiques par code_18  zone etude (tableur en sortie)
        alg_params = {
            'CATEGORIES_FIELD_NAME': ['code_18'],
            'INPUT': outputs['CalculatriceDeChampShape_areaClcZoneEtude']['OUTPUT'],
            'VALUES_FIELD_NAME': 'shape_area',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['StatistiquesParCode_18ZoneEtudeTableurEnSortie'] = processing.run('qgis:statisticsbycategories', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(200)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ tampon ZNIEFF2
        alg_params = {
            'FIELD_LENGTH': 100,
            'FIELD_NAME': 'Tampon',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': " @quelle_est_la_valeur_du_tampon_de_recherche_que_vous_souhaitez_en_km_pour_les_zonages_despaces_naturels_ ||' km'",
            'INPUT': outputs['RparerLesGomtriesZnieff2']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampTamponZnieff2'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(201)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ tampon pnr
        alg_params = {
            'FIELD_LENGTH': 100,
            'FIELD_NAME': 'Tampon',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': " @quelle_est_la_valeur_du_tampon_de_recherche_que_vous_souhaitez_en_km_pour_les_zonages_despaces_naturels_ ||' km'\r\n",
            'INPUT': outputs['RparerLesGomtriesPnr']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampTamponPnr'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(202)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ area_ha contexte Pisicicole zone etude
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'area_ha',
            'FIELD_PRECISION': 2,
            'FIELD_TYPE': 0,  # Décimal (double)
            'FORMULA': ' $area /10000',
            'INPUT': outputs['AjouterUnChampArea_haLaCoucheContextePiscicole']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampArea_haContextePisicicoleZoneEtude'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(203)
        if feedback.isCanceled():
            return {}

        # Ligne la plus courte entre les entités Reserves de Biosphere
        alg_params = {
            'DESTINATION': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'DISTANCE': None,
            'METHOD': 0,  # Distance to Nearest Point on feature
            'NEIGHBORS': 1,
            'SOURCE': outputs['CalculatriceDeChampTamponReservesDeBiosphere']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['LigneLaPlusCourteEntreLesEntitsReservesDeBiosphere'] = processing.run('native:shortestline', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(204)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ nomClient_SAGE emprise
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'nomClient',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': ' @quelestlenomdumatredouvrage ',
            'INPUT': outputs['CalculatriceDeChampCheminlogo_sageEmprise']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampNomclient_sageEmprise'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(205)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ lienDocument Zonages Cartes Communales
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'lienDocument',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': '\'https://data.geopf.fr/annexes/gpu/documents/\'||"partition"||\'/\'||"gpu_doc_id"||\'/\'||"nomfic"',
            'INPUT': outputs['CalculatriceDeChampLienlocagpuZonagesCartesCommunales']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampLiendocumentZonagesCartesCommunales'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(206)
        if feedback.isCanceled():
            return {}

        # Joindre les attributs par valeur de champ BSS
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'fid',
            'FIELDS_TO_COPY': ['distance'],
            'FIELD_2': 'fid',
            'INPUT': outputs['ExtraireDansUnRayon1kmBss']['OUTPUT'],
            'INPUT_2': outputs['LigneLaPlusCourteEntreLesEntitsZoneetudeBss']['OUTPUT'],
            'METHOD': 1,  # Prendre uniquement les attributs de la première entité correspondante (un à un)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoindreLesAttributsParValeurDeChampBss'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(207)
        if feedback.isCanceled():
            return {}

        # Ajouter un champ nomProjet à la couche zone etude
        alg_params = {
            'FIELD_ALIAS': None,
            'FIELD_COMMENT': None,
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'nomProjet',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'INPUT': outputs['CalculatriceDeChampNomclient_site']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AjouterUnChampNomprojetLaCoucheZoneEtude'] = processing.run('native:addfieldtoattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(208)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ nomProjet_SAGE emprise
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'nomProjet',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': '@quelestlenomduprojet ',
            'INPUT': outputs['CalculatriceDeChampNomclient_sageEmprise']['OUTPUT'],
            'OUTPUT': QgsExpression("@localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\sage_intersect_emprise.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampNomprojet_sageEmprise'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(209)
        if feedback.isCanceled():
            return {}

        # Ligne la plus courte entre les entités stations qualité
        alg_params = {
            'DESTINATION': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'DISTANCE': None,
            'METHOD': 0,  # Distance to Nearest Point on feature
            'NEIGHBORS': 1,
            'SOURCE': outputs['ReprojeterUneCoucheEn2154StationsQualit']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['LigneLaPlusCourteEntreLesEntitsStationsQualit'] = processing.run('native:shortestline', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(210)
        if feedback.isCanceled():
            return {}

        # Ligne la plus courte entre les entités ZNIEFF2
        alg_params = {
            'DESTINATION': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'DISTANCE': None,
            'METHOD': 0,  # Distance to Nearest Point on feature
            'NEIGHBORS': 1,
            'SOURCE': outputs['RparerLesGomtriesZnieff2']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['LigneLaPlusCourteEntreLesEntitsZnieff2'] = processing.run('native:shortestline', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(211)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation sites archéologiques 5km
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_la_couche_prescriptions_archeologiques_=0,\r\n'R:\\\\SIG\\\\01_Vecteur\\\\Milieu_humain\\\\ATLAS DU PATRIMOINE\\\\Atlas_FRANCE\\\\zonesPrescriptionsArcheologiques_France.shp',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\sitesArcheo_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['Tampon5km']['OUTPUT'],
            'PREDICATE': [0,4],  # intersecte,touche
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationSitesArchologiques5km'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(212)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source RN
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_rn_nat_ =0 THEN 'https://ws.carmencarto.fr/WFS/119/fxx_inpn - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_rn_nat_ =1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND",
            'INPUT': outputs['JoindreLesAttributsParValeurDeChampRn']['OUTPUT'],
            'OUTPUT': QgsExpression("@localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\ReservesNationales_intersect.gpkg'\n").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceRn'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(213)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ LIB_CULTU RPG
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'LIB_CULTU',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\n\r\nWHEN\tCODE_CULTU=\t'BTH'\tTHEN\t'Blé tendre d’hiver'\r\nWHEN\tCODE_CULTU=\t'BTP'\tTHEN\t'Blé tendre de printemps'\r\nWHEN\tCODE_CULTU=\t'MID'\tTHEN\t'Maïs doux'\r\nWHEN\tCODE_CULTU=\t'MIE'\tTHEN\t'Maïs ensilage'\r\nWHEN\tCODE_CULTU=\t'MIS'\tTHEN\t'Maïs (hors maïs doux)'\r\nWHEN\tCODE_CULTU=\t'ORH'\tTHEN\t'Orge d\\'hiver'\r\nWHEN\tCODE_CULTU=\t'ORP'\tTHEN\t'Orge de printemps'\r\nWHEN\tCODE_CULTU=\t'AVH'\tTHEN\t'Avoine d’hiver'\r\nWHEN\tCODE_CULTU=\t'AVP'\tTHEN\t'Avoine de printemps'\r\nWHEN\tCODE_CULTU=\t'BDH'\tTHEN\t'Blé dur d’hiver'\r\nWHEN\tCODE_CULTU=\t'BDP'\tTHEN\t'Blé dur de printemps'\r\nWHEN\tCODE_CULTU=\t'BDT'\tTHEN\t'Blé dur de printemps semé tardivement (après le 31/05)'\r\nWHEN\tCODE_CULTU=\t'CAG'\tTHEN\t'Autre céréale ou pseudo-céréale secondaire de printemps (alpiste, quinoa, chia, …)'\r\nWHEN\tCODE_CULTU=\t'CAH'\tTHEN\t'Autre céréale ou pseudo-céréale secondaire d\\'hiver'\r\nWHEN\tCODE_CULTU=\t'CGF'\tTHEN\t'Autre céréale de genre Fagopyrum'\r\nWHEN\tCODE_CULTU=\t'CGH'\tTHEN\t'Autre céréale de genre Phalaris'\r\nWHEN\tCODE_CULTU=\t'CGO'\tTHEN\t'Autre céréale de genre Sorghum'\r\nWHEN\tCODE_CULTU=\t'CGP'\tTHEN\t'Autre céréale de genre Panicum'\r\nWHEN\tCODE_CULTU=\t'CGS'\tTHEN\t'Autre céréale de genre Setaria'\r\nWHEN\tCODE_CULTU=\t'CHA'\tTHEN\t'Autre céréale d’hiver de genre Avena'\r\nWHEN\tCODE_CULTU=\t'CHH'\tTHEN\t'Autre céréale d’hiver de genre Hordeum'\r\nWHEN\tCODE_CULTU=\t'CHS'\tTHEN\t'Autre céréale d’hiver de genre Secale'\r\nWHEN\tCODE_CULTU=\t'CHT'\tTHEN\t'Autre céréale d’hiver de genre Triticum'\r\nWHEN\tCODE_CULTU=\t'CPA'\tTHEN\t'Autre céréale de printemps de genre Avena'\r\nWHEN\tCODE_CULTU=\t'CPH'\tTHEN\t'Autre céréale de printemps de genre Hordeum'\r\nWHEN\tCODE_CULTU=\t'CPS'\tTHEN\t'Autre céréale de printemps de genre Secale'\r\nWHEN\tCODE_CULTU=\t'CPT'\tTHEN\t'Autre céréale de printemps de genre Triticum'\r\nWHEN\tCODE_CULTU=\t'CPZ'\tTHEN\t'Autre céréale de printemps de genre Zea'\r\nWHEN\tCODE_CULTU=\t'EPE'\tTHEN\t'Epeautre (petit épeautre ou engrain et grand épeautre)'\r\nWHEN\tCODE_CULTU=\t'MCR'\tTHEN\t'Mélange de céréales ou pseudo-céréales d\\'hiver entre elles'\r\nWHEN\tCODE_CULTU=\t'MCS'\tTHEN\t'Mélange de céréales ou pseudo-céréales de printemps entre elles'\r\nWHEN\tCODE_CULTU=\t'MLT'\tTHEN\t'Millet'\r\nWHEN\tCODE_CULTU=\t'SGH'\tTHEN\t'Seigle d’hiver'\r\nWHEN\tCODE_CULTU=\t'SGP'\tTHEN\t'Seigle de printemps'\r\nWHEN\tCODE_CULTU=\t'SOG'\tTHEN\t'Sorgho'\r\nWHEN\tCODE_CULTU=\t'SRS'\tTHEN\t'Sarrasin'\r\nWHEN\tCODE_CULTU=\t'TTH'\tTHEN\t'Triticale d’hiver'\r\nWHEN\tCODE_CULTU=\t'TTP'\tTHEN\t'Triticale de printemps'\r\nWHEN\tCODE_CULTU=\t'CZH'\tTHEN\t'Colza d’hiver'\r\nWHEN\tCODE_CULTU=\t'CZP'\tTHEN\t'Colza de printemps'\r\nWHEN\tCODE_CULTU=\t'TRN'\tTHEN\t'Tournesol'\r\nWHEN\tCODE_CULTU=\t'ARA'\tTHEN\t'Arachide'\r\nWHEN\tCODE_CULTU=\t'LIH'\tTHEN\t'Lin non textile d’hiver'\r\nWHEN\tCODE_CULTU=\t'LIP'\tTHEN\t'Lin non textile de printemps'\r\nWHEN\tCODE_CULTU=\t'MOL'\tTHEN\t'Mélange d’oléagineux'\r\nWHEN\tCODE_CULTU=\t'NVE'\tTHEN\t'Navette d’été'\r\nWHEN\tCODE_CULTU=\t'NVH'\tTHEN\t'Navette d’hiver'\r\nWHEN\tCODE_CULTU=\t'OAG'\tTHEN\t'Autres oléagineux ou mélange d\\'oléagineux de printemps et d\\'été (dont moutarde ou navette d\\'été, sésame et nyger)'\r\nWHEN\tCODE_CULTU=\t'OEH'\tTHEN\t'Autre oléagineux d’espèce Helianthus'\r\nWHEN\tCODE_CULTU=\t'OEI'\tTHEN\t'Oeillette (pavot)'\r\nWHEN\tCODE_CULTU=\t'OHN'\tTHEN\t'Autre oléagineux d’hiver d’espèce Brassica napus'\r\nWHEN\tCODE_CULTU=\t'OHR'\tTHEN\t'Autres oléagineux ou mélange d\\'oléagineux d\\'hiver (dont navette d\\'hiver)'\r\nWHEN\tCODE_CULTU=\t'OPN'\tTHEN\t'Autre oléagineux de printemps d’espèce Brassica napus'\r\nWHEN\tCODE_CULTU=\t'OPR'\tTHEN\t'Autre oléagineux de printemps d’espèce Brassica rapa'\r\nWHEN\tCODE_CULTU=\t'SOJ'\tTHEN\t'Soja'\r\nWHEN\tCODE_CULTU=\t'FEV'\tTHEN\t'Fève'\r\nWHEN\tCODE_CULTU=\t'FVL'\tTHEN\t'Féverole d\\'hiver'\r\nWHEN\tCODE_CULTU=\t'FVP'\tTHEN\t'Féverole de printemps'\r\nWHEN\tCODE_CULTU=\t'FVT'\tTHEN\t'Féverole semée tardivement (après le 31/05)'\r\nWHEN\tCODE_CULTU=\t'LDH'\tTHEN\t'Lupin doux d’hiver'\r\nWHEN\tCODE_CULTU=\t'LDP'\tTHEN\t'Lupin doux de printemps semé avant le 31/05'\r\nWHEN\tCODE_CULTU=\t'LDT'\tTHEN\t'Lupin doux de printemps semé tardivement (après le 31/05)'\r\nWHEN\tCODE_CULTU=\t'MPC'\tTHEN\t'Mélange de protéagineux (pois et/ou lupin et/ou féverole) prépondérants semés avant le 31/05 et de céréales'\r\nWHEN\tCODE_CULTU=\t'MPP'\tTHEN\t'Mélange de protéagineux (pois et/ou lupin et/ou féverole)'\r\nWHEN\tCODE_CULTU=\t'MPT'\tTHEN\t'Mélange de protéagineux semés tardivement (après le 31/05)'\r\nWHEN\tCODE_CULTU=\t'PAG'\tTHEN\t'Autre légumineuse à graines ou fourragères'\r\nWHEN\tCODE_CULTU=\t'PHF'\tTHEN\t'Pois et haricot frais (alimentation humaine)'\r\nWHEN\tCODE_CULTU=\t'PHI'\tTHEN\t'Pois protéagineux d\\'hiver (alimentation animale)'\r\nWHEN\tCODE_CULTU=\t'PHS'\tTHEN\t'Pois et haricot secs (alimentation humaine)'\r\nWHEN\tCODE_CULTU=\t'PPR'\tTHEN\t'Pois protéagineux de printemps (alimentation animale)'\r\nWHEN\tCODE_CULTU=\t'PPT'\tTHEN\t'Pois de printemps semé tardivement (après le 31/05)'\r\nWHEN\tCODE_CULTU=\t'CHV'\tTHEN\t'Chanvre'\r\nWHEN\tCODE_CULTU=\t'CSE'\tTHEN\t'Chanvre sans étiquette conforme'\r\nWHEN\tCODE_CULTU=\t'LIF'\tTHEN\t'Lin fibres'\r\nWHEN\tCODE_CULTU=\t'J5M'\tTHEN\t'Jachère de 5 ans ou moins'\r\nWHEN\tCODE_CULTU=\t'J6P'\tTHEN\t'Jachère de 6 ans ou plus'\r\nWHEN\tCODE_CULTU=\t'J6S'\tTHEN\t'Jachère de 6 ans ou plus déclarée comme Surface d’intérêt écologique'\r\nWHEN\tCODE_CULTU=\t'JAC'\tTHEN\t'Jachère (terre arable)'\r\nWHEN\tCODE_CULTU=\t'JNO'\tTHEN\t'Jachère sanitaire imposée par l\\'administration'\r\nWHEN\tCODE_CULTU=\t'RIZ'\tTHEN\t'Riz'\r\nWHEN\tCODE_CULTU=\t'LEC'\tTHEN\t'Lentille'\r\nWHEN\tCODE_CULTU=\t'PCH'\tTHEN\t'Pois chiche'\r\nWHEN\tCODE_CULTU=\t'AFG'\tTHEN\t'Autre plante fourragère annuelle (ni légumineuse, ni graminée, ni céréale, ni oléagineux)'\r\nWHEN\tCODE_CULTU=\t'BVF'\tTHEN\t'Betterave fourragère'\r\nWHEN\tCODE_CULTU=\t'CAF'\tTHEN\t'Carotte fourragère'\r\nWHEN\tCODE_CULTU=\t'CHF'\tTHEN\t'Chou fourrager'\r\nWHEN\tCODE_CULTU=\t'CPL'\tTHEN\t'Mélange multi-espèces (céréales, oléagineux, légumineuses, …) sans graminées prairiales et sans prédominance de légumineuses'\r\nWHEN\tCODE_CULTU=\t'DTY'\tTHEN\t'Dactyle de 5 ans ou moins'\r\nWHEN\tCODE_CULTU=\t'FAG'\tTHEN\t'Autre fourrage annuel d’un autre genre'\r\nWHEN\tCODE_CULTU=\t'FET'\tTHEN\t'Fétuque de 5 ans ou moins'\r\nWHEN\tCODE_CULTU=\t'FF5'\tTHEN\t'Féverole fourragère implantée pour la récolte 2015'\r\nWHEN\tCODE_CULTU=\t'FF6'\tTHEN\t'Féverole fourragère implantée pour la récolte 2016'\r\nWHEN\tCODE_CULTU=\t'FF7'\tTHEN\t'Féverole fourragère implantée pour la récolte 2017'\r\nWHEN\tCODE_CULTU=\t'FF8'\tTHEN\t'Féverole fourragère implantée pour la récolte 2018'\r\nWHEN\tCODE_CULTU=\t'FFO'\tTHEN\t'Autre féverole fourragère'\r\nWHEN\tCODE_CULTU=\t'FLO'\tTHEN\t'Fléole de 5 ans ou moins'\r\nWHEN\tCODE_CULTU=\t'FSG'\tTHEN\t'Autre plante fourragère sarclée d’un autre genre'\r\nWHEN\tCODE_CULTU=\t'GAI'\tTHEN\t'Gaillet'\r\nWHEN\tCODE_CULTU=\t'GES'\tTHEN\t'Cornille, dolique (y/c lablab), gesse'\r\nWHEN\tCODE_CULTU=\t'GFP'\tTHEN\t'Autre graminée fourragère pure de 5 ans ou moins'\r\nWHEN\tCODE_CULTU=\t'JO5'\tTHEN\t'Jarosse implantée pour la récolte 2015'\r\nWHEN\tCODE_CULTU=\t'JO6'\tTHEN\t'Jarosse implantée pour la récolte 2016'\r\nWHEN\tCODE_CULTU=\t'JO7'\tTHEN\t'Jarosse implantée pour la récolte 2017'\r\nWHEN\tCODE_CULTU=\t'JO8'\tTHEN\t'Jarosse implantée pour la récolte 2018'\r\nWHEN\tCODE_CULTU=\t'JOD'\tTHEN\t'Jarosse déshydratée'\r\nWHEN\tCODE_CULTU=\t'JOS'\tTHEN\t'Autre jarosse'\r\nWHEN\tCODE_CULTU=\t'LEF'\tTHEN\t'Lentille fourragère'\r\nWHEN\tCODE_CULTU=\t'LFH'\tTHEN\t'Autre lupin fourrager d’hiver'\r\nWHEN\tCODE_CULTU=\t'LFP'\tTHEN\t'Autre lupin fourrager de printemps'\r\nWHEN\tCODE_CULTU=\t'LH5'\tTHEN\t'Lupin fourrager d’hiver implanté pour la récolte 2015'\r\nWHEN\tCODE_CULTU=\t'LH6'\tTHEN\t'Lupin fourrager d’hiver implanté pour la récolte 2016'\r\nWHEN\tCODE_CULTU=\t'LH7'\tTHEN\t'Lupin fourrager d’hiver implanté pour la récolte 2017'\r\nWHEN\tCODE_CULTU=\t'LH8'\tTHEN\t'Lupin fourrager d\\'hiver implanté pour la récolte 2018'\r\nWHEN\tCODE_CULTU=\t'LO7'\tTHEN\t'Lotier implanté pour la récolte 2017'\r\nWHEN\tCODE_CULTU=\t'LO8'\tTHEN\t'Lotier implanté pour la récolte 2018'\r\nWHEN\tCODE_CULTU=\t'LOT'\tTHEN\t'Lotier, minette'\r\nWHEN\tCODE_CULTU=\t'LP5'\tTHEN\t'Lupin fourrager de printemps implanté pour la récolte 2015'\r\nWHEN\tCODE_CULTU=\t'LP6'\tTHEN\t'Lupin fourrager de printemps implanté pour la récolte 2016'\r\nWHEN\tCODE_CULTU=\t'LP7'\tTHEN\t'Lupin fourrager de printemps implanté pour la récolte 2017'\r\nWHEN\tCODE_CULTU=\t'LP8'\tTHEN\t'Lupin fourrager de printemps implanté pour la récolte 2018'\r\nWHEN\tCODE_CULTU=\t'LU5'\tTHEN\t'Luzerne implantée pour la récolte 2015'\r\nWHEN\tCODE_CULTU=\t'LU6'\tTHEN\t'Luzerne implantée pour la récolte 2016'\r\nWHEN\tCODE_CULTU=\t'LU7'\tTHEN\t'Luzerne implantée pour la récolte 2017'\r\nWHEN\tCODE_CULTU=\t'LU8'\tTHEN\t'Luzerne implantée pour la récolte 2018'\r\nWHEN\tCODE_CULTU=\t'LUD'\tTHEN\t'Luzerne déshydratée'\r\nWHEN\tCODE_CULTU=\t'LUZ'\tTHEN\t'Autre luzerne'\r\nWHEN\tCODE_CULTU=\t'MC5'\tTHEN\t'Mélange de légumineuses fourragères prépondérantes au semis implantées pour la récolte 2015 et de céréales'\r\nWHEN\tCODE_CULTU=\t'MC6'\tTHEN\t'Mélange de légumineuses fourragères prépondérantes au semis implantées pour la récolte 2016 et de céréales'\r\nWHEN\tCODE_CULTU=\t'MC7'\tTHEN\t'Mélange de légumineuses fourragères prépondérantes au semis implantées pour la récolte 2017 et de céréales'\r\nWHEN\tCODE_CULTU=\t'MC8'\tTHEN\t'Mélange de légumineuses fourragères prépondérantes implantées pour la récolte 2018 et de céréales et d’oléagineux'\r\nWHEN\tCODE_CULTU=\t'ME5'\tTHEN\t'Mélilot implanté pour la récolte 2015'\r\nWHEN\tCODE_CULTU=\t'ME6'\tTHEN\t'Mélilot implanté pour la récolte 2016'\r\nWHEN\tCODE_CULTU=\t'ME7'\tTHEN\t'Mélilot implanté pour la récolte 2017'\r\nWHEN\tCODE_CULTU=\t'ME8'\tTHEN\t'Mélilot implanté pour la récolte 2018'\r\nWHEN\tCODE_CULTU=\t'MED'\tTHEN\t'Mélilot déshydraté'\r\nWHEN\tCODE_CULTU=\t'MEL'\tTHEN\t'Autre mélilot'\r\nWHEN\tCODE_CULTU=\t'MH5'\tTHEN\t'Mélange de légumineuses fourragères prépondérantes au semis implantées pour la récolte 2015 et d’herbacées ou de graminées fourragères'\r\nWHEN\tCODE_CULTU=\t'MH6'\tTHEN\t'Mélange de légumineuses fourragères prépondérantes au semis implantées pour la récolte 2016 et d’herbacées ou de graminées fourragères'\r\nWHEN\tCODE_CULTU=\t'MH7'\tTHEN\t'Mélange de légumineuses fourragères prépondérantes au semis implantées pour la récolte 2017 et d’herbacées ou de graminées fourragères'\r\nWHEN\tCODE_CULTU=\t'MI7'\tTHEN\t'Minette implanté pour la récolte 2017'\r\nWHEN\tCODE_CULTU=\t'MI8'\tTHEN\t'Minette implanté pour la récolte 2018'\r\nWHEN\tCODE_CULTU=\t'MIN'\tTHEN\t'Minette'\r\nWHEN\tCODE_CULTU=\t'ML5'\tTHEN\t'Mélange de légumineuses fourragères implantées pour la récolte 2015 (entre elles)'\r\nWHEN\tCODE_CULTU=\t'ML6'\tTHEN\t'Mélange de légumineuses fourragères implantées pour la récolte 2016 (entre elles)'\r\nWHEN\tCODE_CULTU=\t'ML7'\tTHEN\t'Mélange de légumineuses fourragères implantées pour la récolte 2017 (entre elles)'\r\nWHEN\tCODE_CULTU=\t'ML8'\tTHEN\t'Mélange de légumineuses fourragères implantées pour la récolte 2018 (entre elles)'\r\nWHEN\tCODE_CULTU=\t'MLC'\tTHEN\t'Mélange multi-espèces avec légumineuses fourragères prépondérantes sans graminées prairiales'\r\nWHEN\tCODE_CULTU=\t'MLD'\tTHEN\t'Mélange de légumineuses déshydratées (entre elles)'\r\nWHEN\tCODE_CULTU=\t'MLF'\tTHEN\t'Mélange de légumineuses à graines ou fourragères pures'\r\nWHEN\tCODE_CULTU=\t'MLG'\tTHEN\t'Mélange de légumineuses prépondérantes et de graminées fourragères de 5 ans ou moins'\r\nWHEN\tCODE_CULTU=\t'MOH'\tTHEN\t'Moha'\r\nWHEN\tCODE_CULTU=\t'NVF'\tTHEN\t'Navet fourrager'\r\nWHEN\tCODE_CULTU=\t'PAT'\tTHEN\t'Pâturin commun de 5 ans ou moins'\r\nWHEN\tCODE_CULTU=\t'PFH'\tTHEN\t'Autre pois fourrager d’hiver'\r\nWHEN\tCODE_CULTU=\t'PFP'\tTHEN\t'Autre pois fourrager de printemps'\r\nWHEN\tCODE_CULTU=\t'PH5'\tTHEN\t'Pois fourrager d’hiver implanté pour la récolte 2015'\r\nWHEN\tCODE_CULTU=\t'PH6'\tTHEN\t'Pois fourrager d’hiver implanté pour la récolte 2016'\r\nWHEN\tCODE_CULTU=\t'PH7'\tTHEN\t'Pois fourrager d’hiver implanté pour la récolte 2017'\r\nWHEN\tCODE_CULTU=\t'PH8'\tTHEN\t'Pois fourrager d’hiver implanté pour la récolte 2018'\r\nWHEN\tCODE_CULTU=\t'PP5'\tTHEN\t'Pois fourrager de printemps implanté pour la récolte 2015'\r\nWHEN\tCODE_CULTU=\t'PP6'\tTHEN\t'Pois fourrager de printemps implanté pour la récolte 2016'\r\nWHEN\tCODE_CULTU=\t'PP7'\tTHEN\t'Pois fourrager de printemps implanté pour la récolte 2017'\r\nWHEN\tCODE_CULTU=\t'PP8'\tTHEN\t'Pois fourrager de printemps implanté pour la récolte 2018'\r\nWHEN\tCODE_CULTU=\t'RDF'\tTHEN\t'Radis fourrager'\r\nWHEN\tCODE_CULTU=\t'SA5'\tTHEN\t'Sainfoin implanté pour la récolte 2015'\r\nWHEN\tCODE_CULTU=\t'SA6'\tTHEN\t'Sainfoin implanté pour la récolte 2016'\r\nWHEN\tCODE_CULTU=\t'SA7'\tTHEN\t'Sainfoin implanté pour la récolte 2017'\r\nWHEN\tCODE_CULTU=\t'SA8'\tTHEN\t'Sainfoin implanté pour la récolte 2018'\r\nWHEN\tCODE_CULTU=\t'SAD'\tTHEN\t'Sainfoin déshydraté'\r\nWHEN\tCODE_CULTU=\t'SAI'\tTHEN\t'Sainfoin'\r\nWHEN\tCODE_CULTU=\t'SE5'\tTHEN\t'Serradelle implantée pour la récolte 2015'\r\nWHEN\tCODE_CULTU=\t'SE6'\tTHEN\t'Serradelle implantée pour la récolte 2016'\r\nWHEN\tCODE_CULTU=\t'SE7'\tTHEN\t'Serradelle implantée pour la récolte 2017'\r\nWHEN\tCODE_CULTU=\t'SE8'\tTHEN\t'Serradelle implantée pour la récolte 2018'\r\nWHEN\tCODE_CULTU=\t'SED'\tTHEN\t'Serradelle déshydratée'\r\nWHEN\tCODE_CULTU=\t'SER'\tTHEN\t'Autre serradelle'\r\nWHEN\tCODE_CULTU=\t'TR5'\tTHEN\t'Trèfle implanté pour la récolte 2015'\r\nWHEN\tCODE_CULTU=\t'TR6'\tTHEN\t'Trèfle implanté pour la récolte 2016'\r\nWHEN\tCODE_CULTU=\t'TR7'\tTHEN\t'Trèfle implanté pour la récolte 2017'\r\nWHEN\tCODE_CULTU=\t'TR8'\tTHEN\t'Trèfle implanté pour la récolte 2018'\r\nWHEN\tCODE_CULTU=\t'TRD'\tTHEN\t'Trèfle déshydraté'\r\nWHEN\tCODE_CULTU=\t'TRE'\tTHEN\t'Autre trèfle'\r\nWHEN\tCODE_CULTU=\t'VE5'\tTHEN\t'Vesce implantée pour la récolte 2015'\r\nWHEN\tCODE_CULTU=\t'VE6'\tTHEN\t'Vesce implantée pour la récolte 2016'\r\nWHEN\tCODE_CULTU=\t'VE7'\tTHEN\t'Vesce implantée pour la récolte 2017'\r\nWHEN\tCODE_CULTU=\t'VE8'\tTHEN\t'Vesce implantée pour la récolte 2018'\r\nWHEN\tCODE_CULTU=\t'VED'\tTHEN\t'Vesce déshydratée'\r\nWHEN\tCODE_CULTU=\t'VES'\tTHEN\t'Vesce, mélilot, jarosse, serradelle'\r\nWHEN\tCODE_CULTU=\t'XFE'\tTHEN\t'X-Felium de 5 ans ou moins'\r\nWHEN\tCODE_CULTU=\t'BOP'\tTHEN\t'Bois pâturé'\r\nWHEN\tCODE_CULTU=\t'SPH'\tTHEN\t'Prairie avec herbe prédominante et ressources fourragères ligneuses présentes'\r\nWHEN\tCODE_CULTU=\t'SPL'\tTHEN\t'Surface pastorale - Ressources fourragères ligneuses prédominantes'\r\nWHEN\tCODE_CULTU=\t'PPH'\tTHEN\t'Prairie de 6 ans ou plus (couvert herbacé)'\r\nWHEN\tCODE_CULTU=\t'PRL'\tTHEN\t'Prairie en rotation longue (6 ans ou plus)'\r\nWHEN\tCODE_CULTU=\t'PTR'\tTHEN\t'Prairie temporaire de moins de 5 ans et autre mélange avec graminées'\r\nWHEN\tCODE_CULTU=\t'RGA'\tTHEN\t'Ray-grass de 5 ans ou moins'\r\nWHEN\tCODE_CULTU=\t'AGR'\tTHEN\t'Agrume'\r\nWHEN\tCODE_CULTU=\t'ANA'\tTHEN\t'Ananas'\r\nWHEN\tCODE_CULTU=\t'AVO'\tTHEN\t'Avocat'\r\nWHEN\tCODE_CULTU=\t'BCA'\tTHEN\t'Banane (hors export)'\r\nWHEN\tCODE_CULTU=\t'BCF'\tTHEN\t'Banane créole (fruit et légume) - fermage'\r\nWHEN\tCODE_CULTU=\t'BCI'\tTHEN\t'Banane créole (fruit et légume) - indivision'\r\nWHEN\tCODE_CULTU=\t'BCP'\tTHEN\t'Banane créole (fruit et légume) - propriété ou faire valoir direct'\r\nWHEN\tCODE_CULTU=\t'BCR'\tTHEN\t'Banane créole (fruit et légume) - réforme foncière'\r\nWHEN\tCODE_CULTU=\t'BEA'\tTHEN\t'Banane export - autre'\r\nWHEN\tCODE_CULTU=\t'BEF'\tTHEN\t'Banane (export)'\r\nWHEN\tCODE_CULTU=\t'BEI'\tTHEN\t'Banane export - indivision'\r\nWHEN\tCODE_CULTU=\t'BEP'\tTHEN\t'Banane export - propriété ou faire valoir direct'\r\nWHEN\tCODE_CULTU=\t'BER'\tTHEN\t'Banane export - réforme foncière'\r\nWHEN\tCODE_CULTU=\t'CAC'\tTHEN\t'Café et cacao'\r\nWHEN\tCODE_CULTU=\t'CBT'\tTHEN\t'Cerise'\r\nWHEN\tCODE_CULTU=\t'PFR'\tTHEN\t'Petit fruit à baie (hors fraise)'\r\nWHEN\tCODE_CULTU=\t'PRU'\tTHEN\t'Prune (y compris mirabelle, quetsche, reine-claude, …)'\r\nWHEN\tCODE_CULTU=\t'PVT'\tTHEN\t'Pêche (y compris nectarine, brugnon)'\r\nWHEN\tCODE_CULTU=\t'PWT'\tTHEN\t'Poire'\r\nWHEN\tCODE_CULTU=\t'VGD'\tTHEN\t'Verger (DOM)'\r\nWHEN\tCODE_CULTU=\t'VRG'\tTHEN\t'Autre verger (y compris verger DOM)'\r\nWHEN\tCODE_CULTU=\t'RVI'\tTHEN\t'Restructuration du vignoble'\r\nWHEN\tCODE_CULTU=\t'VRC'\tTHEN\t'Vigne (sauf vigne rouge)'\r\nWHEN\tCODE_CULTU=\t'VRN'\tTHEN\t'Vigne : raisins de cuve non en production'\r\nWHEN\tCODE_CULTU=\t'VRT'\tTHEN\t'Vigne : raisins de table'\r\nWHEN\tCODE_CULTU=\t'CAB'\tTHEN\t'Caroube'\r\nWHEN\tCODE_CULTU=\t'CTG'\tTHEN\t'Châtaigne'\r\nWHEN\tCODE_CULTU=\t'NOS'\tTHEN\t'Noisette'\r\nWHEN\tCODE_CULTU=\t'NOX'\tTHEN\t'Noix (y compris noix de coco)'\r\nWHEN\tCODE_CULTU=\t'PIS'\tTHEN\t'Pistache'\r\nWHEN\tCODE_CULTU=\t'OLI'\tTHEN\t'Olive'\r\nWHEN\tCODE_CULTU=\t'AME'\tTHEN\t'Plantes médicinales et à parfum non pérennes (< 5 ans)'\r\nWHEN\tCODE_CULTU=\t'ANE'\tTHEN\t'Aneth'\r\nWHEN\tCODE_CULTU=\t'ANG'\tTHEN\t'Angélique'\r\nWHEN\tCODE_CULTU=\t'ANI'\tTHEN\t'Anis'\r\nWHEN\tCODE_CULTU=\t'AAR'\tTHEN\t'Plantes aromatiques herbacées non pérennes (< 5 ans) autres que persil'\r\nWHEN\tCODE_CULTU=\t'ARP'\tTHEN\t'Plante aromatique pérenne non arbustive ou arborée autre que la vanille'\r\nWHEN\tCODE_CULTU=\t'BAR'\tTHEN\t'Bardane'\r\nWHEN\tCODE_CULTU=\t'BAS'\tTHEN\t'Basilic'\r\nWHEN\tCODE_CULTU=\t'BRH'\tTHEN\t'Bourrache de 5 ans ou moins'\r\nWHEN\tCODE_CULTU=\t'BTN'\tTHEN\t'Betterave'\r\nWHEN\tCODE_CULTU=\t'CAV'\tTHEN\t'Carvi'\r\nWHEN\tCODE_CULTU=\t'CHR'\tTHEN\t'Chardon Marie'\r\nWHEN\tCODE_CULTU=\t'CIB'\tTHEN\t'Ciboulette'\r\nWHEN\tCODE_CULTU=\t'CML'\tTHEN\t'Cameline'\r\nWHEN\tCODE_CULTU=\t'CMM'\tTHEN\t'Camomille'\r\nWHEN\tCODE_CULTU=\t'CRD'\tTHEN\t'Coriandre'\r\nWHEN\tCODE_CULTU=\t'CRF'\tTHEN\t'Cerfeuil'\r\nWHEN\tCODE_CULTU=\t'CUM'\tTHEN\t'Cumin'\r\nWHEN\tCODE_CULTU=\t'CUR'\tTHEN\t'Curcuma'\r\nWHEN\tCODE_CULTU=\t'EST'\tTHEN\t'Estragon'\r\nWHEN\tCODE_CULTU=\t'FNO'\tTHEN\t'Fenouil'\r\nWHEN\tCODE_CULTU=\t'FNU'\tTHEN\t'Fenugrec'\r\nWHEN\tCODE_CULTU=\t'HBL'\tTHEN\t'Houblon'\r\nWHEN\tCODE_CULTU=\t'LAV'\tTHEN\t'Lavande et lavandin'\r\nWHEN\tCODE_CULTU=\t'MAV'\tTHEN\t'Mauve'\r\nWHEN\tCODE_CULTU=\t'MLI'\tTHEN\t'Mélisse'\r\nWHEN\tCODE_CULTU=\t'MLP'\tTHEN\t'Millepertuis'\r\nWHEN\tCODE_CULTU=\t'MOT'\tTHEN\t'Moutarde d\\'hiver'\r\nWHEN\tCODE_CULTU=\t'MRJ'\tTHEN\t'Marjolaine / Origan'\r\nWHEN\tCODE_CULTU=\t'MTH'\tTHEN\t'Menthe'\r\nWHEN\tCODE_CULTU=\t'ORT'\tTHEN\t'Ortie'\r\nWHEN\tCODE_CULTU=\t'OSE'\tTHEN\t'Oseille'\r\nWHEN\tCODE_CULTU=\t'PAR'\tTHEN\t'Plante aromatique (autre que vanille)'\r\nWHEN\tCODE_CULTU=\t'PMD'\tTHEN\t'Plante médicinale'\r\nWHEN\tCODE_CULTU=\t'PME'\tTHEN\t'Plantes médicinales pérennes (autres que arbres)'\r\nWHEN\tCODE_CULTU=\t'PPA'\tTHEN\t'Autre plante à parfum'\r\nWHEN\tCODE_CULTU=\t'PPF'\tTHEN\t'Plante à parfum (autre que géranium et vétiver)'\r\nWHEN\tCODE_CULTU=\t'PPP'\tTHEN\t'Plantes médicinales pérennes (arbres ou arbustes) sauf cassis'\r\nWHEN\tCODE_CULTU=\t'PRF'\tTHEN\t'Plantes à parfum pérennes autres que lavande et lavandin'\r\nWHEN\tCODE_CULTU=\t'PSL'\tTHEN\t'Persil'\r\nWHEN\tCODE_CULTU=\t'PSN'\tTHEN\t'Psyllium noir de Provence'\r\nWHEN\tCODE_CULTU=\t'PSY'\tTHEN\t'Plantain psyllium'\r\nWHEN\tCODE_CULTU=\t'ROM'\tTHEN\t'Romarin'\r\nWHEN\tCODE_CULTU=\t'SGE'\tTHEN\t'Sauge'\r\nWHEN\tCODE_CULTU=\t'SRI'\tTHEN\t'Sarriette'\r\nWHEN\tCODE_CULTU=\t'TAB'\tTHEN\t'Tabac'\r\nWHEN\tCODE_CULTU=\t'THY'\tTHEN\t'Thym'\r\nWHEN\tCODE_CULTU=\t'TOT'\tTHEN\t'Tomate pour transformation'\r\nWHEN\tCODE_CULTU=\t'VAL'\tTHEN\t'Valériane'\r\nWHEN\tCODE_CULTU=\t'VNB'\tTHEN\t'Vanille sous bois'\r\nWHEN\tCODE_CULTU=\t'VNL'\tTHEN\t'Vanille'\r\nWHEN\tCODE_CULTU=\t'VNV'\tTHEN\t'Vanille verte'\r\nWHEN\tCODE_CULTU=\t'YLA'\tTHEN\t'Ylang-ylang'\r\nWHEN\tCODE_CULTU=\t'AIL'\tTHEN\t'Aïl'\r\nWHEN\tCODE_CULTU=\t'ART'\tTHEN\t'Artichaut'\r\nWHEN\tCODE_CULTU=\t'AUB'\tTHEN\t'Aubergine'\r\nWHEN\tCODE_CULTU=\t'BLT'\tTHEN\t'Bleuet'\r\nWHEN\tCODE_CULTU=\t'BUR'\tTHEN\t'Bugle rampante'\r\nWHEN\tCODE_CULTU=\t'CAR'\tTHEN\t'Carotte'\r\nWHEN\tCODE_CULTU=\t'CCN'\tTHEN\t'Concombre, cornichon et courgette'\r\nWHEN\tCODE_CULTU=\t'CCT'\tTHEN\t'Courgette / Citrouille'\r\nWHEN\tCODE_CULTU=\t'CEL'\tTHEN\t'Céleri'\r\nWHEN\tCODE_CULTU=\t'CES'\tTHEN\t'Chicorée / Endive / Scarole'\r\nWHEN\tCODE_CULTU=\t'CHU'\tTHEN\t'Chou'\r\nWHEN\tCODE_CULTU=\t'CMB'\tTHEN\t'Courge musquée / Butternut'\r\nWHEN\tCODE_CULTU=\t'CRA'\tTHEN\t'Cresson alénois de 5 ans ou moins'\r\nWHEN\tCODE_CULTU=\t'CRN'\tTHEN\t'Cornille'\r\nWHEN\tCODE_CULTU=\t'CRS'\tTHEN\t'Cresson'\r\nWHEN\tCODE_CULTU=\t'CSS'\tTHEN\t'Culture sous serre hors sol'\r\nWHEN\tCODE_CULTU=\t'DOL'\tTHEN\t'Dolique'\r\nWHEN\tCODE_CULTU=\t'EPI'\tTHEN\t'Epinard, oseille et bette'\r\nWHEN\tCODE_CULTU=\t'FLA'\tTHEN\t'Autre légume ou fruit annuel'\r\nWHEN\tCODE_CULTU=\t'FLP'\tTHEN\t'Autre légume ou fruit pérenne (hors petit fruit à baie)'\r\nWHEN\tCODE_CULTU=\t'FRA'\tTHEN\t'Fraise (en pleine terre)'\r\nWHEN\tCODE_CULTU=\t'GER'\tTHEN\t'Géranium'\r\nWHEN\tCODE_CULTU=\t'HAR'\tTHEN\t'Haricot / Flageolet'\r\nWHEN\tCODE_CULTU=\t'HPC'\tTHEN\t'Horticulture ornementale'\r\nWHEN\tCODE_CULTU=\t'HSA'\tTHEN\t'Horticulture ornementale sous abri'\r\nWHEN\tCODE_CULTU=\t'LBF'\tTHEN\t'Laitue, endive et autres salades'\r\nWHEN\tCODE_CULTU=\t'LSA'\tTHEN\t'Légume sous abri'\r\nWHEN\tCODE_CULTU=\t'MAC'\tTHEN\t'Mâche'\r\nWHEN\tCODE_CULTU=\t'MDI'\tTHEN\t'Maraîchage diversifié (plusieurs espèces de fruits et légumes majoritairement non pérennes)'\r\nWHEN\tCODE_CULTU=\t'MLO'\tTHEN\t'Melon et pastèque'\r\nWHEN\tCODE_CULTU=\t'MRG'\tTHEN\t'Marguerite'\r\nWHEN\tCODE_CULTU=\t'NVT'\tTHEN\t'Navet, rutabaga et autres légumes racines (hors carotte, radis, betterave)'\r\nWHEN\tCODE_CULTU=\t'OIG'\tTHEN\t'Oignon et échalote'\r\nWHEN\tCODE_CULTU=\t'PAN'\tTHEN\t'Panais'\r\nWHEN\tCODE_CULTU=\t'PAQ'\tTHEN\t'Pâquerette'\r\nWHEN\tCODE_CULTU=\t'PAS'\tTHEN\t'Pastèque'\r\nWHEN\tCODE_CULTU=\t'PMV'\tTHEN\t'Primevère'\r\nWHEN\tCODE_CULTU=\t'POR'\tTHEN\t'Poireau'\r\nWHEN\tCODE_CULTU=\t'POT'\tTHEN\t'Potiron, citrouille et autres courges'\r\nWHEN\tCODE_CULTU=\t'PPO'\tTHEN\t'Petits pois'\r\nWHEN\tCODE_CULTU=\t'PSE'\tTHEN\t'Pensée'\r\nWHEN\tCODE_CULTU=\t'PTC'\tTHEN\t'Pomme de terre'\r\nWHEN\tCODE_CULTU=\t'PTF'\tTHEN\t'Pomme de terre féculière'\r\nWHEN\tCODE_CULTU=\t'PVP'\tTHEN\t'Poivron, piment et aubergine'\r\nWHEN\tCODE_CULTU=\t'RDI'\tTHEN\t'Radis'\r\nWHEN\tCODE_CULTU=\t'ROQ'\tTHEN\t'Roquette'\r\nWHEN\tCODE_CULTU=\t'RUT'\tTHEN\t'Rutabaga'\r\nWHEN\tCODE_CULTU=\t'SFI'\tTHEN\t'Salsifis'\r\nWHEN\tCODE_CULTU=\t'TOM'\tTHEN\t'Tomate (en pleine terre)'\r\nWHEN\tCODE_CULTU=\t'TOP'\tTHEN\t'Topinambour'\r\nWHEN\tCODE_CULTU=\t'VER'\tTHEN\t'Véronique'\r\nWHEN\tCODE_CULTU=\t'CSA'\tTHEN\t'Canne à sucre'\r\nWHEN\tCODE_CULTU=\t'CSF'\tTHEN\t'Canne à sucre - fermage'\r\nWHEN\tCODE_CULTU=\t'CSI'\tTHEN\t'Canne à sucre - indivision'\r\nWHEN\tCODE_CULTU=\t'CSP'\tTHEN\t'Canne à sucre - propriété ou faire valoir direct'\r\nWHEN\tCODE_CULTU=\t'CSR'\tTHEN\t'Canne à sucre - réforme foncière'\r\nWHEN\tCODE_CULTU=\t'ACA'\tTHEN\t'Autre culture non précisée dans la liste (admissible)'\r\nWHEN\tCODE_CULTU=\t'BFP'\tTHEN\t'Bande admissible le long d’une forêt avec production'\r\nWHEN\tCODE_CULTU=\t'BFS'\tTHEN\t'Bordure le long d\\'une forêt sans production'\r\nWHEN\tCODE_CULTU=\t'BOR'\tTHEN\t'Bordure de champ'\r\nWHEN\tCODE_CULTU=\t'BRO'\tTHEN\t'Brome de 5 ans ou moins'\r\nWHEN\tCODE_CULTU=\t'BTA'\tTHEN\t'Bande tampon'\r\nWHEN\tCODE_CULTU=\t'CAE'\tTHEN\t'Châtaigneraie entretenue par des porcins ou des petits ruminants'\r\nWHEN\tCODE_CULTU=\t'CEE'\tTHEN\t'Chênaie entretenue par des porcins ou des petits ruminants'\r\nWHEN\tCODE_CULTU=\t'CNE'\tTHEN\t'Chênaie non entretenue par des porcins ou des petits ruminants'\r\nWHEN\tCODE_CULTU=\t'CID'\tTHEN\t'Cultures conduites en inter-rangs (bandes de cultures différentes)  - 2 cultures représentant chacune plus de 25  %'\r\nWHEN\tCODE_CULTU=\t'CIT'\tTHEN\t'Cultures conduites en inter-rangs (bandes de cultures différentes)  - 3 cultures représentant chacune plus de 25  %'\r\nWHEN\tCODE_CULTU=\t'CUA'\tTHEN\t'Culture sous abattis'\r\nWHEN\tCODE_CULTU=\t'GRA'\tTHEN\t'Graminée pure exclusivement pour gazon ou pour production de semences certifiées'\r\nWHEN\tCODE_CULTU=\t'MCT'\tTHEN\t'Miscanthus'\r\nWHEN\tCODE_CULTU=\t'MPA'\tTHEN\t'Autre mélange de plantes fixant l’azote'\r\nWHEN\tCODE_CULTU=\t'MRS'\tTHEN\t'Marais salants'\r\nWHEN\tCODE_CULTU=\t'MSW'\tTHEN\t'Culture pérenne à forte biomasse (miscanthus, switchgrass, silphie, canne fourragère, …)'\r\nWHEN\tCODE_CULTU=\t'NYG'\tTHEN\t'Nyger'\r\nWHEN\tCODE_CULTU=\t'PCL'\tTHEN\t'Phacélie de 5 ans ou moins'\r\nWHEN\tCODE_CULTU=\t'PEP'\tTHEN\t'Pépinière (plants laissés en terre plus d’un an)'\r\nWHEN\tCODE_CULTU=\t'PEV'\tTHEN\t'Pépinière (plants laissés en terre moins d’un an)'\r\nWHEN\tCODE_CULTU=\t'ROS'\tTHEN\t'Roselière'\r\nWHEN\tCODE_CULTU=\t'SAG'\tTHEN\t'Roselière (récolte de sagnes)'\r\nWHEN\tCODE_CULTU=\t'SBO'\tTHEN\t'Boisement aidé d\\'une surface agricole'\r\nWHEN\tCODE_CULTU=\t'SHD'\tTHEN\t'Surfaces hautement diversifiées (DOM)'\r\nWHEN\tCODE_CULTU=\t'SIN'\tTHEN\t'Surface pastorale ou parcours non utilisé l\\'année en cours'\r\nWHEN\tCODE_CULTU=\t'SNA'\tTHEN\t'Surface non agricole non visible sur l’orthophotographie'\r\nWHEN\tCODE_CULTU=\t'SNE'\tTHEN\t'Surface agricole temporairement non admissible, autre que surface pâturable'\r\nWHEN\tCODE_CULTU=\t'SNU'\tTHEN\t'Parc d\\'élevage de monogastriques avec couvert dégradé, voire sol nu'\r\nWHEN\tCODE_CULTU=\t'TBT'\tTHEN\t'Tubercule tropical'\r\nWHEN\tCODE_CULTU=\t'TCR'\tTHEN\t'Taillis à courte rotation'\r\nWHEN\tCODE_CULTU=\t'TRU'\tTHEN\t'Truffière (chênaie de plants mycorhizés)'\r\nWHEN\tCODE_CULTU=\t'VET'\tTHEN\t'Vétiver'\r\nWHEN\tCODE_CULTU=\t'ZZZ'\tTHEN\t'Culture inconnue'\r\nWHEN\tCODE_CULTU=\t'MLS'\tTHEN\t'Mélange de légumineuses non fourragères prépondérantes et de céréales et/ou d\\'oléagineux'\r\nWHEN\tCODE_CULTU=\t'ACP'\tTHEN\t'Autre culture pérenne et jachère dans les bananeraies'\r\nELSE 'Autre'\r\n\r\nEND",
            'INPUT': outputs['AjouterUnChampLib_cultuRpg']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampLib_cultuRpg'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(214)
        if feedback.isCanceled():
            return {}

        # Joindre les attributs par valeur de champ Reserves de Biosphere
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': QgsExpression("'ID_MNHN'").evaluate(),
            'FIELDS_TO_COPY': QgsExpression("'distance'").evaluate(),
            'FIELD_2': QgsExpression("'ID_MNHN'").evaluate(),
            'INPUT': outputs['CalculatriceDeChampTamponReservesDeBiosphere']['OUTPUT'],
            'INPUT_2': outputs['LigneLaPlusCourteEntreLesEntitsReservesDeBiosphere']['OUTPUT'],
            'METHOD': 1,  # Prendre uniquement les attributs de la première entité correspondante (un à un)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoindreLesAttributsParValeurDeChampReservesDeBiosphere'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(215)
        if feedback.isCanceled():
            return {}

        # Conserver le champ code et sum zone etude
        alg_params = {
            'FIELDS': ['code_18','sum'],
            'INPUT': outputs['StatistiquesParCode_18ZoneEtudeTableurEnSortie']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ConserverLeChampCodeEtSumZoneEtude'] = processing.run('native:retainfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(216)
        if feedback.isCanceled():
            return {}

        # Renommer le champ sum zone etude
        alg_params = {
            'FIELD': 'sum',
            'INPUT': outputs['ConserverLeChampCodeEtSumZoneEtude']['OUTPUT'],
            'NEW_NAME': 'surface_ha',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenommerLeChampSumZoneEtude'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(217)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ tampon ZNIEFF1
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Tampon',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': " @quelle_est_la_valeur_du_tampon_de_recherche_que_vous_souhaitez_en_km_pour_les_zonages_despaces_naturels_ ||' km'",
            'INPUT': outputs['RparerLesGomtriesZnieff1']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampTamponZnieff1'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(218)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation sites patrimoniaux remarquables
        alg_params = {
            'INPUT': QgsExpression("if (@utiliser_la_couche_sites_patrimoniaux_remarquables_ =0,\r\n'R:\\\\SIG\\\\01_Vecteur\\\\Milieu_humain\\\\ATLAS DU PATRIMOINE\\\\Atlas_FRANCE\\\\SitesPatrimoniauxRemarquables_France.shp',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\sitesPatrimoniaux_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['Tampon5km']['OUTPUT'],
            'PREDICATE': [0,4],  # intersecte,touche
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationSitesPatrimoniauxRemarquables'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(219)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source Hydroecoregions
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_hydroecoregions_ =0 THEN 'https://services.sandre.eaufrance.fr/geo/sandre  - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_hydroecoregions_=1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND\r\n\r\n\r\n\r\n",
            'INPUT': outputs['CalculatriceDeChampNomher1']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\hydroecoregions.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceHydroecoregions'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(220)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ Orientation stationsMeteo
        alg_params = {
            'FIELD_LENGTH': 50,
            'FIELD_NAME': 'Orientation',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN x($geometry) <   @Reprojeter_couche_zone_etude_en_2154_OUTPUT_maxx   AND y($geometry) <   @Reprojeter_couche_zone_etude_en_2154_OUTPUT_maxy \r\nTHEN 'Sud-Ouest'\r\nWHEN x($geometry) > @Reprojeter_couche_zone_etude_en_2154_OUTPUT_maxx AND y($geometry) < @Reprojeter_couche_zone_etude_en_2154_OUTPUT_maxy \r\nTHEN 'Sud-Est'\r\nWHEN x($geometry) < @Reprojeter_couche_zone_etude_en_2154_OUTPUT_maxx AND y($geometry) > @Reprojeter_couche_zone_etude_en_2154_OUTPUT_maxy \r\nTHEN 'Nord-Ouest'\r\nWHEN x($geometry) > @Reprojeter_couche_zone_etude_en_2154_OUTPUT_maxx AND y($geometry) > @Reprojeter_couche_zone_etude_en_2154_OUTPUT_maxy  \r\nTHEN 'Nord-Est'\r\nELSE 'Indéterminé'\r\nEND",
            'INPUT': outputs['JoindreLesAttributsParValeurDeChampStationsmeteo']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampOrientationStationsmeteo'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(221)
        if feedback.isCanceled():
            return {}

        # Tampon 10km
        alg_params = {
            'DISSOLVE': True,
            'DISTANCE': 10000,
            'END_CAP_STYLE': 0,  # Rond
            'INPUT': outputs['CalculatriceDeChampNomprojet_zoneetudeEmprise']['OUTPUT'],
            'JOIN_STYLE': 0,  # Rond
            'MITER_LIMIT': 2,
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\Tampon_10km.gpkg'").evaluate(),
            'SEGMENTS': 5,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Tampon10km'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(222)
        if feedback.isCanceled():
            return {}

        # Reprojeter une couche en 2154 communes 40km
        alg_params = {
            'CONVERT_CURVED_GEOMETRIES': False,
            'INPUT': outputs['ExtraireParLocalisationCommunes40Km']['OUTPUT'],
            'OPERATION': None,
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:2154'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojeterUneCoucheEn2154Communes40km'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(223)
        if feedback.isCanceled():
            return {}

        # Ajouter un champ libelle1 zone etude avant regroupement
        alg_params = {
            'FIELD_ALIAS': None,
            'FIELD_COMMENT': None,
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'libelle1',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'INPUT': outputs['ConserverLeChampCodeEtArea_haClc_clip_zoneEtude']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AjouterUnChampLibelle1ZoneEtudeAvantRegroupement'] = processing.run('native:addfieldtoattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(224)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source SIC
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_sic_ =0 THEN 'https://ws.carmencarto.fr/WFS/119/fxx_inpn - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_sic_ =1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND",
            'INPUT': outputs['JoindreLesAttributsParValeurDeChampSic']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\SIC_intersect.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceSic'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(225)
        if feedback.isCanceled():
            return {}

        # Joindre les attributs par valeur de champ Ramsar
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': QgsExpression("'ID_MNHN'").evaluate(),
            'FIELDS_TO_COPY': QgsExpression("'distance'").evaluate(),
            'FIELD_2': QgsExpression("'ID_MNHN'").evaluate(),
            'INPUT': outputs['CalculatriceDeChampTamponRamsar']['OUTPUT'],
            'INPUT_2': outputs['LigneLaPlusCourteEntreLesEntitsRamsar']['OUTPUT'],
            'METHOD': 1,  # Prendre uniquement les attributs de la première entité correspondante (un à un)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoindreLesAttributsParValeurDeChampRamsar'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(226)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source rose des vents IOWA
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN     @utiliser_la_couche_rose_des_vents_iowa_2 =0 THEN 'source : www.mesonet.agron.iastate.edu / NCA Environnement (stationsIOWAroseDesVents)'\r\n\r\nWHEN   @utiliser_la_couche_rose_des_vents_iowa_2 =1 THEN '[Refus de l\\'utilisateur]'\r\nEND\r\n",
            'INPUT': outputs['JoindreLesAttributsParValeurDeChampRoseDesVentsIowa']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\roseDesVentsIOWA.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceRoseDesVentsIowa'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(227)
        if feedback.isCanceled():
            return {}

        # Ligne la plus courte entre les entités APPB
        alg_params = {
            'DESTINATION': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'DISTANCE': None,
            'METHOD': 0,  # Distance to Nearest Point on feature
            'NEIGHBORS': 1,
            'SOURCE': outputs['RparerLesGomtriesAppb']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['LigneLaPlusCourteEntreLesEntitsAppb'] = processing.run('native:shortestline', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(228)
        if feedback.isCanceled():
            return {}

        # Ligne la plus courte entre les entités communes 40 km
        alg_params = {
            'DESTINATION': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'DISTANCE': None,
            'METHOD': 0,  # Distance to Nearest Point on feature
            'NEIGHBORS': 1,
            'SOURCE': outputs['ReprojeterUneCoucheEn2154Communes40km']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['LigneLaPlusCourteEntreLesEntitsCommunes40Km'] = processing.run('native:shortestline', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(229)
        if feedback.isCanceled():
            return {}

        # Ligne la plus courte entre les entités Pacrs Nationaux
        alg_params = {
            'DESTINATION': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'DISTANCE': None,
            'METHOD': 0,  # Distance to Nearest Point on feature
            'NEIGHBORS': 1,
            'SOURCE': outputs['RparerLesGomtriesParcsNationaux']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['LigneLaPlusCourteEntreLesEntitsPacrsNationaux'] = processing.run('native:shortestline', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(230)
        if feedback.isCanceled():
            return {}

        # Reprojeter une couche en 2154 cavites souterraines
        alg_params = {
            'CONVERT_CURVED_GEOMETRIES': False,
            'INPUT': outputs['CalculatriceDeChampTamponCavitesSouterraines']['OUTPUT'],
            'OPERATION': None,
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:2154'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojeterUneCoucheEn2154CavitesSouterraines'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(231)
        if feedback.isCanceled():
            return {}

        # Couper couche géologie siteEtude
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_couches_gologiques_ =0,\r\n'R:\\\\SIG\\\\01_Vecteur\\\\Milieu_physique\\\\Cartes_géologiques_50000\\\\GEO050K_HARM_France_S_FGEOL_2154.shp',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\geologie_vide.gpkg')").evaluate(),
            'OVERLAY': outputs['Tampon5km']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CouperCoucheGologieSiteetude'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(232)
        if feedback.isCanceled():
            return {}

        # Ligne la plus courte entre les entités Reserves Biologiques
        alg_params = {
            'DESTINATION': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'DISTANCE': None,
            'METHOD': 0,  # Distance to Nearest Point on feature
            'NEIGHBORS': 1,
            'SOURCE': outputs['RparerLesGomtriesReserveBiologique']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['LigneLaPlusCourteEntreLesEntitsReservesBiologiques'] = processing.run('native:shortestline', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(233)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source RNR
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_rnr_ =0 THEN 'https://ws.carmencarto.fr/WFS/119/fxx_inpn - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_rnr_ =1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND",
            'INPUT': outputs['JoindreLesAttributsParValeurDeChampRnr']['OUTPUT'],
            'OUTPUT': QgsExpression("@localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\ReservesRegionales_intersect.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceRnr'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(234)
        if feedback.isCanceled():
            return {}

        # Ligne la plus courte entre les entités perimetresMH
        alg_params = {
            'DESTINATION': parameters['veuillez_slectionner_la_couche_de_la_zone_dtude_'],
            'DISTANCE': None,
            'METHOD': 0,  # Distance to Nearest Point on feature
            'NEIGHBORS': 1,
            'SOURCE': outputs['CalculatriceDeChampFidMh']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['LigneLaPlusCourteEntreLesEntitsPerimetresmh'] = processing.run('native:shortestline', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(235)
        if feedback.isCanceled():
            return {}

        # Joindre les attributs par valeur de champ APHabitatsNaturels
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': QgsExpression("'ID_MNHN'").evaluate(),
            'FIELDS_TO_COPY': QgsExpression("'distance'").evaluate(),
            'FIELD_2': QgsExpression("'ID_MNHN'").evaluate(),
            'INPUT': outputs['CalculatriceDeChampTamponAphabitatsnaturels']['OUTPUT'],
            'INPUT_2': outputs['LigneLaPlusCourteEntreLesEntitsAphabitatsnaturels']['OUTPUT'],
            'METHOD': 1,  # Prendre uniquement les attributs de la première entité correspondante (un à un)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoindreLesAttributsParValeurDeChampAphabitatsnaturels'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(236)
        if feedback.isCanceled():
            return {}

        # Ligne la plus courte entre les entités pnr
        alg_params = {
            'DESTINATION': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'DISTANCE': None,
            'METHOD': 0,  # Distance to Nearest Point on feature
            'NEIGHBORS': 1,
            'SOURCE': outputs['RparerLesGomtriesPnr']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['LigneLaPlusCourteEntreLesEntitsPnr'] = processing.run('native:shortestline', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(237)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation sites classes inscrits 5 km
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_la_couche_sites_classes_inscrits_=0,\r\n'R:\\\\SIG\\\\01_Vecteur\\\\Milieu_humain\\\\ATLAS DU PATRIMOINE\\\\Atlas_FRANCE\\\\sitesClassesInscrits_FRANCE.shp',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\sitesClassesInscrits_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['Tampon5km']['OUTPUT'],
            'PREDICATE': [0,4],  # intersecte,touche
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationSitesClassesInscrits5Km'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(238)
        if feedback.isCanceled():
            return {}

        # Joindre les attributs par valeur de champ Parcs Nationaux
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': QgsExpression("'ID_MNHN'").evaluate(),
            'FIELDS_TO_COPY': QgsExpression("'distance'").evaluate(),
            'FIELD_2': QgsExpression("'ID_MNHN'").evaluate(),
            'INPUT': outputs['CalculatriceDeChampTamponParcsNationaux']['OUTPUT'],
            'INPUT_2': outputs['LigneLaPlusCourteEntreLesEntitsPacrsNationaux']['OUTPUT'],
            'METHOD': 1,  # Prendre uniquement les attributs de la première entité correspondante (un à un)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoindreLesAttributsParValeurDeChampParcsNationaux'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(239)
        if feedback.isCanceled():
            return {}

        # Ajouter un champ libelle1 zone etude
        alg_params = {
            'FIELD_ALIAS': None,
            'FIELD_COMMENT': None,
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'libelle1',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'INPUT': outputs['RenommerLeChampSumZoneEtude']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AjouterUnChampLibelle1ZoneEtude'] = processing.run('native:addfieldtoattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(240)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ fid sites archéologiques
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'fid',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Entier (32bit)
            'FORMULA': '@id',
            'INPUT': outputs['ExtraireParLocalisationSitesArchologiques5km']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampFidSitesArchologiques'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(241)
        if feedback.isCanceled():
            return {}

        # Joindre les attributs par valeur de champ Reserves Biologiques
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': QgsExpression("'ID_MNHN'").evaluate(),
            'FIELDS_TO_COPY': QgsExpression("'distance'").evaluate(),
            'FIELD_2': QgsExpression("'ID_MNHN'").evaluate(),
            'INPUT': outputs['CalculatriceDeChampTamponReserveBiologique']['OUTPUT'],
            'INPUT_2': outputs['LigneLaPlusCourteEntreLesEntitsReservesBiologiques']['OUTPUT'],
            'METHOD': 1,  # Prendre uniquement les attributs de la première entité correspondante (un à un)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoindreLesAttributsParValeurDeChampReservesBiologiques'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(242)
        if feedback.isCanceled():
            return {}

        # Joindre les attributs par valeur de champ ZICO
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': QgsExpression("'ID_SPN'").evaluate(),
            'FIELDS_TO_COPY': QgsExpression("'distance'").evaluate(),
            'FIELD_2': QgsExpression("'ID_SPN'").evaluate(),
            'INPUT': outputs['CalculatriceDeChampTamponZico']['OUTPUT'],
            'INPUT_2': outputs['LigneLaPlusCourteEntreLesEntitsZico']['OUTPUT'],
            'METHOD': 1,  # Prendre uniquement les attributs de la première entité correspondante (un à un)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoindreLesAttributsParValeurDeChampZico'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(243)
        if feedback.isCanceled():
            return {}

        # Joindre les attributs par valeur de champ perimetres MH
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': QgsExpression("'fid'").evaluate(),
            'FIELDS_TO_COPY': QgsExpression("'distance'").evaluate(),
            'FIELD_2': QgsExpression("'fid'").evaluate(),
            'INPUT': outputs['CalculatriceDeChampFidMh']['OUTPUT'],
            'INPUT_2': outputs['LigneLaPlusCourteEntreLesEntitsPerimetresmh']['OUTPUT'],
            'METHOD': 1,  # Prendre uniquement les attributs de la première entité correspondante (un à un)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoindreLesAttributsParValeurDeChampPerimetresMh'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(244)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ tampon APPB
        alg_params = {
            'FIELD_LENGTH': 100,
            'FIELD_NAME': 'Tampon',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': " @quelle_est_la_valeur_du_tampon_de_recherche_que_vous_souhaitez_en_km_pour_les_zonages_despaces_naturels_ ||' km'",
            'INPUT': outputs['RparerLesGomtriesAppb']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampTamponAppb'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(245)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source Contexte Piscicole
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_contexte_piscicole_ =0 THEN 'https://services.sandre.eaufrance.fr/geo/sandre - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_contexte_piscicole_ =1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND\r\n\r\n",
            'INPUT': outputs['CalculatriceDeChampArea_haContextePisicicoleZoneEtude']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\synthese_contextepiscicole.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceContextePiscicole'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(246)
        if feedback.isCanceled():
            return {}

        # Joindre les attributs par valeur de champ APPB
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': QgsExpression("'ID_MNHN'").evaluate(),
            'FIELDS_TO_COPY': QgsExpression("'distance'").evaluate(),
            'FIELD_2': QgsExpression("'ID_MNHN'").evaluate(),
            'INPUT': outputs['CalculatriceDeChampTamponAppb']['OUTPUT'],
            'INPUT_2': outputs['LigneLaPlusCourteEntreLesEntitsAppb']['OUTPUT'],
            'METHOD': 1,  # Prendre uniquement les attributs de la première entité correspondante (un à un)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoindreLesAttributsParValeurDeChampAppb'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(247)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source Parcs Nationaux
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_parcs_nationaux_ =0 THEN 'https://ws.carmencarto.fr/WFS/119/fxx_inpn - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_parcs_nationaux_ =1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND",
            'INPUT': outputs['JoindreLesAttributsParValeurDeChampParcsNationaux']['OUTPUT'],
            'OUTPUT': QgsExpression("@localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\parcsNationaux_intersect.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceParcsNationaux'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(248)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source BSS
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': 'CASE\r\nWHEN      @utiliser_la_couche_des_points_bss_  =0 THEN \'source : https://www.geocatalogue.fr/geonetwork/srv/fre/catalog.search#/metadata/BR_BSS_BAA / extraction du : \'||"datExtracNCA"\r\n\r\nWHEN   @utiliser_la_couche_des_points_bss_ =1 THEN \'[Refus de l\\\'utilisateur]\'\r\nEND',
            'INPUT': outputs['JoindreLesAttributsParValeurDeChampBss']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\pointsBSS_1km.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceBss'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(249)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source ZICO
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_zico_ =0 THEN 'https://ws.carmencarto.fr/WFS/119/fxx_inpn - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_zico_ =1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND",
            'INPUT': outputs['JoindreLesAttributsParValeurDeChampZico']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\zico_intersect.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceZico'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(250)
        if feedback.isCanceled():
            return {}

        # Joindre les attributs par valeur de champ stations débit
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': QgsExpression("'CdStationHydro'").evaluate(),
            'FIELDS_TO_COPY': QgsExpression("'distance'").evaluate(),
            'FIELD_2': QgsExpression("'CdStationHydro'").evaluate(),
            'INPUT': outputs['ReprojeterUneCoucheEn2154StationsDbit']['OUTPUT'],
            'INPUT_2': outputs['LigneLaPlusCourteEntreLesEntitsStationsDbit']['OUTPUT'],
            'METHOD': 1,  # Prendre uniquement les attributs de la première entité correspondante (un à un)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoindreLesAttributsParValeurDeChampStationsDbit'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(251)
        if feedback.isCanceled():
            return {}

        # Joindre les attributs par localisation Topo zone etude
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['AjouterUnChampNomprojetLaCoucheZoneEtude']['OUTPUT'],
            'JOIN': outputs['RenommerLeChamp_maxEnAlt_max']['OUTPUT'],
            'JOIN_FIELDS': ['Alt_moy','Alt_min','Alt_max'],
            'METHOD': 1,  # Prendre uniquement les attributs de la première entité correspondante (un à un)
            'PREDICATE': [2],  # égal
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoindreLesAttributsParLocalisationTopoZoneEtude'] = processing.run('native:joinattributesbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(252)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source Zonages Cartes Communales
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_zonages_cartes_communales_ =0 THEN 'https://data.geopf.fr/wfs/ows - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_zonages_cartes_communales_=1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n",
            'INPUT': outputs['CalculatriceDeChampLiendocumentZonagesCartesCommunales']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\ZonesCartesCommunales_intersect.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceZonagesCartesCommunales'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(253)
        if feedback.isCanceled():
            return {}

        # Joindre les attributs par valeur de champ communes 40 km
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': QgsExpression("'code_insee'").evaluate(),
            'FIELDS_TO_COPY': QgsExpression("'distance'").evaluate(),
            'FIELD_2': QgsExpression("'code_insee'").evaluate(),
            'INPUT': outputs['ReprojeterUneCoucheEn2154Communes40km']['OUTPUT'],
            'INPUT_2': outputs['LigneLaPlusCourteEntreLesEntitsCommunes40Km']['OUTPUT'],
            'METHOD': 1,  # Prendre uniquement les attributs de la première entité correspondante (un à un)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoindreLesAttributsParValeurDeChampCommunes40Km'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(254)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ fid sites classés inscrits
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'fid',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Entier (32bit)
            'FORMULA': '@id',
            'INPUT': outputs['ExtraireParLocalisationSitesClassesInscrits5Km']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampFidSitesClasssInscrits'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(255)
        if feedback.isCanceled():
            return {}

        # Joindre les attributs par valeur de champ stations qualité
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': QgsExpression("'CdStationMesureEauxSurface'").evaluate(),
            'FIELDS_TO_COPY': QgsExpression("'distance'").evaluate(),
            'FIELD_2': QgsExpression("'CdStationMesureEauxSurface'").evaluate(),
            'INPUT': outputs['ReprojeterUneCoucheEn2154StationsQualit']['OUTPUT'],
            'INPUT_2': outputs['LigneLaPlusCourteEntreLesEntitsStationsQualit']['OUTPUT'],
            'METHOD': 1,  # Prendre uniquement les attributs de la première entité correspondante (un à un)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoindreLesAttributsParValeurDeChampStationsQualit'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(256)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ lienLocaGPU Zonages PLU
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'lienLocaGPU',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "to_string(attribute( get_feature(   @Calculatrice_de_champ_lien4326_OUTPUT   , 'idUnique', 1),'lien4326'))\r\n",
            'INPUT': outputs['ExtraireParLocalisationZonagesPlu']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampLienlocagpuZonagesPlu'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(257)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ fid sites patrimoniaux remarquables
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'fid',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Entier (32bit)
            'FORMULA': '@id',
            'INPUT': outputs['ExtraireParLocalisationSitesPatrimoniauxRemarquables']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampFidSitesPatrimoniauxRemarquables'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(258)
        if feedback.isCanceled():
            return {}

        # Ligne la plus courte entre les entités cavités souterraines
        alg_params = {
            'DESTINATION': outputs['ReprojeterCoucheZoneEtudeEn2154']['OUTPUT'],
            'DISTANCE': None,
            'METHOD': 0,  # Distance to Nearest Point on feature
            'NEIGHBORS': 1,
            'SOURCE': outputs['ReprojeterUneCoucheEn2154CavitesSouterraines']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['LigneLaPlusCourteEntreLesEntitsCavitsSouterraines'] = processing.run('native:shortestline', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(259)
        if feedback.isCanceled():
            return {}

        # Ajouter un champ COD_GROUP RPG
        alg_params = {
            'FIELD_ALIAS': None,
            'FIELD_COMMENT': None,
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'COD_GROUP',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'INPUT': outputs['CalculatriceDeChampLib_cultuRpg']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AjouterUnChampCod_groupRpg'] = processing.run('native:addfieldtoattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(260)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source Reserves Biologiques
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_reserve_biologique_ =0 THEN 'https://ws.carmencarto.fr/WFS/119/fxx_inpn - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_reserve_biologique_ =1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND",
            'INPUT': outputs['JoindreLesAttributsParValeurDeChampReservesBiologiques']['OUTPUT'],
            'OUTPUT': QgsExpression("@localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\ReservesBiologiques_intersect.gpkg'\n").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceReservesBiologiques'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(261)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ  source stationsMeteo
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_la_couche_des_stations_meteo_ =0 THEN 'source : Meteo France / NCA Environnement (Stations_Meteorologiques)'\r\nWHEN @utiliser_la_couche_des_stations_meteo_=1 THEN '[Refus de l\\'utilisateur]'\r\nEND\r\n",
            'INPUT': outputs['CalculatriceDeChampOrientationStationsmeteo']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\stationsMeteo.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceStationsmeteo'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(262)
        if feedback.isCanceled():
            return {}

        # Joindre les attributs par valeur de champ cavites souterraines
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': QgsExpression("'gid'").evaluate(),
            'FIELDS_TO_COPY': QgsExpression("'distance'").evaluate(),
            'FIELD_2': QgsExpression("'gid'").evaluate(),
            'INPUT': outputs['ReprojeterUneCoucheEn2154CavitesSouterraines']['OUTPUT'],
            'INPUT_2': outputs['LigneLaPlusCourteEntreLesEntitsCavitsSouterraines']['OUTPUT'],
            'METHOD': 1,  # Prendre uniquement les attributs de la première entité correspondante (un à un)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoindreLesAttributsParValeurDeChampCavitesSouterraines'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(263)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source APPB
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_appb_ =0 THEN 'https://ws.carmencarto.fr/WFS/119/fxx_inpn - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_appb_ =1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND",
            'INPUT': outputs['JoindreLesAttributsParValeurDeChampAppb']['OUTPUT'],
            'OUTPUT': QgsExpression("@localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\APPB_intersect.gpkg'\n").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceAppb'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(264)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ libelle1 zone etude
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'libelle1',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': 'CASE \r\n\r\nWHEN "code_18"= 111 THEN \'Territoires artificialisés\'\r\nWHEN "code_18"= 112 THEN \'Territoires artificialisés\'\r\nWHEN "code_18"= 121 THEN \'Territoires artificialisés\'\r\nWHEN "code_18"= 122 THEN \'Territoires artificialisés\'\r\nWHEN "code_18"= 123 THEN \'Territoires artificialisés\'\r\nWHEN "code_18"= 124 THEN \'Territoires artificialisés\'\r\nWHEN "code_18"= 131 THEN \'Territoires artificialisés\'\r\nWHEN "code_18"= 132 THEN \'Territoires artificialisés\'\r\nWHEN "code_18"= 133 THEN \'Territoires artificialisés\'\r\nWHEN "code_18"= 141 THEN \'Territoires artificialisés\'\r\nWHEN "code_18"= 142 THEN \'Territoires artificialisés\'\r\nWHEN "code_18"= 211 THEN \'Territoires agricoles\'\r\nWHEN "code_18"= 212 THEN \'Territoires agricoles\'\r\nWHEN "code_18"= 213 THEN \'Territoires agricoles\'\r\nWHEN "code_18"= 221 THEN \'Territoires agricoles\'\r\nWHEN "code_18"= 222 THEN \'Territoires agricoles\'\r\nWHEN "code_18"= 223 THEN \'Territoires agricoles\'\r\nWHEN "code_18"= 231 THEN \'Territoires agricoles\'\r\nWHEN "code_18"= 241 THEN \'Territoires agricoles\'\r\nWHEN "code_18"= 242 THEN \'Territoires agricoles\'\r\nWHEN "code_18"= 243 THEN \'Territoires agricoles\'\r\nWHEN "code_18"= 244 THEN \'Territoires agricoles\'\r\nWHEN "code_18"= 311 THEN \'Forêts et milieux semi-naturels\'\r\nWHEN "code_18"= 312 THEN \'Forêts et milieux semi-naturels\'\r\nWHEN "code_18"= 313 THEN \'Forêts et milieux semi-naturels\'\r\nWHEN "code_18"= 321 THEN \'Forêts et milieux semi-naturels\'\r\nWHEN "code_18"= 322 THEN \'Forêts et milieux semi-naturels\'\r\nWHEN "code_18"= 323 THEN \'Forêts et milieux semi-naturels\'\r\nWHEN "code_18"= 324 THEN \'Forêts et milieux semi-naturels\'\r\nWHEN "code_18"= 331 THEN \'Forêts et milieux semi-naturels\'\r\nWHEN "code_18"= 332 THEN \'Forêts et milieux semi-naturels\'\r\nWHEN "code_18"= 333 THEN \'Forêts et milieux semi-naturels\'\r\nWHEN "code_18"= 334 THEN \'Forêts et milieux semi-naturels\'\r\nWHEN "code_18"= 335 THEN \'Forêts et milieux semi-naturels\'\r\nWHEN "code_18"= 411 THEN \'Zones humides\'\r\nWHEN "code_18"= 412 THEN \'Zones humides\'\r\nWHEN "code_18"= 421 THEN \'Zones humides\'\r\nWHEN "code_18"= 422 THEN \'Zones humides\'\r\nWHEN "code_18"= 423 THEN \'Zones humides\'\r\nWHEN "code_18"= 511 THEN \'Surfaces en eau\'\r\nWHEN "code_18"= 512 THEN \'Surfaces en eau\'\r\nWHEN "code_18"= 521 THEN \'Surfaces en eau\'\r\nWHEN "code_18"= 522 THEN \'Surfaces en eau\'\r\nWHEN "code_18"= 523 THEN \'Surfaces en eau\'\r\n\r\n\r\nEND',
            'INPUT': outputs['AjouterUnChampLibelle1ZoneEtude']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampLibelle1ZoneEtude'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(265)
        if feedback.isCanceled():
            return {}

        # Joindre les attributs par valeur de champ ZNIEFF2
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': QgsExpression("'ID_MNHN'").evaluate(),
            'FIELDS_TO_COPY': QgsExpression("'distance'").evaluate(),
            'FIELD_2': QgsExpression("'ID_MNHN'").evaluate(),
            'INPUT': outputs['CalculatriceDeChampTamponZnieff2']['OUTPUT'],
            'INPUT_2': outputs['LigneLaPlusCourteEntreLesEntitsZnieff2']['OUTPUT'],
            'METHOD': 1,  # Prendre uniquement les attributs de la première entité correspondante (un à un)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoindreLesAttributsParValeurDeChampZnieff2'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(266)
        if feedback.isCanceled():
            return {}

        # Joindre les attributs par valeur de champ ZNIEFF1
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': QgsExpression("'ID_MNHN'").evaluate(),
            'FIELDS_TO_COPY': QgsExpression("'distance'").evaluate(),
            'FIELD_2': QgsExpression("'ID_MNHN'").evaluate(),
            'INPUT': outputs['CalculatriceDeChampTamponZnieff1']['OUTPUT'],
            'INPUT_2': outputs['LigneLaPlusCourteEntreLesEntitsZnieff1']['OUTPUT'],
            'METHOD': 1,  # Prendre uniquement les attributs de la première entité correspondante (un à un)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoindreLesAttributsParValeurDeChampZnieff1'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(267)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source Reserve de Biosphere
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_reserve_biosphre_ =0 THEN 'https://ws.carmencarto.fr/WFS/119/fxx_inpn - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_reserve_biosphre_ =1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND",
            'INPUT': outputs['JoindreLesAttributsParValeurDeChampReservesDeBiosphere']['OUTPUT'],
            'OUTPUT': QgsExpression("@localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\ReservesBiosphere_intersect.gpkg'\n").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceReserveDeBiosphere'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(268)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source stations débit
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_stations_dbit_ =0 THEN 'https://services.sandre.eaufrance.fr/geo/sandre  - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_stations_dbit_ =1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND\r\n\r\n\r\n",
            'INPUT': outputs['JoindreLesAttributsParValeurDeChampStationsDbit']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\stationsDebit_intra_tampon.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceStationsDbit'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(269)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source Ramsar
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_ramsar_ =0 THEN 'https://ws.carmencarto.fr/WFS/119/fxx_inpn - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_ramsar_ =1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND",
            'INPUT': outputs['JoindreLesAttributsParValeurDeChampRamsar']['OUTPUT'],
            'OUTPUT': QgsExpression("@localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\Ramsar_intersect.gpkg'\n").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceRamsar'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(270)
        if feedback.isCanceled():
            return {}

        # Ligne la plus courte entre les entités sites archéologiques
        alg_params = {
            'DESTINATION': parameters['veuillez_slectionner_la_couche_de_la_zone_dtude_'],
            'DISTANCE': None,
            'METHOD': 0,  # Distance to Nearest Point on feature
            'NEIGHBORS': 1,
            'SOURCE': outputs['CalculatriceDeChampFidSitesArchologiques']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['LigneLaPlusCourteEntreLesEntitsSitesArchologiques'] = processing.run('native:shortestline', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(271)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source perimetres MH
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_la_couche_monuments_historiques_=0 THEN 'http://atlas.patrimoines.culture.fr/atlas/trunk/ - extraction de mai 2023'\r\nWHEN @utiliser_la_couche_monuments_historiques_=1 THEN '[Refus de l\\'utilisateur]'\r\nEND\r\n\r\n\r\n",
            'INPUT': outputs['JoindreLesAttributsParValeurDeChampPerimetresMh']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\synthese_perimetreMH.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourcePerimetresMh'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(272)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ libelle1 zone etude avant regroupement
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'libelle1',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': 'CASE \r\n\r\nWHEN "code_18"= 111 THEN \'Territoires artificialisés\'\r\nWHEN "code_18"= 112 THEN \'Territoires artificialisés\'\r\nWHEN "code_18"= 121 THEN \'Territoires artificialisés\'\r\nWHEN "code_18"= 122 THEN \'Territoires artificialisés\'\r\nWHEN "code_18"= 123 THEN \'Territoires artificialisés\'\r\nWHEN "code_18"= 124 THEN \'Territoires artificialisés\'\r\nWHEN "code_18"= 131 THEN \'Territoires artificialisés\'\r\nWHEN "code_18"= 132 THEN \'Territoires artificialisés\'\r\nWHEN "code_18"= 133 THEN \'Territoires artificialisés\'\r\nWHEN "code_18"= 141 THEN \'Territoires artificialisés\'\r\nWHEN "code_18"= 142 THEN \'Territoires artificialisés\'\r\nWHEN "code_18"= 211 THEN \'Territoires agricoles\'\r\nWHEN "code_18"= 212 THEN \'Territoires agricoles\'\r\nWHEN "code_18"= 213 THEN \'Territoires agricoles\'\r\nWHEN "code_18"= 221 THEN \'Territoires agricoles\'\r\nWHEN "code_18"= 222 THEN \'Territoires agricoles\'\r\nWHEN "code_18"= 223 THEN \'Territoires agricoles\'\r\nWHEN "code_18"= 231 THEN \'Territoires agricoles\'\r\nWHEN "code_18"= 241 THEN \'Territoires agricoles\'\r\nWHEN "code_18"= 242 THEN \'Territoires agricoles\'\r\nWHEN "code_18"= 243 THEN \'Territoires agricoles\'\r\nWHEN "code_18"= 244 THEN \'Territoires agricoles\'\r\nWHEN "code_18"= 311 THEN \'Forêts et milieux semi-naturels\'\r\nWHEN "code_18"= 312 THEN \'Forêts et milieux semi-naturels\'\r\nWHEN "code_18"= 313 THEN \'Forêts et milieux semi-naturels\'\r\nWHEN "code_18"= 321 THEN \'Forêts et milieux semi-naturels\'\r\nWHEN "code_18"= 322 THEN \'Forêts et milieux semi-naturels\'\r\nWHEN "code_18"= 323 THEN \'Forêts et milieux semi-naturels\'\r\nWHEN "code_18"= 324 THEN \'Forêts et milieux semi-naturels\'\r\nWHEN "code_18"= 331 THEN \'Forêts et milieux semi-naturels\'\r\nWHEN "code_18"= 332 THEN \'Forêts et milieux semi-naturels\'\r\nWHEN "code_18"= 333 THEN \'Forêts et milieux semi-naturels\'\r\nWHEN "code_18"= 334 THEN \'Forêts et milieux semi-naturels\'\r\nWHEN "code_18"= 335 THEN \'Forêts et milieux semi-naturels\'\r\nWHEN "code_18"= 411 THEN \'Zones humides\'\r\nWHEN "code_18"= 412 THEN \'Zones humides\'\r\nWHEN "code_18"= 421 THEN \'Zones humides\'\r\nWHEN "code_18"= 422 THEN \'Zones humides\'\r\nWHEN "code_18"= 423 THEN \'Zones humides\'\r\nWHEN "code_18"= 511 THEN \'Surfaces en eau\'\r\nWHEN "code_18"= 512 THEN \'Surfaces en eau\'\r\nWHEN "code_18"= 521 THEN \'Surfaces en eau\'\r\nWHEN "code_18"= 522 THEN \'Surfaces en eau\'\r\nWHEN "code_18"= 523 THEN \'Surfaces en eau\'\r\n\r\n\r\nEND',
            'INPUT': outputs['AjouterUnChampLibelle1ZoneEtudeAvantRegroupement']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampLibelle1ZoneEtudeAvantRegroupement'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(273)
        if feedback.isCanceled():
            return {}

        # Regrouper par libelle1
        alg_params = {
            'FIELD': ['libelle1'],
            'INPUT': outputs['CalculatriceDeChampLibelle1ZoneEtudeAvantRegroupement']['OUTPUT'],
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RegrouperParLibelle1'] = processing.run('native:dissolve', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(274)
        if feedback.isCanceled():
            return {}

        # Joindre les attributs par valeur de champ pnr
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': QgsExpression("'ID_MNHN'").evaluate(),
            'FIELDS_TO_COPY': QgsExpression("'distance'").evaluate(),
            'FIELD_2': QgsExpression("'ID_MNHN'").evaluate(),
            'INPUT': outputs['CalculatriceDeChampTamponPnr']['OUTPUT'],
            'INPUT_2': outputs['LigneLaPlusCourteEntreLesEntitsPnr']['OUTPUT'],
            'METHOD': 1,  # Prendre uniquement les attributs de la première entité correspondante (un à un)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoindreLesAttributsParValeurDeChampPnr'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(275)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ surf_ha apres regroupement
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'surf_ha',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Décimal (double)
            'FORMULA': ' $area /10000',
            'INPUT': outputs['RegrouperParLibelle1']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\synthese_clc.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSurf_haApresRegroupement'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(276)
        if feedback.isCanceled():
            return {}

        # Regrouper champ DESCR
        alg_params = {
            'FIELD': ['DESCR'],
            'INPUT': outputs['CouperCoucheGologieSiteetude']['OUTPUT'],
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RegrouperChampDescr'] = processing.run('native:dissolve', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(277)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ lienDocument Zonages PLU
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'lienDocument',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': '\'https://data.geopf.fr/annexes/gpu/documents/\'||"partition"||\'/\'||"gpu_doc_id"||\'/\'||"nomfic"',
            'INPUT': outputs['CalculatriceDeChampLienlocagpuZonagesPlu']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampLiendocumentZonagesPlu'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(278)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source APHabitatsNaturels
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_ap_habitats_ =0 THEN 'https://ws.carmencarto.fr/WFS/119/fxx_inpn - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_ap_habitats_ =1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND",
            'INPUT': outputs['JoindreLesAttributsParValeurDeChampAphabitatsnaturels']['OUTPUT'],
            'OUTPUT': QgsExpression("@localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\APHabitatsNaturels_intersect.gpkg'\n").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceAphabitatsnaturels'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(279)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ nomProjet  zone etude
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'nomProjet',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': ' @quelestlenomduprojet ',
            'INPUT': outputs['JoindreLesAttributsParLocalisationTopoZoneEtude']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\ZoneEtude.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampNomprojetZoneEtude'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(280)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source ZNIEFF2
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_znieff2_ =0 THEN 'https://ws.carmencarto.fr/WFS/119/fxx_inpn - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_znieff2_ =1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND",
            'INPUT': outputs['JoindreLesAttributsParValeurDeChampZnieff2']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\znieff2_intersect.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceZnieff2'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(281)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source ZNIEFF1
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_znieff1_ =0 THEN 'https://ws.carmencarto.fr/WFS/119/fxx_inpn - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_znieff1_ =1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND",
            'INPUT': outputs['JoindreLesAttributsParValeurDeChampZnieff1']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\znieff1_intersect.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceZnieff1'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(282)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source CommunesTampon
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_communes_tampon_ =0 THEN 'https://data.geopf.fr/wfs/ows  - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_communes_tampon_ =1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND\r\n\r\n\r\n\r\n",
            'INPUT': outputs['JoindreLesAttributsParValeurDeChampCommunes40Km']['OUTPUT'],
            'OUTPUT': QgsExpression("@localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\CommunesTampon_intersect.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceCommunestampon'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(283)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ COD_GROUP  RPG
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'COD_GROUP',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\n\r\nWHEN\tCODE_CULTU=\t'BTH'\tTHEN\t'1'\r\nWHEN\tCODE_CULTU=\t'BTP'\tTHEN\t'1'\r\nWHEN\tCODE_CULTU=\t'MID'\tTHEN\t'2'\r\nWHEN\tCODE_CULTU=\t'MIE'\tTHEN\t'2'\r\nWHEN\tCODE_CULTU=\t'MIS'\tTHEN\t'2'\r\nWHEN\tCODE_CULTU=\t'ORH'\tTHEN\t'3'\r\nWHEN\tCODE_CULTU=\t'ORP'\tTHEN\t'3'\r\nWHEN\tCODE_CULTU=\t'AVH'\tTHEN\t'4'\r\nWHEN\tCODE_CULTU=\t'AVP'\tTHEN\t'4'\r\nWHEN\tCODE_CULTU=\t'BDH'\tTHEN\t'4'\r\nWHEN\tCODE_CULTU=\t'BDP'\tTHEN\t'4'\r\nWHEN\tCODE_CULTU=\t'BDT'\tTHEN\t'4'\r\nWHEN\tCODE_CULTU=\t'CAG'\tTHEN\t'4'\r\nWHEN\tCODE_CULTU=\t'CAH'\tTHEN\t'4'\r\nWHEN\tCODE_CULTU=\t'CGF'\tTHEN\t'4'\r\nWHEN\tCODE_CULTU=\t'CGH'\tTHEN\t'4'\r\nWHEN\tCODE_CULTU=\t'CGO'\tTHEN\t'4'\r\nWHEN\tCODE_CULTU=\t'CGP'\tTHEN\t'4'\r\nWHEN\tCODE_CULTU=\t'CGS'\tTHEN\t'4'\r\nWHEN\tCODE_CULTU=\t'CHA'\tTHEN\t'4'\r\nWHEN\tCODE_CULTU=\t'CHH'\tTHEN\t'4'\r\nWHEN\tCODE_CULTU=\t'CHS'\tTHEN\t'4'\r\nWHEN\tCODE_CULTU=\t'CHT'\tTHEN\t'4'\r\nWHEN\tCODE_CULTU=\t'CPA'\tTHEN\t'4'\r\nWHEN\tCODE_CULTU=\t'CPH'\tTHEN\t'4'\r\nWHEN\tCODE_CULTU=\t'CPS'\tTHEN\t'4'\r\nWHEN\tCODE_CULTU=\t'CPT'\tTHEN\t'4'\r\nWHEN\tCODE_CULTU=\t'CPZ'\tTHEN\t'4'\r\nWHEN\tCODE_CULTU=\t'EPE'\tTHEN\t'4'\r\nWHEN\tCODE_CULTU=\t'MCR'\tTHEN\t'4'\r\nWHEN\tCODE_CULTU=\t'MCS'\tTHEN\t'4'\r\nWHEN\tCODE_CULTU=\t'MLT'\tTHEN\t'4'\r\nWHEN\tCODE_CULTU=\t'SGH'\tTHEN\t'4'\r\nWHEN\tCODE_CULTU=\t'SGP'\tTHEN\t'4'\r\nWHEN\tCODE_CULTU=\t'SOG'\tTHEN\t'4'\r\nWHEN\tCODE_CULTU=\t'SRS'\tTHEN\t'4'\r\nWHEN\tCODE_CULTU=\t'TTH'\tTHEN\t'4'\r\nWHEN\tCODE_CULTU=\t'TTP'\tTHEN\t'4'\r\nWHEN\tCODE_CULTU=\t'CZH'\tTHEN\t'5'\r\nWHEN\tCODE_CULTU=\t'CZP'\tTHEN\t'5'\r\nWHEN\tCODE_CULTU=\t'TRN'\tTHEN\t'6'\r\nWHEN\tCODE_CULTU=\t'ARA'\tTHEN\t'7'\r\nWHEN\tCODE_CULTU=\t'LIH'\tTHEN\t'7'\r\nWHEN\tCODE_CULTU=\t'LIP'\tTHEN\t'7'\r\nWHEN\tCODE_CULTU=\t'MOL'\tTHEN\t'7'\r\nWHEN\tCODE_CULTU=\t'NVE'\tTHEN\t'7'\r\nWHEN\tCODE_CULTU=\t'NVH'\tTHEN\t'7'\r\nWHEN\tCODE_CULTU=\t'OAG'\tTHEN\t'7'\r\nWHEN\tCODE_CULTU=\t'OEH'\tTHEN\t'7'\r\nWHEN\tCODE_CULTU=\t'OEI'\tTHEN\t'7'\r\nWHEN\tCODE_CULTU=\t'OHN'\tTHEN\t'7'\r\nWHEN\tCODE_CULTU=\t'OHR'\tTHEN\t'7'\r\nWHEN\tCODE_CULTU=\t'OPN'\tTHEN\t'7'\r\nWHEN\tCODE_CULTU=\t'OPR'\tTHEN\t'7'\r\nWHEN\tCODE_CULTU=\t'SOJ'\tTHEN\t'7'\r\nWHEN\tCODE_CULTU=\t'FEV'\tTHEN\t'8'\r\nWHEN\tCODE_CULTU=\t'FVL'\tTHEN\t'8'\r\nWHEN\tCODE_CULTU=\t'FVP'\tTHEN\t'8'\r\nWHEN\tCODE_CULTU=\t'FVT'\tTHEN\t'8'\r\nWHEN\tCODE_CULTU=\t'LDH'\tTHEN\t'8'\r\nWHEN\tCODE_CULTU=\t'LDP'\tTHEN\t'8'\r\nWHEN\tCODE_CULTU=\t'LDT'\tTHEN\t'8'\r\nWHEN\tCODE_CULTU=\t'MPC'\tTHEN\t'8'\r\nWHEN\tCODE_CULTU=\t'MPP'\tTHEN\t'8'\r\nWHEN\tCODE_CULTU=\t'MPT'\tTHEN\t'8'\r\nWHEN\tCODE_CULTU=\t'PAG'\tTHEN\t'8'\r\nWHEN\tCODE_CULTU=\t'PHF'\tTHEN\t'8'\r\nWHEN\tCODE_CULTU=\t'PHI'\tTHEN\t'8'\r\nWHEN\tCODE_CULTU=\t'PHS'\tTHEN\t'8'\r\nWHEN\tCODE_CULTU=\t'PPR'\tTHEN\t'8'\r\nWHEN\tCODE_CULTU=\t'PPT'\tTHEN\t'8'\r\nWHEN\tCODE_CULTU=\t'CHV'\tTHEN\t'9'\r\nWHEN\tCODE_CULTU=\t'CSE'\tTHEN\t'9'\r\nWHEN\tCODE_CULTU=\t'LIF'\tTHEN\t'9'\r\nWHEN\tCODE_CULTU=\t'J5M'\tTHEN\t'11'\r\nWHEN\tCODE_CULTU=\t'J6P'\tTHEN\t'11'\r\nWHEN\tCODE_CULTU=\t'J6S'\tTHEN\t'11'\r\nWHEN\tCODE_CULTU=\t'JAC'\tTHEN\t'11'\r\nWHEN\tCODE_CULTU=\t'JNO'\tTHEN\t'11'\r\nWHEN\tCODE_CULTU=\t'RIZ'\tTHEN\t'14'\r\nWHEN\tCODE_CULTU=\t'LEC'\tTHEN\t'15'\r\nWHEN\tCODE_CULTU=\t'PCH'\tTHEN\t'15'\r\nWHEN\tCODE_CULTU=\t'AFG'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'BVF'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'CAF'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'CHF'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'CPL'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'DTY'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'FAG'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'FET'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'FF5'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'FF6'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'FF7'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'FF8'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'FFO'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'FLO'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'FSG'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'GAI'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'GES'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'GFP'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'JO5'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'JO6'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'JO7'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'JO8'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'JOD'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'JOS'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'LEF'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'LFH'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'LFP'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'LH5'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'LH6'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'LH7'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'LH8'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'LO7'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'LO8'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'LOT'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'LP5'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'LP6'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'LP7'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'LP8'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'LU5'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'LU6'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'LU7'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'LU8'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'LUD'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'LUZ'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'MC5'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'MC6'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'MC7'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'MC8'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'ME5'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'ME6'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'ME7'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'ME8'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'MED'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'MEL'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'MH5'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'MH6'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'MH7'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'MI7'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'MI8'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'MIN'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'ML5'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'ML6'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'ML7'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'ML8'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'MLC'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'MLD'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'MLF'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'MLG'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'MOH'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'NVF'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'PAT'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'PFH'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'PFP'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'PH5'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'PH6'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'PH7'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'PH8'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'PP5'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'PP6'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'PP7'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'PP8'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'RDF'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'SA5'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'SA6'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'SA7'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'SA8'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'SAD'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'SAI'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'SE5'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'SE6'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'SE7'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'SE8'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'SED'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'SER'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'TR5'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'TR6'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'TR7'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'TR8'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'TRD'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'TRE'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'VE5'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'VE6'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'VE7'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'VE8'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'VED'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'VES'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'XFE'\tTHEN\t'16'\r\nWHEN\tCODE_CULTU=\t'BOP'\tTHEN\t'17'\r\nWHEN\tCODE_CULTU=\t'SPH'\tTHEN\t'17'\r\nWHEN\tCODE_CULTU=\t'SPL'\tTHEN\t'17'\r\nWHEN\tCODE_CULTU=\t'PPH'\tTHEN\t'18'\r\nWHEN\tCODE_CULTU=\t'PRL'\tTHEN\t'18'\r\nWHEN\tCODE_CULTU=\t'PTR'\tTHEN\t'19'\r\nWHEN\tCODE_CULTU=\t'RGA'\tTHEN\t'19'\r\nWHEN\tCODE_CULTU=\t'AGR'\tTHEN\t'20'\r\nWHEN\tCODE_CULTU=\t'ANA'\tTHEN\t'20'\r\nWHEN\tCODE_CULTU=\t'AVO'\tTHEN\t'20'\r\nWHEN\tCODE_CULTU=\t'BCA'\tTHEN\t'20'\r\nWHEN\tCODE_CULTU=\t'BCF'\tTHEN\t'20'\r\nWHEN\tCODE_CULTU=\t'BCI'\tTHEN\t'20'\r\nWHEN\tCODE_CULTU=\t'BCP'\tTHEN\t'20'\r\nWHEN\tCODE_CULTU=\t'BCR'\tTHEN\t'20'\r\nWHEN\tCODE_CULTU=\t'BEA'\tTHEN\t'20'\r\nWHEN\tCODE_CULTU=\t'BEF'\tTHEN\t'20'\r\nWHEN\tCODE_CULTU=\t'BEI'\tTHEN\t'20'\r\nWHEN\tCODE_CULTU=\t'BEP'\tTHEN\t'20'\r\nWHEN\tCODE_CULTU=\t'BER'\tTHEN\t'20'\r\nWHEN\tCODE_CULTU=\t'CAC'\tTHEN\t'20'\r\nWHEN\tCODE_CULTU=\t'CBT'\tTHEN\t'20'\r\nWHEN\tCODE_CULTU=\t'PFR'\tTHEN\t'20'\r\nWHEN\tCODE_CULTU=\t'PRU'\tTHEN\t'20'\r\nWHEN\tCODE_CULTU=\t'PVT'\tTHEN\t'20'\r\nWHEN\tCODE_CULTU=\t'PWT'\tTHEN\t'20'\r\nWHEN\tCODE_CULTU=\t'VGD'\tTHEN\t'20'\r\nWHEN\tCODE_CULTU=\t'VRG'\tTHEN\t'20'\r\nWHEN\tCODE_CULTU=\t'RVI'\tTHEN\t'21'\r\nWHEN\tCODE_CULTU=\t'VRC'\tTHEN\t'21'\r\nWHEN\tCODE_CULTU=\t'VRN'\tTHEN\t'21'\r\nWHEN\tCODE_CULTU=\t'VRT'\tTHEN\t'21'\r\nWHEN\tCODE_CULTU=\t'CAB'\tTHEN\t'22'\r\nWHEN\tCODE_CULTU=\t'CTG'\tTHEN\t'22'\r\nWHEN\tCODE_CULTU=\t'NOS'\tTHEN\t'22'\r\nWHEN\tCODE_CULTU=\t'NOX'\tTHEN\t'22'\r\nWHEN\tCODE_CULTU=\t'PIS'\tTHEN\t'22'\r\nWHEN\tCODE_CULTU=\t'OLI'\tTHEN\t'23'\r\nWHEN\tCODE_CULTU=\t'AME'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'ANE'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'ANG'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'ANI'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'AAR'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'ARP'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'BAR'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'BAS'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'BRH'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'BTN'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'CAV'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'CHR'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'CIB'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'CML'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'CMM'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'CRD'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'CRF'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'CUM'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'CUR'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'EST'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'FNO'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'FNU'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'HBL'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'LAV'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'MAV'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'MLI'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'MLP'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'MOT'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'MRJ'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'MTH'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'ORT'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'OSE'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'PAR'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'PMD'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'PME'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'PPA'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'PPF'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'PPP'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'PRF'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'PSL'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'PSN'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'PSY'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'ROM'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'SGE'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'SRI'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'TAB'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'THY'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'TOT'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'VAL'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'VNB'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'VNL'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'VNV'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'YLA'\tTHEN\t'24'\r\nWHEN\tCODE_CULTU=\t'AIL'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'ART'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'AUB'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'BLT'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'BUR'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'CAR'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'CCN'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'CCT'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'CEL'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'CES'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'CHU'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'CMB'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'CRA'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'CRN'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'CRS'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'CSS'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'DOL'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'EPI'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'FLA'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'FLP'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'FRA'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'GER'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'HAR'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'HPC'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'HSA'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'LBF'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'LSA'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'MAC'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'MDI'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'MLO'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'MRG'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'NVT'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'OIG'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'PAN'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'PAQ'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'PAS'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'PMV'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'POR'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'POT'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'PPO'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'PSE'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'PTC'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'PTF'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'PVP'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'RDI'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'ROQ'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'RUT'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'SFI'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'TOM'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'TOP'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'VER'\tTHEN\t'25'\r\nWHEN\tCODE_CULTU=\t'CSA'\tTHEN\t'26'\r\nWHEN\tCODE_CULTU=\t'CSF'\tTHEN\t'26'\r\nWHEN\tCODE_CULTU=\t'CSI'\tTHEN\t'26'\r\nWHEN\tCODE_CULTU=\t'CSP'\tTHEN\t'26'\r\nWHEN\tCODE_CULTU=\t'CSR'\tTHEN\t'26'\r\nWHEN\tCODE_CULTU=\t'ACA'\tTHEN\t'28'\r\nWHEN\tCODE_CULTU=\t'BFP'\tTHEN\t'28'\r\nWHEN\tCODE_CULTU=\t'BFS'\tTHEN\t'28'\r\nWHEN\tCODE_CULTU=\t'BOR'\tTHEN\t'28'\r\nWHEN\tCODE_CULTU=\t'BRO'\tTHEN\t'28'\r\nWHEN\tCODE_CULTU=\t'BTA'\tTHEN\t'28'\r\nWHEN\tCODE_CULTU=\t'CAE'\tTHEN\t'28'\r\nWHEN\tCODE_CULTU=\t'CEE'\tTHEN\t'28'\r\nWHEN\tCODE_CULTU=\t'CNE'\tTHEN\t'28'\r\nWHEN\tCODE_CULTU=\t'CID'\tTHEN\t'28'\r\nWHEN\tCODE_CULTU=\t'CIT'\tTHEN\t'28'\r\nWHEN\tCODE_CULTU=\t'CUA'\tTHEN\t'28'\r\nWHEN\tCODE_CULTU=\t'GRA'\tTHEN\t'28'\r\nWHEN\tCODE_CULTU=\t'MCT'\tTHEN\t'28'\r\nWHEN\tCODE_CULTU=\t'MPA'\tTHEN\t'28'\r\nWHEN\tCODE_CULTU=\t'MRS'\tTHEN\t'28'\r\nWHEN\tCODE_CULTU=\t'MSW'\tTHEN\t'28'\r\nWHEN\tCODE_CULTU=\t'NYG'\tTHEN\t'28'\r\nWHEN\tCODE_CULTU=\t'PCL'\tTHEN\t'28'\r\nWHEN\tCODE_CULTU=\t'PEP'\tTHEN\t'28'\r\nWHEN\tCODE_CULTU=\t'PEV'\tTHEN\t'28'\r\nWHEN\tCODE_CULTU=\t'ROS'\tTHEN\t'28'\r\nWHEN\tCODE_CULTU=\t'SAG'\tTHEN\t'28'\r\nWHEN\tCODE_CULTU=\t'SBO'\tTHEN\t'28'\r\nWHEN\tCODE_CULTU=\t'SHD'\tTHEN\t'28'\r\nWHEN\tCODE_CULTU=\t'SIN'\tTHEN\t'28'\r\nWHEN\tCODE_CULTU=\t'SNA'\tTHEN\t'28'\r\nWHEN\tCODE_CULTU=\t'SNE'\tTHEN\t'28'\r\nWHEN\tCODE_CULTU=\t'SNU'\tTHEN\t'28'\r\nWHEN\tCODE_CULTU=\t'TBT'\tTHEN\t'28'\r\nWHEN\tCODE_CULTU=\t'TCR'\tTHEN\t'28'\r\nWHEN\tCODE_CULTU=\t'TRU'\tTHEN\t'28'\r\nWHEN\tCODE_CULTU=\t'VET'\tTHEN\t'28'\r\nWHEN\tCODE_CULTU=\t'ZZZ'\tTHEN\t'28'\r\nWHEN\tCODE_CULTU=\t'MLS'\tTHEN\t'8'\r\nWHEN\tCODE_CULTU=\t'ACP'\tTHEN\t'28'\r\nELSE 'AUTRE'\r\n\r\nEND",
            'INPUT': outputs['AjouterUnChampCod_groupRpg']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampCod_groupRpg'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(284)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ surface_ha geologie
        alg_params = {
            'FIELD_LENGTH': 20,
            'FIELD_NAME': 'surface_ha',
            'FIELD_PRECISION': 7,
            'FIELD_TYPE': 0,  # Décimal (double)
            'FORMULA': ' $area /10000',
            'INPUT': outputs['RegrouperChampDescr']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSurface_haGeologie'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(285)
        if feedback.isCanceled():
            return {}

        # Ligne la plus courte entre les entités sites Classes inscrits
        alg_params = {
            'DESTINATION': parameters['veuillez_slectionner_la_couche_de_la_zone_dtude_'],
            'DISTANCE': None,
            'METHOD': 0,  # Distance to Nearest Point on feature
            'NEIGHBORS': 1,
            'SOURCE': outputs['CalculatriceDeChampFidSitesClasssInscrits']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['LigneLaPlusCourteEntreLesEntitsSitesClassesInscrits'] = processing.run('native:shortestline', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(286)
        if feedback.isCanceled():
            return {}

        # Ligne la plus courte entre les entités sites patrimoniaux remarquables
        alg_params = {
            'DESTINATION': parameters['veuillez_slectionner_la_couche_de_la_zone_dtude_'],
            'DISTANCE': None,
            'METHOD': 0,  # Distance to Nearest Point on feature
            'NEIGHBORS': 1,
            'SOURCE': outputs['CalculatriceDeChampFidSitesPatrimoniauxRemarquables']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['LigneLaPlusCourteEntreLesEntitsSitesPatrimoniauxRemarquables'] = processing.run('native:shortestline', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(287)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source pnr
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_pnr_ =0 THEN 'https://ws.carmencarto.fr/WFS/119/fxx_inpn - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_pnr_ =1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND",
            'INPUT': outputs['JoindreLesAttributsParValeurDeChampPnr']['OUTPUT'],
            'OUTPUT': QgsExpression("@localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\PNR_intersect.gpkg'\n").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourcePnr'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(288)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source Stations qualité
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_stations_qualit_ =0 THEN 'https://services.sandre.eaufrance.fr/geo/sandre  - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_stations_qualit_ =1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND\r\n\r\n\r\n",
            'INPUT': outputs['JoindreLesAttributsParValeurDeChampStationsQualit']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\stationsQualite_intra_tampon.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceStationsQualit'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(289)
        if feedback.isCanceled():
            return {}

        # Ajouter un champ libelle3 zone etude
        alg_params = {
            'FIELD_ALIAS': None,
            'FIELD_COMMENT': None,
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'libelle3',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'INPUT': outputs['CalculatriceDeChampLibelle1ZoneEtude']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AjouterUnChampLibelle3ZoneEtude'] = processing.run('native:addfieldtoattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(290)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ %
        alg_params = {
            'FIELD_LENGTH': 23,
            'FIELD_NAME': '%',
            'FIELD_PRECISION': 7,
            'FIELD_TYPE': 0,  # Décimal (double)
            'FORMULA': 'surface_ha/(sum($area)/10000)*100',
            'INPUT': outputs['CalculatriceDeChampSurface_haGeologie']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChamp'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(291)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source Zonages PLU
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_zonages_plu_ =0 THEN 'https://data.geopf.fr/wfs/ows - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_zonages_plu_=1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n",
            'INPUT': outputs['CalculatriceDeChampLiendocumentZonagesPlu']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\ZonagesPLU_intersect.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceZonagesPlu'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(292)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source cavites souterraines
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN    @utiliser_le_flux_cavits_souterraines_abandonnes_non_minires_ =0 THEN 'http://geoservices.brgm.fr/risques  - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN  @utiliser_le_flux_cavits_souterraines_abandonnes_non_minires_ =1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND",
            'INPUT': outputs['JoindreLesAttributsParValeurDeChampCavitesSouterraines']['OUTPUT'],
            'OUTPUT': QgsExpression("@localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\cavitesSouterraines_intra_tampon.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceCavitesSouterraines'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(293)
        if feedback.isCanceled():
            return {}

        # Ordonner par % surface_ha
        alg_params = {
            'ASCENDING': False,
            'EXPRESSION': "'surface_ha'",
            'INPUT': outputs['CalculatriceDeChamp']['OUTPUT'],
            'NULLS_FIRST': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['OrdonnerParSurface_ha'] = processing.run('native:orderbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(294)
        if feedback.isCanceled():
            return {}

        # Joindre les attributs par valeur de champ sites archeologiques
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': QgsExpression("'fid'").evaluate(),
            'FIELDS_TO_COPY': QgsExpression("'distance'").evaluate(),
            'FIELD_2': QgsExpression("'fid'").evaluate(),
            'INPUT': outputs['CalculatriceDeChampFidSitesArchologiques']['OUTPUT'],
            'INPUT_2': outputs['LigneLaPlusCourteEntreLesEntitsSitesArchologiques']['OUTPUT'],
            'METHOD': 1,  # Prendre uniquement les attributs de la première entité correspondante (un à un)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoindreLesAttributsParValeurDeChampSitesArcheologiques'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(295)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation EPCI
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_epci_ =0,\r\n'WFS:// pagingEnabled=\\'true\\' preferCoordinatesForWfsT11=\\'false\\' restrictToRequestBBOX=\\'1\\' srsname=\\'EPSG:4326\\' typename=\\'BDTOPO_V3:epci\\' url=\\'https://data.geopf.fr/wfs/ows\\' url=\\'https://data.geopf.fr/wfs/ows?VERSION=2.0.0\\' version=\\'auto\\'',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\epci_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['CalculatriceDeChampNomprojetZoneEtude']['OUTPUT'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationEpci'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(296)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source EPCI
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_epci_ =0 THEN 'https://data.geopf.fr/wfs/ows - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_epci_ =1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND\r\n\r\n\r\n",
            'INPUT': outputs['ExtraireParLocalisationEpci']['OUTPUT'],
            'OUTPUT': QgsExpression("@localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\EPCI_intersect.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceEpci'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(297)
        if feedback.isCanceled():
            return {}

        # Joindre les attributs par valeur de champ sites Classes inscrits
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': QgsExpression("'fid'").evaluate(),
            'FIELDS_TO_COPY': QgsExpression("'distance'").evaluate(),
            'FIELD_2': QgsExpression("'fid'").evaluate(),
            'INPUT': outputs['CalculatriceDeChampFidSitesClasssInscrits']['OUTPUT'],
            'INPUT_2': outputs['LigneLaPlusCourteEntreLesEntitsSitesClassesInscrits']['OUTPUT'],
            'METHOD': 1,  # Prendre uniquement les attributs de la première entité correspondante (un à un)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoindreLesAttributsParValeurDeChampSitesClassesInscrits'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(298)
        if feedback.isCanceled():
            return {}

        # Ajouter un champ LIB_GROUP RPG
        alg_params = {
            'FIELD_ALIAS': None,
            'FIELD_COMMENT': None,
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'LIB_GROUP',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'INPUT': outputs['CalculatriceDeChampCod_groupRpg']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AjouterUnChampLib_groupRpg'] = processing.run('native:addfieldtoattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(299)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source sites archéologiques
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_la_couche_prescriptions_archeologiques_=0 THEN 'http://atlas.patrimoines.culture.fr/atlas/trunk/ - extraction de mai 2023'\r\nWHEN @utiliser_la_couche_prescriptions_archeologiques_=1 THEN '[Refus de l\\'utilisateur]'\r\nEND\r\n\r\n\r\n",
            'INPUT': outputs['JoindreLesAttributsParValeurDeChampSitesArcheologiques']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\synthese_sitesArcheo.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceSitesArchologiques'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(300)
        if feedback.isCanceled():
            return {}

        # Joindre les attributs par valeur de champ sites patrimoniaux remarquables
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': QgsExpression("'fid'").evaluate(),
            'FIELDS_TO_COPY': QgsExpression("'distance'").evaluate(),
            'FIELD_2': QgsExpression("'fid'").evaluate(),
            'INPUT': outputs['CalculatriceDeChampFidSitesPatrimoniauxRemarquables']['OUTPUT'],
            'INPUT_2': outputs['LigneLaPlusCourteEntreLesEntitsSitesPatrimoniauxRemarquables']['OUTPUT'],
            'METHOD': 1,  # Prendre uniquement les attributs de la première entité correspondante (un à un)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoindreLesAttributsParValeurDeChampSitesPatrimoniauxRemarquables'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(301)
        if feedback.isCanceled():
            return {}

        # Extraire par localisation commune
        alg_params = {
            'INPUT': QgsExpression("if ( @utiliser_le_flux_communes_ =0,\r\n'WFS:// pagingEnabled=\\'true\\' preferCoordinatesForWfsT11=\\'false\\' restrictToRequestBBOX=\\'1\\' srsname=\\'EPSG:4326\\' typename=\\'BDTOPO_V3:commune\\' url=\\'https://data.geopf.fr/wfs/ows\\' url=\\'https://data.geopf.fr/wfs/ows?VERSION=2.0.0\\' version=\\'auto\\'',\r\n'R:\\\\SIG\\\\09_Outils\\\\DataPick\\\\couchesVidesNePasOuvrir\\\\commune_vide.gpkg')").evaluate(),
            'INTERSECT': outputs['CalculatriceDeChampNomprojetZoneEtude']['OUTPUT'],
            'PREDICATE': [0],  # intersecte
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraireParLocalisationCommune'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(302)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source sites classes inscrits
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_la_couche_sites_classes_inscrits_=0 THEN 'http://atlas.patrimoines.culture.fr/atlas/trunk/ - extraction de mai 2023'\r\nWHEN @utiliser_la_couche_sites_classes_inscrits_=1 THEN '[Refus de l\\'utilisateur]'\r\nEND\r\n\r\n\r\n",
            'INPUT': outputs['JoindreLesAttributsParValeurDeChampSitesClassesInscrits']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\synthese_sitesClassesInscrits.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceSitesClassesInscrits'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(303)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ liste Zone de Répartition des Eaux
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'communes',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': '\r\narray_to_string(overlay_intersects(   @Extraire_par_localisation_commune_OUTPUT  , nom_officiel))',
            'INPUT': outputs['CouperZonesDeRpartitionDesEaux']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampListeZoneDeRpartitionDesEaux'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(304)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ liste Zones Vulnérables
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'communes',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': '\r\narray_to_string(overlay_intersects(   @Extraire_par_localisation_commune_OUTPUT  , nom_officiel))',
            'INPUT': outputs['CouperZonesVulnrables']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampListeZonesVulnrables'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(305)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source commune
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_communes_ =0 THEN 'https://data.geopf.fr/wfs/ows - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_communes_ =1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND\r\n\r\n\r\n",
            'INPUT': outputs['ExtraireParLocalisationCommune']['OUTPUT'],
            'OUTPUT': QgsExpression("@localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\Commune_intersect.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceCommune'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(306)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ libelle3  zone etude
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'libelle3',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': 'CASE \r\nWHEN "code_18"= 111 THEN \'Tissu urbain continu\'\r\nWHEN "code_18"= 112 THEN \'Tissu urbain discontinu\'\r\nWHEN "code_18"= 121 THEN \'Zones industrielles ou commerciales et installations publiques\'\r\nWHEN "code_18"= 122 THEN \'Réseaux routier et ferroviaire et espaces associés\'\r\nWHEN "code_18"= 123 THEN \'Zones portuaires\'\r\nWHEN "code_18"= 124 THEN \'Aéroports\'\r\nWHEN "code_18"= 131 THEN \'Extraction de matériaux\'\r\nWHEN "code_18"= 132 THEN \'Décharges\'\r\nWHEN "code_18"= 133 THEN \'Chantiers\'\r\nWHEN "code_18"= 141 THEN \'Espaces verts urbains\'\r\nWHEN "code_18"= 142 THEN \'Equipements sportifs et de loisirs\'\r\nWHEN "code_18"= 211 THEN \'Terres arables hors périmètres d\\\'irrigation\'\r\nWHEN "code_18"= 212 THEN \'Périmètres irrigués en permanence\'\r\nWHEN "code_18"= 213 THEN \'Rizières\'\r\nWHEN "code_18"= 221 THEN \'Vignobles\'\r\nWHEN "code_18"= 222 THEN \'Vergers et petits fruits\'\r\nWHEN "code_18"= 223 THEN \'Oliveraies\'\r\nWHEN "code_18"= 231 THEN \'Prairies et autres surfaces toujours en herbe à usage agricole\'\r\nWHEN "code_18"= 241 THEN \'Cultures annuelles associées à des cultures permanentes\'\r\nWHEN "code_18"= 242 THEN \'Systèmes culturaux et parcellaires complexes\'\r\nWHEN "code_18"= 243 THEN \'Surfaces essentiellement agricoles, interrompues par des espaces naturels importants\'\r\nWHEN "code_18"= 244 THEN \'Territoires agroforestiers\'\r\nWHEN "code_18"= 311 THEN \'Forêts de feuillus\'\r\nWHEN "code_18"= 312 THEN \'Forêts de conifères\'\r\nWHEN "code_18"= 313 THEN \'Forêts mélangées\'\r\nWHEN "code_18"= 321 THEN \'Pelouses et pâturages naturels\'\r\nWHEN "code_18"= 322 THEN \'Landes et broussailles\'\r\nWHEN "code_18"= 323 THEN \'Végétation sclérophylle\'\r\nWHEN "code_18"= 324 THEN \'Forêt et végétation arbustive en mutation\'\r\nWHEN "code_18"= 331 THEN \'Plages, dunes et sable\'\r\nWHEN "code_18"= 332 THEN \'Roches nues\'\r\nWHEN "code_18"= 333 THEN \'Végétation clairsemée\'\r\nWHEN "code_18"= 334 THEN \'Zones incendiées\'\r\nWHEN "code_18"= 335 THEN \'Glaciers et neiges éternelles\'\r\nWHEN "code_18"= 411 THEN \'Marais intérieurs\'\r\nWHEN "code_18"= 412 THEN \'Tourbières\'\r\nWHEN "code_18"= 421 THEN \'Marais maritimes\'\r\nWHEN "code_18"= 422 THEN \'Marais salants\'\r\nWHEN "code_18"= 423 THEN \'Zones intertidales\'\r\nWHEN "code_18"= 511 THEN \'Cours et voies d\\\'eau\'\r\nWHEN "code_18"= 512 THEN \'Plans d\\\'eau\'\r\nWHEN "code_18"= 521 THEN \'Lagunes littorales\'\r\nWHEN "code_18"= 522 THEN \'Estuaires\'\r\nWHEN "code_18"= 523 THEN \'Mers et océans\'\r\n\r\nEND',
            'INPUT': outputs['AjouterUnChampLibelle3ZoneEtude']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampLibelle3ZoneEtude'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(307)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ liste Zones Sensibles eutrophisation
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'communes',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': '\r\narray_to_string(overlay_intersects(   @Extraire_par_localisation_commune_OUTPUT  , nom_officiel))',
            'INPUT': outputs['CouperZonesSensiblesEutrophisation']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampListeZonesSensiblesEutrophisation'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(308)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ LIB_GROUP  RPG
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'LIB_GROUP',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\n\r\nWHEN\tCODE_CULTU=\t'BTH'\tTHEN\t'Blé tendre'\r\nWHEN\tCODE_CULTU=\t'BTP'\tTHEN\t'Blé tendre'\r\nWHEN\tCODE_CULTU=\t'MID'\tTHEN\t'Maïs grain et ensilage'\r\nWHEN\tCODE_CULTU=\t'MIE'\tTHEN\t'Maïs grain et ensilage'\r\nWHEN\tCODE_CULTU=\t'MIS'\tTHEN\t'Maïs grain et ensilage'\r\nWHEN\tCODE_CULTU=\t'ORH'\tTHEN\t'Orge'\r\nWHEN\tCODE_CULTU=\t'ORP'\tTHEN\t'Orge'\r\nWHEN\tCODE_CULTU=\t'AVH'\tTHEN\t'Autres céréales'\r\nWHEN\tCODE_CULTU=\t'AVP'\tTHEN\t'Autres céréales'\r\nWHEN\tCODE_CULTU=\t'BDH'\tTHEN\t'Autres céréales'\r\nWHEN\tCODE_CULTU=\t'BDP'\tTHEN\t'Autres céréales'\r\nWHEN\tCODE_CULTU=\t'BDT'\tTHEN\t'Autres céréales'\r\nWHEN\tCODE_CULTU=\t'CAG'\tTHEN\t'Autres céréales'\r\nWHEN\tCODE_CULTU=\t'CAH'\tTHEN\t'Autres céréales'\r\nWHEN\tCODE_CULTU=\t'CGF'\tTHEN\t'Autres céréales'\r\nWHEN\tCODE_CULTU=\t'CGH'\tTHEN\t'Autres céréales'\r\nWHEN\tCODE_CULTU=\t'CGO'\tTHEN\t'Autres céréales'\r\nWHEN\tCODE_CULTU=\t'CGP'\tTHEN\t'Autres céréales'\r\nWHEN\tCODE_CULTU=\t'CGS'\tTHEN\t'Autres céréales'\r\nWHEN\tCODE_CULTU=\t'CHA'\tTHEN\t'Autres céréales'\r\nWHEN\tCODE_CULTU=\t'CHH'\tTHEN\t'Autres céréales'\r\nWHEN\tCODE_CULTU=\t'CHS'\tTHEN\t'Autres céréales'\r\nWHEN\tCODE_CULTU=\t'CHT'\tTHEN\t'Autres céréales'\r\nWHEN\tCODE_CULTU=\t'CPA'\tTHEN\t'Autres céréales'\r\nWHEN\tCODE_CULTU=\t'CPH'\tTHEN\t'Autres céréales'\r\nWHEN\tCODE_CULTU=\t'CPS'\tTHEN\t'Autres céréales'\r\nWHEN\tCODE_CULTU=\t'CPT'\tTHEN\t'Autres céréales'\r\nWHEN\tCODE_CULTU=\t'CPZ'\tTHEN\t'Autres céréales'\r\nWHEN\tCODE_CULTU=\t'EPE'\tTHEN\t'Autres céréales'\r\nWHEN\tCODE_CULTU=\t'MCR'\tTHEN\t'Autres céréales'\r\nWHEN\tCODE_CULTU=\t'MCS'\tTHEN\t'Autres céréales'\r\nWHEN\tCODE_CULTU=\t'MLT'\tTHEN\t'Autres céréales'\r\nWHEN\tCODE_CULTU=\t'SGH'\tTHEN\t'Autres céréales'\r\nWHEN\tCODE_CULTU=\t'SGP'\tTHEN\t'Autres céréales'\r\nWHEN\tCODE_CULTU=\t'SOG'\tTHEN\t'Autres céréales'\r\nWHEN\tCODE_CULTU=\t'SRS'\tTHEN\t'Autres céréales'\r\nWHEN\tCODE_CULTU=\t'TTH'\tTHEN\t'Autres céréales'\r\nWHEN\tCODE_CULTU=\t'TTP'\tTHEN\t'Autres céréales'\r\nWHEN\tCODE_CULTU=\t'CZH'\tTHEN\t'Colza'\r\nWHEN\tCODE_CULTU=\t'CZP'\tTHEN\t'Colza'\r\nWHEN\tCODE_CULTU=\t'TRN'\tTHEN\t'Tournesol'\r\nWHEN\tCODE_CULTU=\t'ARA'\tTHEN\t'Autres oléagineux'\r\nWHEN\tCODE_CULTU=\t'LIH'\tTHEN\t'Autres oléagineux'\r\nWHEN\tCODE_CULTU=\t'LIP'\tTHEN\t'Autres oléagineux'\r\nWHEN\tCODE_CULTU=\t'MOL'\tTHEN\t'Autres oléagineux'\r\nWHEN\tCODE_CULTU=\t'NVE'\tTHEN\t'Autres oléagineux'\r\nWHEN\tCODE_CULTU=\t'NVH'\tTHEN\t'Autres oléagineux'\r\nWHEN\tCODE_CULTU=\t'OAG'\tTHEN\t'Autres oléagineux'\r\nWHEN\tCODE_CULTU=\t'OEH'\tTHEN\t'Autres oléagineux'\r\nWHEN\tCODE_CULTU=\t'OEI'\tTHEN\t'Autres oléagineux'\r\nWHEN\tCODE_CULTU=\t'OHN'\tTHEN\t'Autres oléagineux'\r\nWHEN\tCODE_CULTU=\t'OHR'\tTHEN\t'Autres oléagineux'\r\nWHEN\tCODE_CULTU=\t'OPN'\tTHEN\t'Autres oléagineux'\r\nWHEN\tCODE_CULTU=\t'OPR'\tTHEN\t'Autres oléagineux'\r\nWHEN\tCODE_CULTU=\t'SOJ'\tTHEN\t'Autres oléagineux'\r\nWHEN\tCODE_CULTU=\t'FEV'\tTHEN\t'Protéagineux'\r\nWHEN\tCODE_CULTU=\t'FVL'\tTHEN\t'Protéagineux'\r\nWHEN\tCODE_CULTU=\t'FVP'\tTHEN\t'Protéagineux'\r\nWHEN\tCODE_CULTU=\t'FVT'\tTHEN\t'Protéagineux'\r\nWHEN\tCODE_CULTU=\t'LDH'\tTHEN\t'Protéagineux'\r\nWHEN\tCODE_CULTU=\t'LDP'\tTHEN\t'Protéagineux'\r\nWHEN\tCODE_CULTU=\t'LDT'\tTHEN\t'Protéagineux'\r\nWHEN\tCODE_CULTU=\t'MPC'\tTHEN\t'Protéagineux'\r\nWHEN\tCODE_CULTU=\t'MPP'\tTHEN\t'Protéagineux'\r\nWHEN\tCODE_CULTU=\t'MPT'\tTHEN\t'Protéagineux'\r\nWHEN\tCODE_CULTU=\t'PAG'\tTHEN\t'Protéagineux'\r\nWHEN\tCODE_CULTU=\t'PHF'\tTHEN\t'Protéagineux'\r\nWHEN\tCODE_CULTU=\t'PHI'\tTHEN\t'Protéagineux'\r\nWHEN\tCODE_CULTU=\t'PHS'\tTHEN\t'Protéagineux'\r\nWHEN\tCODE_CULTU=\t'PPR'\tTHEN\t'Protéagineux'\r\nWHEN\tCODE_CULTU=\t'PPT'\tTHEN\t'Protéagineux'\r\nWHEN\tCODE_CULTU=\t'CHV'\tTHEN\t'Plantes à fibres'\r\nWHEN\tCODE_CULTU=\t'CSE'\tTHEN\t'Plantes à fibres'\r\nWHEN\tCODE_CULTU=\t'LIF'\tTHEN\t'Plantes à fibres'\r\nWHEN\tCODE_CULTU=\t'J5M'\tTHEN\t'Gel (surfaces gelées sans production)'\r\nWHEN\tCODE_CULTU=\t'J6P'\tTHEN\t'Gel (surfaces gelées sans production)'\r\nWHEN\tCODE_CULTU=\t'J6S'\tTHEN\t'Gel (surfaces gelées sans production)'\r\nWHEN\tCODE_CULTU=\t'JAC'\tTHEN\t'Gel (surfaces gelées sans production)'\r\nWHEN\tCODE_CULTU=\t'JNO'\tTHEN\t'Gel (surfaces gelées sans production)'\r\nWHEN\tCODE_CULTU=\t'RIZ'\tTHEN\t'Riz'\r\nWHEN\tCODE_CULTU=\t'LEC'\tTHEN\t'Légumineuses à grains'\r\nWHEN\tCODE_CULTU=\t'PCH'\tTHEN\t'Légumineuses à grains'\r\nWHEN\tCODE_CULTU=\t'AFG'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'BVF'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'CAF'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'CHF'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'CPL'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'DTY'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'FAG'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'FET'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'FF5'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'FF6'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'FF7'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'FF8'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'FFO'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'FLO'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'FSG'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'GAI'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'GES'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'GFP'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'JO5'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'JO6'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'JO7'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'JO8'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'JOD'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'JOS'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'LEF'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'LFH'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'LFP'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'LH5'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'LH6'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'LH7'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'LH8'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'LO7'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'LO8'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'LOT'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'LP5'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'LP6'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'LP7'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'LP8'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'LU5'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'LU6'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'LU7'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'LU8'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'LUD'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'LUZ'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'MC5'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'MC6'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'MC7'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'MC8'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'ME5'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'ME6'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'ME7'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'ME8'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'MED'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'MEL'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'MH5'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'MH6'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'MH7'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'MI7'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'MI8'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'MIN'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'ML5'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'ML6'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'ML7'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'ML8'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'MLC'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'MLD'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'MLF'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'MLG'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'MOH'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'NVF'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'PAT'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'PFH'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'PFP'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'PH5'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'PH6'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'PH7'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'PH8'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'PP5'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'PP6'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'PP7'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'PP8'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'RDF'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'SA5'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'SA6'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'SA7'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'SA8'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'SAD'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'SAI'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'SE5'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'SE6'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'SE7'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'SE8'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'SED'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'SER'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'TR5'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'TR6'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'TR7'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'TR8'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'TRD'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'TRE'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'VE5'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'VE6'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'VE7'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'VE8'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'VED'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'VES'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'XFE'\tTHEN\t'Fourrage'\r\nWHEN\tCODE_CULTU=\t'BOP'\tTHEN\t'Estives et landes'\r\nWHEN\tCODE_CULTU=\t'SPH'\tTHEN\t'Estives et landes'\r\nWHEN\tCODE_CULTU=\t'SPL'\tTHEN\t'Estives et landes'\r\nWHEN\tCODE_CULTU=\t'PPH'\tTHEN\t'Prairies permanentes'\r\nWHEN\tCODE_CULTU=\t'PRL'\tTHEN\t'Prairies permanentes'\r\nWHEN\tCODE_CULTU=\t'PTR'\tTHEN\t'Prairies temporaires'\r\nWHEN\tCODE_CULTU=\t'RGA'\tTHEN\t'Prairies temporaires'\r\nWHEN\tCODE_CULTU=\t'AGR'\tTHEN\t'Vergers'\r\nWHEN\tCODE_CULTU=\t'ANA'\tTHEN\t'Vergers'\r\nWHEN\tCODE_CULTU=\t'AVO'\tTHEN\t'Vergers'\r\nWHEN\tCODE_CULTU=\t'BCA'\tTHEN\t'Vergers'\r\nWHEN\tCODE_CULTU=\t'BCF'\tTHEN\t'Vergers'\r\nWHEN\tCODE_CULTU=\t'BCI'\tTHEN\t'Vergers'\r\nWHEN\tCODE_CULTU=\t'BCP'\tTHEN\t'Vergers'\r\nWHEN\tCODE_CULTU=\t'BCR'\tTHEN\t'Vergers'\r\nWHEN\tCODE_CULTU=\t'BEA'\tTHEN\t'Vergers'\r\nWHEN\tCODE_CULTU=\t'BEF'\tTHEN\t'Vergers'\r\nWHEN\tCODE_CULTU=\t'BEI'\tTHEN\t'Vergers'\r\nWHEN\tCODE_CULTU=\t'BEP'\tTHEN\t'Vergers'\r\nWHEN\tCODE_CULTU=\t'BER'\tTHEN\t'Vergers'\r\nWHEN\tCODE_CULTU=\t'CAC'\tTHEN\t'Vergers'\r\nWHEN\tCODE_CULTU=\t'CBT'\tTHEN\t'Vergers'\r\nWHEN\tCODE_CULTU=\t'PFR'\tTHEN\t'Vergers'\r\nWHEN\tCODE_CULTU=\t'PRU'\tTHEN\t'Vergers'\r\nWHEN\tCODE_CULTU=\t'PVT'\tTHEN\t'Vergers'\r\nWHEN\tCODE_CULTU=\t'PWT'\tTHEN\t'Vergers'\r\nWHEN\tCODE_CULTU=\t'VGD'\tTHEN\t'Vergers'\r\nWHEN\tCODE_CULTU=\t'VRG'\tTHEN\t'Vergers'\r\nWHEN\tCODE_CULTU=\t'RVI'\tTHEN\t'Vignes'\r\nWHEN\tCODE_CULTU=\t'VRC'\tTHEN\t'Vignes'\r\nWHEN\tCODE_CULTU=\t'VRN'\tTHEN\t'Vignes'\r\nWHEN\tCODE_CULTU=\t'VRT'\tTHEN\t'Vignes'\r\nWHEN\tCODE_CULTU=\t'CAB'\tTHEN\t'Fruits à coque'\r\nWHEN\tCODE_CULTU=\t'CTG'\tTHEN\t'Fruits à coque'\r\nWHEN\tCODE_CULTU=\t'NOS'\tTHEN\t'Fruits à coque'\r\nWHEN\tCODE_CULTU=\t'NOX'\tTHEN\t'Fruits à coque'\r\nWHEN\tCODE_CULTU=\t'PIS'\tTHEN\t'Fruits à coque'\r\nWHEN\tCODE_CULTU=\t'OLI'\tTHEN\t'Oliviers'\r\nWHEN\tCODE_CULTU=\t'AME'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'ANE'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'ANG'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'ANI'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'AAR'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'ARP'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'BAR'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'BAS'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'BRH'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'BTN'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'CAV'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'CHR'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'CIB'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'CML'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'CMM'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'CRD'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'CRF'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'CUM'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'CUR'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'EST'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'FNO'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'FNU'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'HBL'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'LAV'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'MAV'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'MLI'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'MLP'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'MOT'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'MRJ'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'MTH'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'ORT'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'OSE'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'PAR'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'PMD'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'PME'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'PPA'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'PPF'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'PPP'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'PRF'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'PSL'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'PSN'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'PSY'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'ROM'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'SGE'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'SRI'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'TAB'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'THY'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'TOT'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'VAL'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'VNB'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'VNL'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'VNV'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'YLA'\tTHEN\t'Autres cultures industrielles'\r\nWHEN\tCODE_CULTU=\t'AIL'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'ART'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'AUB'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'BLT'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'BUR'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'CAR'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'CCN'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'CCT'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'CEL'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'CES'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'CHU'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'CMB'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'CRA'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'CRN'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'CRS'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'CSS'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'DOL'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'EPI'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'FLA'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'FLP'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'FRA'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'GER'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'HAR'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'HPC'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'HSA'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'LBF'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'LSA'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'MAC'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'MDI'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'MLO'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'MRG'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'NVT'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'OIG'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'PAN'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'PAQ'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'PAS'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'PMV'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'POR'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'POT'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'PPO'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'PSE'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'PTC'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'PTF'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'PVP'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'RDI'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'ROQ'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'RUT'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'SFI'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'TOM'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'TOP'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'VER'\tTHEN\t'Légumes ou fleurs'\r\nWHEN\tCODE_CULTU=\t'CSA'\tTHEN\t'Canne à sucre'\r\nWHEN\tCODE_CULTU=\t'CSF'\tTHEN\t'Canne à sucre'\r\nWHEN\tCODE_CULTU=\t'CSI'\tTHEN\t'Canne à sucre'\r\nWHEN\tCODE_CULTU=\t'CSP'\tTHEN\t'Canne à sucre'\r\nWHEN\tCODE_CULTU=\t'CSR'\tTHEN\t'Canne à sucre'\r\nWHEN\tCODE_CULTU=\t'ACA'\tTHEN\t'Divers'\r\nWHEN\tCODE_CULTU=\t'BFP'\tTHEN\t'Divers'\r\nWHEN\tCODE_CULTU=\t'BFS'\tTHEN\t'Divers'\r\nWHEN\tCODE_CULTU=\t'BOR'\tTHEN\t'Divers'\r\nWHEN\tCODE_CULTU=\t'BRO'\tTHEN\t'Divers'\r\nWHEN\tCODE_CULTU=\t'BTA'\tTHEN\t'Divers'\r\nWHEN\tCODE_CULTU=\t'CAE'\tTHEN\t'Divers'\r\nWHEN\tCODE_CULTU=\t'CEE'\tTHEN\t'Divers'\r\nWHEN\tCODE_CULTU=\t'CNE'\tTHEN\t'Divers'\r\nWHEN\tCODE_CULTU=\t'CID'\tTHEN\t'Divers'\r\nWHEN\tCODE_CULTU=\t'CIT'\tTHEN\t'Divers'\r\nWHEN\tCODE_CULTU=\t'CUA'\tTHEN\t'Divers'\r\nWHEN\tCODE_CULTU=\t'GRA'\tTHEN\t'Divers'\r\nWHEN\tCODE_CULTU=\t'MCT'\tTHEN\t'Divers'\r\nWHEN\tCODE_CULTU=\t'MPA'\tTHEN\t'Divers'\r\nWHEN\tCODE_CULTU=\t'MRS'\tTHEN\t'Divers'\r\nWHEN\tCODE_CULTU=\t'MSW'\tTHEN\t'Divers'\r\nWHEN\tCODE_CULTU=\t'NYG'\tTHEN\t'Divers'\r\nWHEN\tCODE_CULTU=\t'PCL'\tTHEN\t'Divers'\r\nWHEN\tCODE_CULTU=\t'PEP'\tTHEN\t'Divers'\r\nWHEN\tCODE_CULTU=\t'PEV'\tTHEN\t'Divers'\r\nWHEN\tCODE_CULTU=\t'ROS'\tTHEN\t'Divers'\r\nWHEN\tCODE_CULTU=\t'SAG'\tTHEN\t'Divers'\r\nWHEN\tCODE_CULTU=\t'SBO'\tTHEN\t'Divers'\r\nWHEN\tCODE_CULTU=\t'SHD'\tTHEN\t'Divers'\r\nWHEN\tCODE_CULTU=\t'SIN'\tTHEN\t'Divers'\r\nWHEN\tCODE_CULTU=\t'SNA'\tTHEN\t'Divers'\r\nWHEN\tCODE_CULTU=\t'SNE'\tTHEN\t'Divers'\r\nWHEN\tCODE_CULTU=\t'SNU'\tTHEN\t'Divers'\r\nWHEN\tCODE_CULTU=\t'TBT'\tTHEN\t'Divers'\r\nWHEN\tCODE_CULTU=\t'TCR'\tTHEN\t'Divers'\r\nWHEN\tCODE_CULTU=\t'TRU'\tTHEN\t'Divers'\r\nWHEN\tCODE_CULTU=\t'VET'\tTHEN\t'Divers'\r\nWHEN\tCODE_CULTU=\t'ZZZ'\tTHEN\t'Divers'\r\nWHEN\tCODE_CULTU=\t'MLS'\tTHEN\t'Protéagineux'\r\nWHEN\tCODE_CULTU=\t'ACP'\tTHEN\t'Divers'\r\nELSE 'Autre'\r\n\r\nEND",
            'INPUT': outputs['AjouterUnChampLib_groupRpg']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampLib_groupRpg'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(309)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source geologie
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_couches_gologiques_ =0 THEN 'https://infoterre.brgm.fr/formulaire/telechargement-cartes-geologiques-departementales-150-000-bd-charm-50 - extraction février 2023'\r\nWHEN @utiliser_le_flux_couches_gologiques_ =1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND\r\n\r\n\r\n",
            'INPUT': outputs['OrdonnerParSurface_ha']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\geologie_pourcentages.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceGeologie'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(310)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source Zone de répartition des eaux
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_zones_repartition_des_eaux_ =0 THEN 'https://services.sandre.eaufrance.fr/geo/sandre - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_zones_repartition_des_eaux_=1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND\r\n\r\n\r\n\r\n\r\n\r\n\r\n",
            'INPUT': outputs['CalculatriceDeChampListeZoneDeRpartitionDesEaux']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\ZRE_intersect.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceZoneDeRpartitionDesEaux'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(311)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source Sites patrimoniaux Remarquables
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_la_couche_sites_patrimoniaux_remarquables_=0 THEN 'http://atlas.patrimoines.culture.fr/atlas/trunk/ - extraction de mai 2023'\r\nWHEN @utiliser_la_couche_sites_patrimoniaux_remarquables_=1 THEN '[Refus de l\\'utilisateur]'\r\nEND\r\n\r\n\r\n",
            'INPUT': outputs['JoindreLesAttributsParValeurDeChampSitesPatrimoniauxRemarquables']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\synthese_sitesPatrimoniaux.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceSitesPatrimoniauxRemarquables'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(312)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ % RPG
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': '%',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Décimal (double)
            'FORMULA': 'round((surface_ha/(sum(surface_ha)))*100,2)',
            'INPUT': outputs['CalculatriceDeChampLib_groupRpg']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampRpg'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(313)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source zones vulnérables
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_zones_vulnerables_nitrates_ =0 THEN 'https://services.sandre.eaufrance.fr/geo/sandre - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_zones_vulnerables_nitrates_=1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND\r\n\r\n\r\n\r\n\r\n\r\n\r\n",
            'INPUT': outputs['CalculatriceDeChampListeZonesVulnrables']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\ZonesVulnerables_intersect.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceZonesVulnrables'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(314)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source synthese RPG
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN    @utiliser_la_couche_rpg_  =0 THEN 'https://geoservices.ign.fr/rpg  - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_la_couche_rpg_ =1 THEN '[refus de l\\'utilisateur]'\r\nEND",
            'INPUT': outputs['CalculatriceDeChampRpg']['OUTPUT'],
            'OUTPUT': QgsExpression("@localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\syntheseTablo_rpg.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceSyntheseRpg'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(315)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source Zones sensibles eutrophisation
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_zones_sensibles_eutrophisation_ =0 THEN 'https://services.sandre.eaufrance.fr/geo/sandre - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_zones_sensibles_eutrophisation_=1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND\r\n\r\n\r\n\r\n\r\n\r\n\r\n",
            'INPUT': outputs['CalculatriceDeChampListeZonesSensiblesEutrophisation']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\ZonesSensibles_intersect.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceZonesSensiblesEutrophisation'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(316)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ pourcentage CLC
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': '%',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Décimal (double)
            'FORMULA': 'round((surface_ha/(sum(surface_ha)))*100,2)',
            'INPUT': outputs['CalculatriceDeChampLibelle3ZoneEtude']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampPourcentageClc'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(317)
        if feedback.isCanceled():
            return {}

        # Exporter vers un tableur statistiques_RPG_zone
        alg_params = {
            'FORMATTED_VALUES': False,
            'LAYERS': outputs['CalculatriceDeChampSourceSyntheseRpg']['OUTPUT'],
            'OUTPUT': QgsExpression("@localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\syntheseTablo_rpg.xlsx'").evaluate(),
            'OVERWRITE': True,
            'USE_ALIAS': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExporterVersUnTableurStatistiques_rpg_zone'] = processing.run('native:exporttospreadsheet', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(318)
        if feedback.isCanceled():
            return {}

        # Ordonner par expression % CLC
        alg_params = {
            'ASCENDING': True,
            'EXPRESSION': 'round((surface_ha/(sum(surface_ha)))*100,2)',
            'INPUT': outputs['CalculatriceDeChampPourcentageClc']['OUTPUT'],
            'NULLS_FIRST': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['OrdonnerParExpressionClc'] = processing.run('native:orderbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(319)
        if feedback.isCanceled():
            return {}

        # Calculatrice de champ source CLC
        alg_params = {
            'FIELD_LENGTH': 254,
            'FIELD_NAME': 'source',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texte (chaîne de caractères)
            'FORMULA': "CASE\r\nWHEN   @utiliser_le_flux_clc_ =0 THEN 'https://data.geopf.fr/wfs/ows - extraction du '||format_date(now(),'dd.MM.yyyy')\r\nWHEN @utiliser_le_flux_clc_ =1 THEN '[flux non opérationnel ou refus de l\\'utilisateur]'\r\nEND\r\n\r\n",
            'INPUT': outputs['OrdonnerParExpressionClc']['OUTPUT'],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\syntheseTablo_clc.gpkg'").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatriceDeChampSourceClc'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(320)
        if feedback.isCanceled():
            return {}

        # Création d'un Géopackage
        alg_params = {
            'EXPORT_RELATED_LAYERS': False,
            'LAYERS': [outputs['CalculatriceDeChampSurf_haApresRegroupement']['OUTPUT'],outputs['CalculatriceDeChampSourceZnieff1']['OUTPUT'],outputs['CalculatriceDeChampSourceZnieff2']['OUTPUT'],outputs['CalculatriceDeChampSourceZps']['OUTPUT'],outputs['CalculatriceDeChampSourceSic']['OUTPUT'],outputs['CalculatriceDeChampSourceClimat']['OUTPUT'],outputs['CalculatriceDeChampSourceContextePiscicole']['OUTPUT'],outputs['CalculatriceDeChampSourceSage']['OUTPUT'],outputs['CalculatriceDeChampSourceMassedosuperficielle']['OUTPUT'],outputs['CalculatriceDeChampSourceMasseDeauSouterraine']['OUTPUT'],outputs['CalculatriceDeChampSourceAgenceDeLeau']['OUTPUT'],outputs['CalculatriceDeChampSourcePerimetresMh']['OUTPUT'],outputs['CalculatriceDeChampSourceSitesArchologiques']['OUTPUT'],outputs['CalculatriceDeChampSourceSitesClassesInscrits']['OUTPUT'],outputs['CalculatriceDeChampSourceSitesPatrimoniauxRemarquables']['OUTPUT'],outputs['CalculatriceDeChampSourceClc']['OUTPUT'],outputs['CalculatriceDeChampSourceStationsQualit']['OUTPUT'],outputs['CalculatriceDeChampSourceStationsDbit']['OUTPUT'],outputs['CalculatriceDeChampSourceGeologie']['OUTPUT'],outputs['CalculatriceDeChampSourceHydroecoregions']['OUTPUT'],outputs['CalculatriceDeChampSourcePpri']['OUTPUT'],outputs['CalculatriceDeChampSourcePprterrain']['OUTPUT'],outputs['CalculatriceDeChampSourcePprSeismes']['OUTPUT'],outputs['CalculatriceDeChampSourcePprTechnologique']['OUTPUT'],outputs['CalculatriceDeChampSourceZoneDeRpartitionDesEaux']['OUTPUT'],outputs['CalculatriceDeChampSourceZonesSensiblesEutrophisation']['OUTPUT'],outputs['CalculatriceDeChampSourceZonagesCartesCommunales']['OUTPUT'],outputs['CalculatriceDeChampSourceZonagesPlu']['OUTPUT'],outputs['CalculatriceDeChampSourceStationsmeteo']['OUTPUT'],outputs['CalculatriceDeChampSourceZico']['OUTPUT'],outputs['CalculatriceDeChampSourceZonesVulnrables']['OUTPUT'],outputs['CalculatriceDeChampSourceAlaInondationsFrquent']['OUTPUT'],outputs['CalculatriceDeChampSourceAlaInondationsMoyen']['OUTPUT'],outputs['CalculatriceDeChampSourceAlaInondationsRare']['OUTPUT'],outputs['CalculatriceDeChampSourceCommune']['OUTPUT'],outputs['CalculatriceDeChampSourceEpci']['OUTPUT'],outputs['CalculatriceDeChampSourceCommunestampon']['OUTPUT'],outputs['CalculatriceDeChampSourceRnr']['OUTPUT'],outputs['CalculatriceDeChampSourceParcsNationaux']['OUTPUT'],outputs['CalculatriceDeChampSourceRamsar']['OUTPUT'],outputs['CalculatriceDeChampSourceAppb']['OUTPUT'],outputs['CalculatriceDeChampSourceAphabitatsnaturels']['OUTPUT'],outputs['CalculatriceDeChampSourcePnr']['OUTPUT'],outputs['CalculatriceDeChampSourceRn']['OUTPUT'],outputs['CalculatriceDeChampSourceReserveDeBiosphere']['OUTPUT'],outputs['CalculatriceDeChampSourceReservesBiologiques']['OUTPUT'],outputs['CalculatriceDeChampNomprojetZoneEtude']['OUTPUT'],outputs['CalculatriceDeChampSourceRoseDesVentsIowa']['OUTPUT'],outputs['Tampon5km']['OUTPUT'],outputs['Tampon10km']['OUTPUT'],outputs['CalculatriceDeChampSourceCavitesSouterraines']['OUTPUT'],outputs['CalculatriceDeChampSourceBss']['OUTPUT'],outputs['CalculatriceDeChampSourceContinuiteEcologiqueListe1']['OUTPUT'],outputs['CalculatriceDeChampSourceContinuiteEcologiqueListe2']['OUTPUT'],outputs['CalculatriceDeChampSourceEnsoleillement']['OUTPUT'],outputs['CalculatriceDeChampSourceSismicit']['OUTPUT'],outputs['CalculatriceDeChampSourceRadon']['OUTPUT']],
            'OUTPUT': QgsExpression("   @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\'||@quelestlenomduprojet||'.gpkg'").evaluate(),
            'OVERWRITE': True,
            'SAVE_METADATA': True,
            'SAVE_STYLES': True,
            'SELECTED_FEATURES_ONLY': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CrationDunGopackage'] = processing.run('native:package', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(321)
        if feedback.isCanceled():
            return {}

        # Exporter vers un tableur statistiques_CLC
        alg_params = {
            'FORMATTED_VALUES': False,
            'LAYERS': outputs['CalculatriceDeChampSourceClc']['OUTPUT'],
            'OUTPUT': QgsExpression("@localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\syntheseTablo_clc.xlsx'").evaluate(),
            'OVERWRITE': True,
            'USE_ALIAS': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExporterVersUnTableurStatistiques_clc'] = processing.run('native:exporttospreadsheet', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(322)
        if feedback.isCanceled():
            return {}

        # Exporter vers un tableur BDD
        alg_params = {
            'FORMATTED_VALUES': False,
            'LAYERS': [outputs['CalculatriceDeChampSourceZnieff1']['OUTPUT'],outputs['CalculatriceDeChampSourceZnieff2']['OUTPUT'],outputs['CalculatriceDeChampSourceZps']['OUTPUT'],outputs['CalculatriceDeChampSourceSic']['OUTPUT'],outputs['CalculatriceDeChampSourceClimat']['OUTPUT'],outputs['CalculatriceDeChampSourceContextePiscicole']['OUTPUT'],outputs['CalculatriceDeChampSourceSage']['OUTPUT'],outputs['CalculatriceDeChampSourceMassedosuperficielle']['OUTPUT'],outputs['CalculatriceDeChampSourceMasseDeauSouterraine']['OUTPUT'],outputs['CalculatriceDeChampSourceAgenceDeLeau']['OUTPUT'],outputs['CalculatriceDeChampSourcePerimetresMh']['OUTPUT'],outputs['CalculatriceDeChampSourceSitesArchologiques']['OUTPUT'],outputs['CalculatriceDeChampSourceSitesClassesInscrits']['OUTPUT'],outputs['CalculatriceDeChampSourceSitesPatrimoniauxRemarquables']['OUTPUT'],outputs['CalculatriceDeChampSourceStationsQualit']['OUTPUT'],outputs['CalculatriceDeChampSourceStationsDbit']['OUTPUT'],outputs['CalculatriceDeChampSourceGeologie']['OUTPUT'],outputs['CalculatriceDeChampSourceHydroecoregions']['OUTPUT'],outputs['CalculatriceDeChampSourcePpri']['OUTPUT'],outputs['CalculatriceDeChampSourcePprterrain']['OUTPUT'],outputs['CalculatriceDeChampSourcePprSeismes']['OUTPUT'],outputs['CalculatriceDeChampSourcePprTechnologique']['OUTPUT'],outputs['CalculatriceDeChampSourceZoneDeRpartitionDesEaux']['OUTPUT'],outputs['CalculatriceDeChampSourceZonesSensiblesEutrophisation']['OUTPUT'],outputs['CalculatriceDeChampSourceZonagesCartesCommunales']['OUTPUT'],outputs['CalculatriceDeChampSourceStationsmeteo']['OUTPUT'],outputs['CalculatriceDeChampSourceZico']['OUTPUT'],outputs['CalculatriceDeChampSourceZonesVulnrables']['OUTPUT'],outputs['CalculatriceDeChampSourceAlaInondationsFrquent']['OUTPUT'],outputs['CalculatriceDeChampSourceAlaInondationsMoyen']['OUTPUT'],outputs['CalculatriceDeChampSourceAlaInondationsRare']['OUTPUT'],outputs['ExporterVersUnTableurStatistiques_clc']['OUTPUT'],outputs['CalculatriceDeChampSourceZonagesPlu']['OUTPUT'],outputs['CalculatriceDeChampSourceCommune']['OUTPUT'],outputs['CalculatriceDeChampSourceEpci']['OUTPUT'],outputs['CalculatriceDeChampSourceCommunestampon']['OUTPUT'],outputs['CalculatriceDeChampSurf_haApresRegroupement']['OUTPUT'],outputs['CalculatriceDeChampSourceRnr']['OUTPUT'],outputs['CalculatriceDeChampSourceParcsNationaux']['OUTPUT'],outputs['CalculatriceDeChampSourceRamsar']['OUTPUT'],outputs['CalculatriceDeChampSourceAppb']['OUTPUT'],outputs['CalculatriceDeChampSourceAphabitatsnaturels']['OUTPUT'],outputs['CalculatriceDeChampSourcePnr']['OUTPUT'],outputs['CalculatriceDeChampSourceRn']['OUTPUT'],outputs['CalculatriceDeChampSourceReserveDeBiosphere']['OUTPUT'],outputs['CalculatriceDeChampSourceReservesBiologiques']['OUTPUT'],outputs['CalculatriceDeChampSourceRoseDesVentsIowa']['OUTPUT'],outputs['CalculatriceDeChampNomprojetZoneEtude']['OUTPUT'],outputs['CalculatriceDeChampSourceCavitesSouterraines']['OUTPUT'],outputs['CalculatriceDeChampSourceBss']['OUTPUT'],outputs['CalculatriceDeChampSourceContinuiteEcologiqueListe1']['OUTPUT'],outputs['CalculatriceDeChampSourceContinuiteEcologiqueListe2']['OUTPUT'],outputs['CalculatriceDeChampSourceEnsoleillement']['OUTPUT'],outputs['CalculatriceDeChampSourceSismicit']['OUTPUT'],outputs['CalculatriceDeChampSourceRadon']['OUTPUT'],outputs['ExporterVersUnTableurStatistiques_rpg_zone']['OUTPUT']],
            'OUTPUT': QgsExpression(" @localisez_le_dossier_de_sortie_pour_les_couches_sig_et_tableurs_ ||'\\\\BDD_SIG_'|| @model_name ||'.xlsx'").evaluate(),
            'OVERWRITE': True,
            'USE_ALIAS': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExporterVersUnTableurBdd'] = processing.run('native:exporttospreadsheet', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results
        
    def id(self):
        return 'phase1_CréationTablo_Etat_Initial_v28'

    def name(self):
        return 'phase1_CréationTablo_Etat_Initial_v28'

    def displayName(self):
        return 'Phase1 CréationTablo Etat Initial v28'

    def group(self):
        return 'Phase1 CréationTablo Etat Initial v28'

    def groupId(self):
        return 'phase1_creationtablo_etat_initial_v28'

    def shortHelpString(self):
        return """<html><body><p><!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><style type="text/css">
p, li { white-space: pre-wrap; }
</style></head><body style=" font-family:'MS Shell Dlg 2'; font-size:8.3pt; font-weight:400; font-style:normal;">
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:600; color:#ff0000;">AVANT D'UTILISER CET OUTIL VOUS DEVEZ AVOIR INSTALLE LE PLUGIN &quot;MapsPrinter&quot; disponible dans la médiathèque</span></p>
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-weight:600; color:#ff0000;"><br /></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:600; color:#ff0000;">VOUS DEVEZ EGALEMENT COPIER LE PROJET QGIS Etat_Initial_Cartographie DANS VOTRE REPERTOIRE DE TRAVAIL</span></p>
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8.25pt; font-weight:600; text-decoration: underline;">VOUS DEVEZ UNIQUEMENT CHARGER LA COUCHE ZONE ETUDE DANS QGIS.</span></p>
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8.25pt;"><br /></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8.25pt;">LE TRAITEMENT GENERE UN TABLEUR EXCEL BDD_SIG QUI EST EST A UTILISER AVEC L'OUTIL DE JUSTINE.</span></p>
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8.25pt;"><br /></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8.25pt;">LE TRAITEMENT DURE ENVIRON 30 MINUTES POUR UNE ZONE D ETUDE DE LA TAILLE D UNE COMMUNE.</span></p>
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8.25pt;"><br /></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8.25pt;">SI VOUS NE SOUHAITEZ PAS UTILISER UN FLUX EN PARTICULIER (PAS UTILE ou FLUX NON OPERATIONNEL) VOUS POUVEZ DEPLIER LA ZONE DES PARAMETRES AVANCES ET PASSER LE PARAMAMETRE DU FLUX SUR &quot;NON&quot;.</span></p>
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8.25pt;"><br /></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8.25pt;">IL EST EGALEMENT POSSIBLE DE FUSIONNER TOUS CES FICHIERS SIG DANS UN GEOPACKAGE UNIQUE. SI LA REPONSE EST OUI ALORS LE TEMPS DE TRAITEMENT SERA ALLONGE (5 - 10 min supplémentaires)</span></p>
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8.25pt;"><br /></p>
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8.25pt;"><br /></p>
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8.25pt;"><br /></p>
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8.25pt;"><br /></p></body></html></p>
<br></body></html>"""

    def createInstance(self):
        return Phase1_creationtablo_etat_initial_v28()
