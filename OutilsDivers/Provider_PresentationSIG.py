from qgis.core import (
    QgsProcessingProvider,
    QgsMessageLog,
    Qgis
)
from .Presentation_SIG import PresentationSig

class Provider_presentationSIG(QgsProcessingProvider):
    def loadAlgorithms(self):
        try:
            self.addAlgorithm(PresentationSig())
        except Exception as e:
            QgsMessageLog.logMessage(
                f"Erreur lors du chargement de PresentationSig : {e}",
                'HU_tools',
                level=Qgis.Critical
            )

    def id(self):
        return 'presentationSig'

    def name(self):
        return 'PrésentationSIG'
        
    
