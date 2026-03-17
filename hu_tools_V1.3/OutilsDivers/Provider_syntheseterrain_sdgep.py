from qgis.core import (
    QgsProcessingProvider,
    QgsMessageLog,
    Qgis
)
from qgis.PyQt.QtGui import QIcon
import os
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
    
    def longName(self):
        return 'Synthèse Terrain SDGEP'
    
    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), '..', 'icon1.png'))
        
    
