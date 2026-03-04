from qgis.core import (
    QgsProcessingProvider,
    QgsMessageLog,
    Qgis
)
from qgis.PyQt.QtGui import QIcon
import os
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
    
    def longName(self):
        return 'Liaison Mini-Cana'
    
    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), '..', 'icon1.png'))
        
    
