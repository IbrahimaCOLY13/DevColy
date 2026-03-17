from qgis.core import (
    QgsProcessingProvider,
    QgsMessageLog,
    Qgis
)
from qgis.PyQt.QtGui import QIcon
import os
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
    
    def longName(self):
        return 'Présentation SIG'
    
    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), '..', 'icon1.png'))
        
    
