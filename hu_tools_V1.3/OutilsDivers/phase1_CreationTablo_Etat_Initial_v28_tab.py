from qgis.PyQt import QtWidgets, uic
from qgis.core import QgsApplication, QgsProject
import processing
import os
from qgis.PyQt.QtWidgets import QMenu, QFileDialog
from qgis.PyQt.QtCore import QPoint
from qgis.PyQt.QtWidgets import QMessageBox

# Import du provider custom
from .Provider_phase1_CreationTablo_Etat_Initial_v28 import Provider_phase1_CreationTablo_EI

# Chargement de l'interface Qt
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'phase1_CreationTablo_Etat_Initial_v28_tab.ui'))


class Phase1_CreationTabloEI_Tab(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, iface=None, parent=None):
        super().__init__(parent)
        self.iface = iface
        self.setupUi(self)
           
        #  Initialisation du provider 
        self.provider = Provider_phase1_CreationTablo_EI()
        registry = QgsApplication.processingRegistry()
        if not any(p.id() == self.provider.id() for p in registry.providers()):
            registry.addProvider(self.provider)

        # Connexions des boutons principaux
        self.bouton_exec.clicked.connect(self.run_model)
        self.bouton_fermer.clicked.connect(self.close)
        self.bouton_lot.clicked.connect(self.run_batch_process)

        # Connexions des boutons de sélection de couches
        self.btn_couche_communes.clicked.connect(lambda: self.ouvrir_fichier_couche(self.couche_communes))
        self.btn_couche_conduites.clicked.connect(lambda: self.ouvrir_fichier_couche(self.couche_conduites))
        self.btn_couche_noeuds.clicked.connect(lambda: self.ouvrir_fichier_couche(self.couche_noeuds))
        self.btn_dossier_sortie.clicked.connect(self.selectionner_dossier_sortie)

        # Connexions des boutons de sortie
        self.btn_stats_noeud.clicked.connect(lambda: self.afficher_menu_sortie(self.btn_stats_noeud, self.stats_noeud))
        self.btn_stats_fosse.clicked.connect(lambda: self.afficher_menu_sortie(self.btn_stats_fosse, self.stats_fosse))
        self.btn_stats_reseau.clicked.connect(lambda: self.afficher_menu_sortie(self.btn_stats_reseau, self.stats_reseau))

        # Peupler les ComboBox au démarrage
        self.populate_layer_comboboxes()

        # Connexion pour mise à jour des champs selon la couche choisie
        #self.couche_noeuds.currentIndexChanged.connect(self.populate_field_lists)
        #self.couche_conduites.currentIndexChanged.connect(self.populate_field_lists)

    # Remplit les ComboBox avec les couches du projet QGIS
    def populate_layer_comboboxes(self):
        """Peuple les listes déroulantes avec les couches vectorielles du projet."""
        for combo in [self.couche_communes, self.couche_conduites, self.couche_noeuds]:
            combo.clear()

        for layer in QgsProject.instance().mapLayers().values():
            if layer.type() == layer.VectorLayer:
                self.couche_communes.addItem(layer.name(), layer.id())
                self.couche_conduites.addItem(layer.name(), layer.id())
                self.couche_noeuds.addItem(layer.name(), layer.id())

    # Ouvre un explorateur pour choisir un fichier de couche
    def ouvrir_fichier_couche(self, combo_box):
        """Permet de choisir un fichier SIG et de l’ajouter à la liste déroulante."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choisir une couche (Shapefile, GeoPackage, etc.)",
            "",
            "Fichiers SIG (*.shp *.gpkg *.geojson *.sqlite *.tab *.kml);;Tous les fichiers (*)"
        )
        if file_path:
            if file_path not in [combo_box.itemText(i) for i in range(combo_box.count())]:
                combo_box.addItem(file_path)
            combo_box.setCurrentText(file_path)

    # Choisir le dossier de sortie
    def selectionner_dossier_sortie(self):
        dossier = QFileDialog.getExistingDirectory(self, "Choisir un dossier de sortie")
        if dossier:
            self.dossier_sortie.setText(dossier)

    # Remplir les champs selon les couches sélectionnées
    #def populate_field_lists(self):
    #    """Met à jour les listes des champs identifiants selon la couche choisie."""
    #    self.identifiant_cana.clear()
    #    self.identifiant_regard.clear()

    #    couche_cana = self.get_layer_by_id(self.couche_conduites.currentData())
    #    couche_regard = self.get_layer_by_id(self.couche_noeuds.currentData())

    #    if couche_cana:
    #        champs = [f.name() for f in couche_cana.fields()]
    #        self.identifiant_cana.addItems(champs)

    #    if couche_regard:
    #        champs = [f.name() for f in couche_regard.fields()]
    #        self.identifiant_regard.addItems(champs)

    # Menu contextuel pour les sorties
    def afficher_menu_sortie(self, bouton, champ_ligne):
        """Affiche un menu contextuel pour choisir le type de sortie."""
        menu = QMenu(self)
        action_temp = menu.addAction("Créer une couche temporaire")
        action_fichier = menu.addAction("Enregistrer vers un fichier…")
        action_gpkg = menu.addAction("Enregistrer dans un GeoPackage…")

        action = menu.exec_(bouton.mapToGlobal(QPoint(0, bouton.height())))

        if action == action_temp:
            champ_ligne.setText("TEMPORARY_OUTPUT")
        elif action == action_fichier:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Enregistrer la couche sous...",
                "", "Fichiers SIG (*.shp *.geojson *.gpkg *.sqlite);;Tous les fichiers (*)"
            )
            if file_path:
                champ_ligne.setText(file_path)
        elif action == action_gpkg:
            gpkg_path, _ = QFileDialog.getSaveFileName(
                self, "Créer un GeoPackage",
                "", "GeoPackage (*.gpkg)"
            )
            if gpkg_path:
                champ_ligne.setText(gpkg_path)

    # Récupération de la couche par ID
    def get_layer_by_id(self, layer_id):
        return QgsProject.instance().mapLayer(layer_id)

    # Lancer le traitement
    def run_model(self):
        """Exécute le modèle Synthèse Terrain SDGEP."""
        try:
            couche_conduites = self.get_layer_by_id(self.couche_conduites.currentData())
            couche_noeuds = self.get_layer_by_id(self.couche_noeuds.currentData())

            if not couche_conduites or not couche_noeuds:
                QMessageBox.warning(self, "Erreur", "Veuillez sélectionner les couches de conduites et de noeuds.")
                return

            params = {
                'COUCHE_COMMUNES': self.get_layer_by_id(self.couche_communes.currentData()),
                'COUCHE_CONDUITES': couche_conduites,
                'COUCHE_NOEUDS': couche_noeuds,
                #'IDENTIFIANT_CANA': self.identifiant_cana.currentText(),
                #'IDENTIFIANT_REGARD': self.identifiant_regard.currentText(),
                'DOSSIER_SORTIE': self.dossier_sortie.text(),
                'STATS_NOEUD': self.stats_noeud.text(),
                'STATS_FOSSE': self.stats_fosse.text(),
                'STATS_RESEAU': self.stats_reseau.text()
            }

            self.barre_progression.setValue(0)
            result = processing.run('syntheseterrain_sdgep:SyntheseTerrain_SDgep', params)
            self.barre_progression.setValue(100)

            # Ajout des couches de sortie
            for key, output_path in result.items():
                if output_path:
                    self.iface.addVectorLayer(output_path, key.replace('_', ' '), 'ogr')

            QMessageBox.information(self, "Succès", "Le modèle a été exécuté avec succès !")

        except Exception as e:
            QMessageBox.critical(self, "Erreur d’exécution", str(e))

    # Mode batch
    def run_batch_process(self):
        QMessageBox.information(
            self,
            "Batch non implémenté",
            "La fonction 'Exécuter comme processus de lot' n’est pas encore disponible."
        )
