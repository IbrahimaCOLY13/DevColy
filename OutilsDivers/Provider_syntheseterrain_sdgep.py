from qgis.core import (
    QgsProcessingProvider,
    QgsMessageLog,
    Qgis
)
from .syntheseterrain_sdgep import Syntheseterrain_sdgep_v3

class Provider_SyntheseTerrain_sdgep(QgsProcessingProvider):
    def loadAlgorithms(self):
        try:
            self.addAlgorithm(Syntheseterrain_sdgep_v3())
        except Exception as e:
            QgsMessageLog.logMessage(
                f"Erreur lors du chargement de syntheseTerrain_SDGEP : {e}",
                'HU_tools',
                level=Qgis.Critical
            )

    def id(self):
        return 'syntheseterrain_sdgep'

    def name(self):
        return 'syntheseTerrain_SDGEP'
        
    
