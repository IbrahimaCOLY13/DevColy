from qgis.core import (
    QgsProcessingProvider,
    QgsMessageLog,
    Qgis
)
from qgis.PyQt.QtGui import QIcon
import os
from .Synthese_champs_EDV import Synthese_champs_EDV

class Provider_synthese_champsEDV(QgsProcessingProvider):
    def loadAlgorithms(self):
        try:
            self.addAlgorithm(Synthese_champs_EDV())
        except Exception as e:
            QgsMessageLog.logMessage(
                f"Erreur lors du chargement de Synthese_champs_EDV : {e}",
                'HU_tools',
                level=Qgis.Critical
            )

    def id(self):
        return 'edv2'

    def name(self):
        return 'EDV'
    
    def longName(self):
        return 'Synthèse Champs EDV'
    
    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), '..', 'icon1.png'))
