from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterField,
                       QgsProcessingParameterString,
                       QgsProcessingParameterFeatureSink,
                       QgsFeatureSink,
                       QgsFeature,
                       QgsField,
                       QgsFields)
from qgis.PyQt.QtCore import QVariant

class CollectLineIdsForPoints(QgsProcessingAlgorithm):
    INPUT_LINE_LAYER = 'INPUT_LINE_LAYER'
    INPUT_POINT_LAYER = 'INPUT_POINT_LAYER'
    POINT_FIELD = 'POINT_FIELD'
    LINE_FIELD = 'LINE_FIELD'
    LINE_ID_FIELD = 'LINE_ID_FIELD'
    NEW_FIELD_NAME = 'NEW_FIELD_NAME'
    OUTPUT_LAYER = 'OUTPUT_LAYER'

    def tr(self, string):
        return string

    def createInstance(self):
        return CollectLineIdsForPoints()

    def name(self):
        return 'Collecte canalisation IDs dans regards'

    def displayName(self):
        return self.tr('Collecte canalisation IDs dans regards')

    def group(self):
        return self.tr('Traitement point')

    def groupId(self):
        return 'Traitement point'

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSource(
            self.INPUT_POINT_LAYER,
            self.tr('Couche de regard'),
            [QgsProcessing.TypeVectorPoint]
        ))
        self.addParameter(QgsProcessingParameterField(
            self.POINT_FIELD,
            self.tr('Champs identifiant unique des regards'),
            parentLayerParameterName=self.INPUT_POINT_LAYER
        ))

        self.addParameter(QgsProcessingParameterFeatureSource(
            self.INPUT_LINE_LAYER,
            self.tr('Couche de canalisation'),
            [QgsProcessing.TypeVectorLine]
        ))
        self.addParameter(QgsProcessingParameterField(
            self.LINE_ID_FIELD,
            self.tr('Champs identifiant unique des canalisations'),
            parentLayerParameterName=self.INPUT_LINE_LAYER
        ))
        self.addParameter(QgsProcessingParameterField(
            self.LINE_FIELD,
            self.tr('Champs regard dans la couche ligne'),
            parentLayerParameterName=self.INPUT_LINE_LAYER
        ))

        self.addParameter(QgsProcessingParameterString(
            self.NEW_FIELD_NAME,
            self.tr('Nom du nouveau champ'),
            defaultValue='list_id_cana'
        ))

        self.addParameter(QgsProcessingParameterFeatureSink(
            self.OUTPUT_LAYER,
            self.tr('Liste de canalisation ajoutée')
        ))

    def processAlgorithm(self, parameters, context, feedback):
        pointLayer = self.parameterAsVectorLayer(parameters, self.INPUT_POINT_LAYER, context)
        lineLayer = self.parameterAsVectorLayer(parameters, self.INPUT_LINE_LAYER, context)
        pointField = self.parameterAsString(parameters, self.POINT_FIELD, context)
        lineField = self.parameterAsString(parameters, self.LINE_FIELD, context)
        lineIdField = self.parameterAsString(parameters, self.LINE_ID_FIELD, context)
        newFieldName = self.parameterAsString(parameters, self.NEW_FIELD_NAME, context)

        fields = QgsFields(pointLayer.fields())
        fields.append(QgsField(newFieldName, QVariant.String))

        (sink, dest_id) = self.parameterAsSink(parameters, self.OUTPUT_LAYER, context,
                                               fields, pointLayer.wkbType(), pointLayer.sourceCrs())

        for pointFeature in pointLayer.getFeatures():
            pointValue = self.realToString(pointFeature[pointField])
            matchingLineIds = []

            for line in lineLayer.getFeatures():
                if self.realToString(line[lineField]) == pointValue:
                    matchingLineIds.append(self.realToString(line[lineIdField]))

            newFeature = QgsFeature(fields)
            newFeature.setGeometry(pointFeature.geometry())
            for field in pointLayer.fields():
                newFeature[field.name()] = pointFeature[field.name()]

            newFeature[newFieldName] = ';'.join(matchingLineIds)
            sink.addFeature(newFeature, QgsFeatureSink.FastInsert)

        return {self.OUTPUT_LAYER: dest_id}

    def realToString(self, value):
        """ Convertit un réel en chaîne de caractères sans '.0' si c'est un entier. """
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        else:
            return str(value)
