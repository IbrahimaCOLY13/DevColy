from qgis.core import (
    QgsProcessingProvider,
    QgsMessageLog,
    Qgis
)
from qgis.PyQt.QtGui import QIcon
import os
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
    
    def longName(self):
        return 'Enregistrer les Styles des Couches'
    
    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), '..', 'icon1.png'))
        
    
