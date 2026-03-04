from qgis.PyQt import QtWidgets, uic
from qgis.core import QgsApplication, QgsProject
import processing
import os
from qgis.PyQt.QtWidgets import QMenu, QFileDialog
from qgis.PyQt.QtCore import QPoint
from qgis.PyQt.QtWidgets import QMessageBox

# Import du provider custom
from .Provider_LiaisonMiniCana import Provider_liaisonminicana

# Chargement de l'interface Qt
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'liaisonminicana_tab.ui'))


class LiaisonminiCanaTab(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, iface=None, parent=None):
        super().__init__(parent)
        self.iface = iface
        self.setupUi(self)
        
        
        #  Initialisation du provider 
        self.provider = Provider_liaisonminicana()
        registry = QgsApplication.processingRegistry()
        if not any(p.id() == self.provider.id() for p in registry.providers()):
            registry.addProvider(self.provider)

        #  Connexions des signaux 
        self.btn_execute.clicked.connect(self.run_model)
        self.btn_close.clicked.connect(self.close)
        self.btn_batch.clicked.connect(self.run_batch_process)
        
        # Connexions des boutons des couches de sortie
        self.btn_attention.clicked.connect(lambda: self.afficher_menu_sortie(self.btn_attention, self.line_attention))
        self.btn_croisement.clicked.connect(lambda: self.afficher_menu_sortie(self.btn_croisement, self.line_croisement))
        self.btn_relation.clicked.connect(lambda: self.afficher_menu_sortie(self.btn_relation, self.line_relation))
        self.btn_double.clicked.connect(lambda: self.afficher_menu_sortie(self.btn_double, self.line_double))
        self.btn_couche_cana.clicked.connect(lambda: self.ouvrir_fichier_couche(self.combo_couche_cana))
        self.btn_couche_regard.clicked.connect(lambda: self.ouvrir_fichier_couche(self.combo_regard))
        #self.btn_couche_regard.clicked.connect(lambda: self.ouvrir_fichier_couche(self.combo_couche_regard))

        #  pour Peupler les ComboBox au démarrage 
        self.populate_layer_comboboxes()

        #  Connexion pour mise à jour des champs 
        self.combo_regard.currentIndexChanged.connect(self.populate_fields_regard)
        self.combo_couche_cana.currentIndexChanged.connect(self.populate_fields_regard)

    # -
    # Peupler les ComboBox avec les couches du projet QGIS
    # -
    def populate_layer_comboboxes(self):
        """Remplit la liste déroulante des couches avec celles du projet."""
        self.combo_regard.clear()
        self.combo_couche_cana.clear()

        for layer in QgsProject.instance().mapLayers().values():
            if layer.type() == layer.VectorLayer:
                self.combo_regard.addItem(layer.name(), layer.id())
                self.combo_couche_cana.addItem(layer.name(), layer.id())
                

    def ouvrir_fichier_couche(self, combo_box):
        """Ouvre un explorateur pour choisir un fichier de couche et l'ajoute au combo."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choisir une couche (Shapefile, GeoPackage, etc.)",
            "",
            "Fichiers SIG (*.shp *.gpkg *.geojson *.sqlite *.tab *.kml);;Tous les fichiers (*)"
        )
        if file_path:
            # Ajoute le fichier dans le combo s'il n'y est pas déjà
            if file_path not in [combo_box.itemText(i) for i in range(combo_box.count())]:
                combo_box.addItem(file_path)
            combo_box.setCurrentText(file_path)

    # -
    # Remplir la liste des champs d'après la couche regard et la couche cana
    # -
    def populate_fields_regard(self):
        """Remplit les champs d'identifiants une fois la couche regard choisie."""
        layer_rg = self.get_layer_by_id(self.combo_regard.currentData())
        layer_cn = self.get_layer_by_id(self.combo_couche_cana.currentData())
        self.combo_id_cana.clear()
        self.combo_id_regard.clear()

        if layer_rg:
            field_names = [f.name() for f in layer_rg.fields()]
            self.combo_id_regard.addItems(field_names)
        if layer_cn:
            field_names = [f.name() for f in layer_cn.fields()]
            self.combo_id_cana.addItems(field_names)

    def afficher_menu_sortie(self, bouton, champ_ligne):
        """Affiche un menu contextuel pour choisir le type de couche de sortie."""
        menu = QMenu(self)

        action_temp = menu.addAction("Créer une couche temporaire")
        action_fichier = menu.addAction("Enregistrer vers un fichier…")
        action_gpkg = menu.addAction("Enregistrer dans un GeoPackage…")

        action = menu.exec_(bouton.mapToGlobal(QPoint(0, bouton.height())))

        if action == action_temp:
            champ_ligne.setText("TEMPORARY_OUTPUT")

        elif action == action_fichier:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Enregistrer la couche sous...",
                "",
                "Fichiers SIG (*.shp *.geojson *.gpkg *.sqlite);;Tous les fichiers (*)"
            )
            if file_path:
                champ_ligne.setText(file_path)

        elif action == action_gpkg:
            gpkg_path, _ = QFileDialog.getSaveFileName(
                self,
                "Créer un GeoPackage",
                "",
                "GeoPackage (*.gpkg)"
            )
            if gpkg_path:
                champ_ligne.setText(gpkg_path)

    # -
    # Récupérer une couche par son ID
    # -
    def get_layer_by_id(self, layer_id):
        """Retourne une couche à partir de son ID."""
        return QgsProject.instance().mapLayer(layer_id)

    # -
    # Lancer le modèle
    # -
    def run_model(self):
        """Exécute le modèle 'liaisonminicana:LiaisonMinicana'."""
        try:
            # Récupération de la couche regard
            layer_regard = self.get_layer_by_id(self.combo_regard.currentData())
            # Récupération de la couche cana
            #layer_cana = self.get_layer_by_id(self.combo_couche_cana.currentData())
            if not layer_regard:
                QtWidgets.QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une couche de regard.")
                return
            #if not layer_cana:
            #    QtWidgets.QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une couche de cana.")
            #    return

            identifiant_cana = self.combo_id_cana.currentText()
            identifiant_regard = self.combo_id_regard.currentText()

            # Paramètres du modèle (adaptés à ton provider)
            params = {
                'couche_de_regard': layer_regard,
                'identifiant_unique_cana': identifiant_cana,
                'identifiant_unique_regard': identifiant_regard,
                'OUTPUT_Attention_croisement': 'TEMPORARY_OUTPUT',
                'Couche_regard_complétée_avec_croisement': 'TEMPORARY_OUTPUT',
                'Relation_cana-regard_sans_croisement': 'TEMPORARY_OUTPUT',
                'Cana_en_double': 'TEMPORARY_OUTPUT'
            }

            # Lancer le traitement
            self.progressBar.setValue(0)
            result = processing.run('liaisonminicana:LiaisonMinicana', params)
            self.progressBar.setValue(100)

            # Charger les couches de sortie
            for key, output_path in result.items():
                if output_path:
                    self.iface.addVectorLayer(output_path, key.replace('_', ' '), 'ogr')

            QtWidgets.QMessageBox.information(
                self, "Succès", "Le modèle Liaison Minicana a été exécuté avec succès !"
            )

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erreur d’exécution", str(e))

    # -
    # Lancer le traitement en mode batch (placeholder)
    # -
    def run_batch_process(self):
        QtWidgets.QMessageBox.information(
            self,
            "Batch non implémenté",
            "La fonction 'Exécuter comme processus de lot' n’est pas encore disponible."
        )
