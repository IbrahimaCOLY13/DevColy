from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterField,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterCrs,
                       QgsField,
                       QgsFeature,
                       QgsWkbTypes,
                       QgsGeometry,
                       QgsProject,
                       QgsFeatureSink,
                       QgsFields,
                       QgsCoordinateTransform,
                       QgsCoordinateReferenceSystem)
from qgis.PyQt.QtCore import QVariant, Qt
from qgis import processing

class LineToPointAttributeTransfer(QgsProcessingAlgorithm):
    INPUT_LINE_LAYER = 'INPUT_LINE_LAYER'
    INPUT_POINT_LAYER = 'INPUT_POINT_LAYER'
    POINT_FIELD = 'POINT_FIELD'
    SEARCH_DISTANCE = 'SEARCH_DISTANCE'
    OUTPUT_LAYER = 'OUTPUT_LAYER'
    OUTPUT_CRS = 'OUTPUT_CRS'  # Ajout d'un nouvel attribut pour le SCR de sortie
    SCRIPT_DESCRIPTION = 'SCRIPT_DESCRIPTION'  # Nouvel attribut pour le champ de commentaire


    def tr(self, string):
        return string

    def createInstance(self):
        return LineToPointAttributeTransfer()

    def name(self):
        return 'Ajout id regard amont et aval'

    def displayName(self):
        return self.tr('Ajout id regard amont et aval')

    def group(self):
        return self.tr('Traitement cana')

    def groupId(self):
        return 'Traitement cana'

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSource(
            self.INPUT_LINE_LAYER, 
            self.tr('Couche canalisation'), 
            [QgsProcessing.TypeVectorLine]))

        self.addParameter(QgsProcessingParameterFeatureSource(
            self.INPUT_POINT_LAYER, 
            self.tr('Couche regard'), 
            [QgsProcessing.TypeVectorPoint]))

        self.addParameter(QgsProcessingParameterField(
            self.POINT_FIELD, 
            self.tr('Champ id regard'), 
            parentLayerParameterName=self.INPUT_POINT_LAYER))

        self.addParameter(QgsProcessingParameterNumber(
            self.SEARCH_DISTANCE,
            self.tr('Distance de recherche au bout des lignes'),
            QgsProcessingParameterNumber.Double,
            defaultValue=0.2))

        self.addParameter(QgsProcessingParameterFeatureSink(
            self.OUTPUT_LAYER, 
            self.tr('Couche de sortie')))
            
        self.addParameter(QgsProcessingParameterCrs(
            self.OUTPUT_CRS,
            self.tr('Choix du SCR de sortie'),
            defaultValue=QgsProject.instance().crs().authid()))
            

    def processAlgorithm(self, parameters, context, feedback):
        lineLayer = self.parameterAsVectorLayer(parameters, self.INPUT_LINE_LAYER, context)
        pointLayer = self.parameterAsVectorLayer(parameters, self.INPUT_POINT_LAYER, context)
        pointField = self.parameterAsString(parameters, self.POINT_FIELD, context)
        searchDistance = self.parameterAsDouble(parameters, self.SEARCH_DISTANCE, context)
        outputCrs = self.parameterAsCrs(parameters, self.OUTPUT_CRS, context)

        # Créer un objet de transformation de coordonnées pour les deux couches
        lineTransform = QgsCoordinateTransform(lineLayer.sourceCrs(), outputCrs, QgsProject.instance())
        pointTransform = QgsCoordinateTransform(pointLayer.sourceCrs(), outputCrs, QgsProject.instance())

        fields = QgsFields(lineLayer.fields())
        fields.append(QgsField('regard_amont', QVariant.String))
        fields.append(QgsField('regard_aval', QVariant.String))

        (sink, dest_id) = self.parameterAsSink(parameters, self.OUTPUT_LAYER, context,
                                               fields, QgsWkbTypes.LineString, outputCrs)

        for lineFeature in lineLayer.getFeatures():
            lineGeom = lineFeature.geometry()
            if not lineGeom or lineGeom.isNull():
                feedback.pushInfo(f'Ignoring null or invalid geometry for feature {lineFeature.id()}')
                continue

            # Transformer la géométrie de la ligne
            lineGeom.transform(lineTransform)

            # Trouver les points les plus proches avec les géométries transformées
            startPoint, endPoint = self.getTransformedLineEnds(lineGeom)
            nearestStartId = self.findNearestFeatureId(startPoint, pointLayer, pointField, searchDistance, pointTransform)
            nearestEndId = self.findNearestFeatureId(endPoint, pointLayer, pointField, searchDistance, pointTransform)

            newFeature = QgsFeature(fields)
            newFeature.setGeometry(lineGeom)
            for field in lineLayer.fields():
                newFeature[field.name()] = lineFeature[field.name()]

            newFeature['regard_amont'] = nearestStartId
            newFeature['regard_aval'] = nearestEndId
            sink.addFeature(newFeature, QgsFeatureSink.FastInsert)

        return {self.OUTPUT_LAYER: dest_id}

    def getTransformedLineEnds(self, lineGeom):
        if lineGeom.isMultipart():
            lineString = lineGeom.asMultiPolyline()
            startPoint = QgsGeometry.fromPointXY(lineString[0][0])
            endPoint = QgsGeometry.fromPointXY(lineString[-1][-1])
        else:
            lineString = lineGeom.asPolyline()
            startPoint = QgsGeometry.fromPointXY(lineString[0])
            endPoint = QgsGeometry.fromPointXY(lineString[-1])
        return startPoint, endPoint

    def findNearestFeatureId(self, pointGeom, pointLayer, pointField, maxDistance, transform):
        nearestId = None
        minDistance = float('inf')
        for pointFeature in pointLayer.getFeatures():
            pointGeom.transform(transform)
            distance = pointGeom.distance(pointFeature.geometry())
            if distance < minDistance and distance <= maxDistance:
                minDistance = distance
                nearestId = pointFeature[pointField]
        return nearestId
