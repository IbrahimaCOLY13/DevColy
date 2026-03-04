from qgis.PyQt import QtWidgets, uic
from qgis.core import QgsApplication
import processing
import os

# Importer le provider (qui enregistre le modèle)
from .Provider_PresentationSIG import Provider_presentationSIG

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'presentationSIG_tab.ui'))

class PresentationSIGTab(QtWidgets.QWidget, FORM_CLASS):
    def __init__(self, iface=None, parent=None):
        super().__init__(parent)
        self.iface = iface
        self.setupUi(self)

        # Connexions des boutons
        self.btn_logo_browse.clicked.connect(self.select_logo_path)
        self.btn_run_model.clicked.connect(self.run_model)

        # Ajouter le provider si nécessaire
        self.provider = Provider_presentationSIG()
        registry = QgsApplication.processingRegistry()
        if not any(p.id() == self.provider.id() for p in registry.providers()):
            registry.addProvider(self.provider)

    def select_logo_path(self):
        """Ouvre une boîte de dialogue pour choisir un logo."""
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Sélectionner le logo", "",
            "Images (*.png *.jpg *.jpeg *.svg);;Tous les fichiers (*.*)"
        )
        if file_path:
            self.line_logo_path.setText(file_path)

    def run_model(self):
        try:
            # Préparer les paramètres
            params = {
                'maitre_douvrage': self.line_maitre_ouvrage.text(),
                'commune_de_': self.line_commune.text(),
                'titre': self.line_titre.text(),
                'chemin_du_logo': self.line_logo_path.text()
            }

            # Exécuter le modèle via l'ID complet : provider_id:algorithm_id
            processing.run('presentationSig:PresentationSIG', params)

            QtWidgets.QMessageBox.information(self, "Succès", "Le modèle a été exécuté avec succès !")

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erreur d’exécution", str(e))
