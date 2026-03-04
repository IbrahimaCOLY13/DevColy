import os
from qgis.core import (
    QgsProject, QgsCoordinateReferenceSystem,
    QgsCoordinateTransform, QgsVectorLayer
)
import processing

# ================================
# PARAMÈTRES GÉNÉRAUX
# ================================
NOM_EMPRISE    = "OSM 77176"  # Nom de la couche emprise dans ton projet QGIS
STYLE_DIR      = r"O:\HU\Fonctionnement\06_SDAEU\Procedure_SDAEU\10_SIG\04_SYMBOLOGIE\00_CADASTRE"
DOSSIER_SORTIE = r"O:\HU\Projets\24-59-HU_SDAEU_ARD_TMVL_LOT1\05_SIG\Modélisation\Cadastre"

# Dictionnaire : nom interne -> (typename WFS, fichier de style QML, source WFS)
COUCHES = {
    "parcelle": ("CADASTRALPARCELS.PARCELLAIRE_EXPRESS:parcelle", "parcelle.qml", "geopf"),
    "bati": ("BDTOPO_V3:batiment", "bâti.qml", "geopf"),
    "rue": ("BDTOPO_V3:voie_nommee", "rue.qml", "geopf"),
    "cours_eau": ("BDTOPO_V3:surface_hydrographique", "courseau.qml", "geopf"),
    "cours_eau_etiquette": ("sa:CoursEau_FXX_Topage2022", "cours_eau_etiquette.qml", "sandre"),
    "adresse": ("BAN.DATA.GOUV:ban", "adresse.qml", "geopf"),
    "commune": ("ADMINEXPRESS-COG.LATEST:commune", "commune.qml", "geopf"),
}

proj = QgsProject.instance()

# ================================
# CALCUL DE L’EMPRISE (EPSG:2154)
# ================================
emp_list = proj.mapLayersByName(NOM_EMPRISE)
if not emp_list:
    raise Exception(f" Couche '{NOM_EMPRISE}' introuvable dans le projet.")
emp = emp_list[0]

crs2154 = QgsCoordinateReferenceSystem("EPSG:2154")
xf2154 = QgsCoordinateTransform(emp.crs(), crs2154, proj)
ext = emp.extent()
xmin2154, ymin2154 = xf2154.transform(ext.xMinimum(), ext.yMinimum())
xmax2154, ymax2154 = xf2154.transform(ext.xMaximum(), ext.yMaximum())
bbox2154 = f"{xmin2154},{ymin2154},{xmax2154},{ymax2154},EPSG:2154"

print("BBox utilisée :", bbox2154)

# ================================
# BOUCLE SUR CHAQUE COUCHE
# ================================
for nom, (typename, qml, source) in COUCHES.items():
    print(f"\n--- Traitement {nom} ({typename}) ---")

    # Sélection du service WFS
    if source == "sandre":
        base_url = "https://services.sandre.eaufrance.fr/geo/sandre"
    else:  # géoportail par défaut
        base_url = "https://data.geopf.fr/wfs/ows"

    # Construction de l’URI WFS
    uri = (
        f"wfs://pagingEnabled='true' restrictToRequestBBOX='1' "
        f"srsname='EPSG:2154' typename='{typename}' "
        f"url='{base_url}?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&bbox={bbox2154}' "
        "version='auto'"
    )

    # Chargement en mémoire
    vlayer = QgsVectorLayer(uri, nom, "WFS")
    if not vlayer.isValid():
        print(f" Impossible de charger {nom}")
        continue

    # Export en GeoJSON
    sortie = os.path.join(DOSSIER_SORTIE, f"{nom}.geojson")
    if os.path.exists(sortie):
        os.remove(sortie)

    try:
        processing.run("native:savefeatures", {"INPUT": vlayer, "OUTPUT": sortie})
        print(f" Export {nom} => {sortie}")
    except Exception as e:
        print(f" Erreur export {nom} : {e}")
        continue

    # Rechargement du fichier exporté
    lyr = QgsVectorLayer(sortie, nom, "ogr")
    if not lyr.isValid():
        print(f" Export OK mais lecture impossible pour {nom}")
        continue

    # Application du style
    qml_path = os.path.join(STYLE_DIR, qml)
    if os.path.exists(qml_path):
        lyr.loadNamedStyle(qml_path)
        lyr.triggerRepaint()
        print(f" Style appliqué : {qml_path}")
    else:
        print(f" Style manquant pour {nom}")

    # Ajout au projet QGIS
    proj.addMapLayer(lyr)

print("\n Extraction terminée => GeoJSON exportés et ajoutés au projet")
