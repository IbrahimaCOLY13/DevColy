from qgis.core import (
    QgsProcessingProvider,
    QgsMessageLog,
    Qgis
)
from .Save_styles import EnregistrerStylesCouches

class Provider_EnregistrerStylesCouches(QgsProcessingProvider):
    def loadAlgorithms(self):
        try:
            self.addAlgorithm(EnregistrerStylesCouches())
        except Exception as e:
            QgsMessageLog.logMessage(
                f"Erreur lors du chargement de EnregistrerStylesCouches : {e}",
                'HU_tools',
                level=Qgis.Critical
            )

    def id(self):
        return 'enregistrerstyle'

    def name(self):
        return 'EnregistrerStyles'
        
    
