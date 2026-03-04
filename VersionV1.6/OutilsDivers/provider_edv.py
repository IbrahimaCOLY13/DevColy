from qgis.core import (
    QgsProcessingProvider,
    QgsMessageLog,
    Qgis
)
from .Bilanclasstopo import Statistiques_SDAEU_v4

class ProviderEDV(QgsProcessingProvider):
    def loadAlgorithms(self):
        try:
            self.addAlgorithm(Statistiques_SDAEU_v4())
        except Exception as e:
            QgsMessageLog.logMessage(
                f"Erreur lors du chargement de Statistiques_SDAEU_v4 : {e}",
                'HU_tools',
                level=Qgis.Critical
            )

    def id(self):
        return 'edv'

    def name(self):
        return 'EDV'
