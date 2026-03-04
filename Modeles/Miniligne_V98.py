from qgis.core import (QgsFeature, QgsVectorLayer, QgsField, QgsSpatialIndex, QgsGeometry,
                       QgsProcessingAlgorithm, QgsProcessingParameterVectorLayer, QgsProcessingParameterFeatureSink,
                       QgsProject, QgsProcessing, QgsProcessingParameterField, QgsProcessingParameterCrs)
from qgis.PyQt.QtCore import QCoreApplication, QVariant
import processing

class MinilignesAlgorithm(QgsProcessingAlgorithm):
    INPUT_TAMPONS = 'Nom_couche_tampons'
    INPUT_LIGNES = 'Nom_couche_lignes'
    NOM_CHAMP_OBJ_MATRIC = 'Nom_champ_OBJ_MATRIC'
    SCR = 'SCR'
    OUTPUT = 'Lignes_filtrées'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer(self.INPUT_TAMPONS, self.tr('Couche de tampons'), types=[QgsProcessing.TypeVectorAnyGeometry], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer(self.INPUT_LIGNES, self.tr('Couche de lignes'), types=[QgsProcessing.TypeVectorLine], defaultValue=None))
        self.addParameter(QgsProcessingParameterField(self.NOM_CHAMP_OBJ_MATRIC, self.tr('Champ id unique cana'), None, self.INPUT_LIGNES, QgsProcessingParameterField.Any))
        self.addParameter(QgsProcessingParameterCrs(self.SCR, self.tr('Système de coordonnées de référence'), defaultValue='EPSG:3947'))
        self.addParameter(QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr('Lignes filtrées'), type=QgsProcessing.TypeVectorLine))

    def processAlgorithm(self, parameters, context, feedback):
        couche_tampons = self.parameterAsVectorLayer(parameters, self.INPUT_TAMPONS, context)
        couche_lignes = self.parameterAsVectorLayer(parameters, self.INPUT_LIGNES, context)
        nom_champ_obj_matric = self.parameterAsString(parameters, self.NOM_CHAMP_OBJ_MATRIC, context)
        scr = self.parameterAsCrs(parameters, self.SCR, context)
        obj_matrics_traites = set()

        index_tampons = QgsSpatialIndex()
        for tampon in couche_tampons.getFeatures():
            index_tampons.addFeature(tampon)

        def fusionner_cheminement(obj_matric_depart, geom_depart):
            lignes_a_fusionner = [geom_depart]
            obj_matrics = [obj_matric_depart]
            lignes_visitees = {obj_matric_depart}

            while True:
                ids_tampons_proches = index_tampons.intersects(geom_depart.boundingBox())
                ligne_trouvee = False
                for id_tampon in ids_tampons_proches:
                    tampon = couche_tampons.getFeature(id_tampon)
                    if geom_depart.intersects(tampon.geometry()):
                        for ligne in couche_lignes.getFeatures():
                            obj_matric = ligne[nom_champ_obj_matric]
                            if obj_matric not in lignes_visitees and ligne.geometry().intersects(tampon.geometry()):
                                lignes_a_fusionner.append(ligne.geometry())
                                obj_matrics.append(obj_matric)
                                geom_depart = ligne.geometry()
                                lignes_visitees.add(obj_matric)
                                ligne_trouvee = True
                                break
                        if ligne_trouvee:
                            break
                if not ligne_trouvee:
                    break
            return QgsGeometry.unaryUnion(lignes_a_fusionner), obj_matrics

        couche_resultat = QgsVectorLayer("LineString?crs=" + scr.authid(), "Lignes_Fusionnees", "memory")
        provider = couche_resultat.dataProvider()
        provider.addAttributes([QgsField("Liste_id_cana", QVariant.String)])
        couche_resultat.updateFields()

        for idx, ligne in enumerate(couche_lignes.getFeatures()):
            obj_matric = ligne[nom_champ_obj_matric]
            if obj_matric not in obj_matrics_traites:
                obj_matrics_traites.add(obj_matric)
                ligne_fusionnee, obj_matrics_ligne = fusionner_cheminement(obj_matric, ligne.geometry())
                if not ligne_fusionnee.isEmpty():
                    feature = QgsFeature()
                    feature.setGeometry(ligne_fusionnee)
                    feature.setAttributes([";".join(map(lambda x: str(int(x)) if x.is_integer() else str(x), obj_matrics_ligne))])
                    provider.addFeature(feature)

        couche_lignes_filtrees = QgsVectorLayer("LineString?crs=" + scr.authid(), "Lignes_Filtrees", "memory")
        provider_filtrees = couche_lignes_filtrees.dataProvider()
        provider_filtrees.addAttributes([QgsField("Liste_id_cana", QVariant.String)])
        couche_lignes_filtrees.updateFields()

        identifiants_filtres = set()
        for feature in couche_resultat.getFeatures():
            obj_matric = feature['Liste_id_cana']
            if not any(obj_matric in autre_obj_matric and obj_matric != autre_obj_matric 
                       for autre_feature in couche_resultat.getFeatures() 
                       for autre_obj_matric in [autre_feature['Liste_id_cana']]):
                identifiants_filtres.add(obj_matric)

        identifiants_uniques = set()
        for id_filtre in identifiants_filtres:
            id_trie = ";".join(sorted(id_filtre.split(';')))
            if id_trie not in identifiants_uniques:
                identifiants_uniques.add(id_trie)
                for feature in couche_resultat.getFeatures():
                    if feature['Liste_id_cana'] == id_filtre:
                        provider_filtrees.addFeature(feature)
      
        context.temporaryLayerStore().addMapLayer(couche_lignes_filtrees)
        Lignes_filtrées = processing.run("native:savefeatures", {'INPUT': couche_lignes_filtrees, 'OUTPUT': 'memory:'}, context=context)['OUTPUT']

        QgsProject.instance().addMapLayer(couche_lignes_filtrees)

        return {'Lignes_filtrées': Lignes_filtrées}

    def name(self):
        return 'minilignes'

    def displayName(self):
        return self.tr('Minilignes')

    def group(self):
        return self.tr('Traitement cana')

    def groupId(self):
        return 'Traitement cana'

    def shortHelpString(self):
        return self.tr("Description courte de l'algorithme Minilignes")

    def createInstance(self):
        return MinilignesAlgorithm()

# Enregistrez cette classe avec QgsProcessingAlgorithm
alg = MinilignesAlgorithm()
