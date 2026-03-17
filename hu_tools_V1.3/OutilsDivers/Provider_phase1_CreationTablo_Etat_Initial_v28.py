from qgis.core import (
    QgsProcessingProvider,
    QgsMessageLog,
    Qgis
)
from qgis.PyQt.QtGui import QIcon
import os
from .phase1_CreationTablo_Etat_Initial_v28 import Phase1_creationtablo_etat_initial_v28

class Provider_phase1_CreationTablo_EI(QgsProcessingProvider):
    def loadAlgorithms(self):
        try:
            self.addAlgorithm(Phase1_creationtablo_etat_initial_v28())
        except Exception as e:
            QgsMessageLog.logMessage(
                f"Erreur lors du chargement de Phase1_creationtablo_etat_initial_v28 : {e}",
                'HU_tools',
                level=Qgis.Critical
            )

    def id(self):
        return 'phase1_creationtablo_etat_initial_v28'

    def name(self):
        return 'phase1_CréationTablo_Etat_Initial_v28'
    
    def longName(self):
        return 'Phase 1 - Création Tableau État Initial v28'
    
    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), '..', 'icon1.png'))
        
    
