import xml.etree.ElementTree as ET

def extract_qml_geometrie_type(qml_path):
    """
    Détecte précisément le type de géométrie (point, line, polygon)
    dans un fichier QML en lisant la structure XML.
    """
    try:
        tree = ET.parse(qml_path)
        root = tree.getroot()

        # Méthode 1 : recherche de la balise layerGeometryType
        geom_tag = root.find(".//layerGeometryType")
        if geom_tag is not None and geom_tag.text is not None:
            geom_value = geom_tag.text.strip().lower()
            mapping = {
                "0": "point",
                "1": "line",
                "2": "polygon",
            }
            return mapping.get(geom_value, None)

        # Méthode 2 : inspecter renderer-v2 @type (fiable pour QGIS)
        renderer = root.find(".//renderer-v2")
        if renderer is not None:
            r_type = renderer.get("type", "").lower()
            if "marker" in r_type:
                return "point"
            if "line" in r_type:
                return "line"
            if "fill" in r_type:
                return "polygon"

    except Exception as e:
        print("Erreur lors de la lecture XML :", e)

    return None


