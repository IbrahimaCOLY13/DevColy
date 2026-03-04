from qgis.core import (
    QgsProcessingProvider,
    QgsMessageLog,
    Qgis
)
from .LiaisonminiCana import LiaisonMinicana

class Provider_liaisonminicana(QgsProcessingProvider):
    def loadAlgorithms(self):
        try:
            self.addAlgorithm(LiaisonMinicana())
        except Exception as e:
            QgsMessageLog.logMessage(
                f"Erreur lors du chargement de Liaison Minicana : {e}",
                'HU_tools',
                level=Qgis.Critical
            )

    def id(self):
        return 'liaisonminicana'

    def name(self):
        return 'LiaisonMinicana'
        
    
