from qgis.core import QgsProject, QgsVectorLayer, QgsRasterLayer
import os
import shutil
import re
import glob
import tempfile
from urllib.parse import unquote
from qgis.PyQt.QtWidgets import QMessageBox, QFileDialog, QProgressDialog, QStyledItemDelegate, QComboBox


def exporter_projet_local(destination_folder):
    """
    Exporte le projet QGIS courant avec toutes ses couches (vecteurs/raster)
    en version locale dans un dossier choisi par l'utilisateur.
    Remplace les fichiers existants si nécessaire.
    """

    # Crée un dossier temporaire pour éviter de bloquer les fichiers ouverts
    temp_folder = tempfile.mkdtemp()

    # Création des sous-dossiers dans le dossier temporaire
    layers_folder = os.path.join(temp_folder, "layers")
    styles_folder = os.path.join(temp_folder, "styles")
    os.makedirs(layers_folder, exist_ok=True)
    os.makedirs(styles_folder, exist_ok=True)

    # Fonction utilitaire : nettoyage du nom de fichier
    def clean_filename(filename):
        return re.sub(r'[<>:"/\\|?*]', "_", filename)

    #  AJOUT : vérifie si le projet est déjà enregistré 
    project = QgsProject.instance()
    if not project.fileName():
        # Propose un enregistrement si le projet n’a jamais été sauvegardé
        project_file, _ = QFileDialog.getSaveFileName(
            None,
            "Enregistrer le projet avant export",
            "",
            "QGIS Projects (*.qgz *.qgs)"
        )
        if not project_file:
            QMessageBox.warning(None, "Export annulé", "Veuillez enregistrer le projet avant d’exporter.")
            return
        project.write(project_file)

    project_path = project.fileName()
    nom_projet = clean_filename(os.path.basename(project_path))

    # Fonction utilitaire : extraction du vrai chemin d'une couche
    def get_clean_layer_path(layer):
        raw_path = layer.source().split("|")[0].split("?")[0]
        if raw_path.lower().startswith("file:///"):
            raw_path = raw_path[8:]
        return unquote(raw_path)

    # Récupération du projet courant
    project = QgsProject.instance()
    project_path = project.fileName()
    nom_projet = clean_filename(os.path.basename(project_path))

    # Création du nom du nouveau projet
    name, ext = os.path.splitext(nom_projet)
    nom_projet_local = f"{name}_local{ext}"  # ex: projet_local.qgz
    new_project_path = os.path.join(temp_folder, nom_projet_local)

    # Copie du fichier projet original dans le dossier temporaire
    shutil.copy(project_path, new_project_path)

    # Dictionnaire pour correspondance ancien chemin => nouveau chemin
    layer_path_map = {}

    # Parcours de toutes les couches du projet
    for layer in project.mapLayers().values():
        layer_name = clean_filename(layer.name())
        provider = layer.providerType().lower()
        source = layer.source()

        # Ignorer les couches distantes (WMS, WFS, HTTP) ou temporaires
        if provider in ["wms", "wfs"] or source.lower().startswith("http") or source.lower().startswith("memory?"):
            print(f"Ignoré (couche distante ou en mémoire) : {layer_name}")
            continue

        # Récupère le vrai chemin du fichier source
        layer_path = get_clean_layer_path(layer)
        new_layer_path = ""

        # CAS 1 : couche vecteur
        if isinstance(layer, QgsVectorLayer):
            ext = os.path.splitext(layer_path)[1].lower()

            # Si shapefile → copier tous les fichiers associés (.dbf, .shx, .prj, etc.)
            if ext == ".shp":
                for file in glob.glob(layer_path.replace(".shp", ".*")):
                    shutil.copy(file, layers_folder)
                new_layer_path = os.path.join(layers_folder, os.path.basename(layer_path))
            else:
                # Sinon (GeoPackage, CSV, etc.) => copie directe du fichier
                new_layer_path = os.path.join(layers_folder, layer_name + ext)
                shutil.copy(layer_path, new_layer_path)

            # Sauvegarde du style QML associé
            qml_path = os.path.join(styles_folder, layer_name + ".qml")
            layer.saveNamedStyle(qml_path)
            print(f"Exporté : {new_layer_path} + style {qml_path}")

        # CAS 2 : couche raster
        elif isinstance(layer, QgsRasterLayer):
            ext = os.path.splitext(layer_path)[1].lower()
            new_layer_path = os.path.join(layers_folder, layer_name + ext)
            shutil.copy(layer_path, new_layer_path)
            print(f"Exporté : {new_layer_path}")

        # Enregistrer la correspondance ancien => nouveau chemin
        if new_layer_path:
            layer_path_map[source] = new_layer_path

    # Mise à jour des chemins dans le projet
    for layer in project.mapLayers().values():
        if layer.source() in layer_path_map:
            new_layer_path = layer_path_map[layer.source()]
            layer.setDataSource(new_layer_path, layer.name(), layer.providerType())

            # Réapplique le style
            qml_path = os.path.join(styles_folder, clean_filename(layer.name()) + ".qml")
            if os.path.exists(qml_path):
                layer.loadNamedStyle(qml_path)
                layer.triggerRepaint()
                print(f"Style réappliqué : {qml_path}")

    # Sauvegarde finale du projet dans le dossier temporaire
    project.write(new_project_path)
    print(f"Projet sauvegardé temporairement : {new_project_path}")

    # Copie finale vers le dossier destination (remplacement des fichiers existants)
    for item in os.listdir(temp_folder):
        src_path = os.path.join(temp_folder, item)
        dst_path = os.path.join(destination_folder, item)

        if os.path.isdir(src_path):
            if os.path.exists(dst_path):
                # Supprime seulement les fichiers et dossiers avec même nom
                for sub_item in os.listdir(src_path):
                    sub_src = os.path.join(src_path, sub_item)
                    sub_dst = os.path.join(dst_path, sub_item)
                    if os.path.isdir(sub_src):
                        if os.path.exists(sub_dst):
                            shutil.rmtree(sub_dst)
                        shutil.copytree(sub_src, sub_dst)
                    else:
                        shutil.copy2(sub_src, sub_dst)
            else:
                shutil.copytree(src_path, dst_path)
        else:
            shutil.copy2(src_path, dst_path)

    print(f"Projet exporté et remplacé dans : {destination_folder}")
