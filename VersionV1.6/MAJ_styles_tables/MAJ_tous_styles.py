from qgis.core import QgsProject
def mettre_a_jour_styles(self):
    """
    Met à jour tous les styles des couches du plugin.
    """
    try:
        layers = QgsProject.instance().mapLayers().values()

        # D'abord rafraîchir les styles en mémoire
        for layer in layers:
            if hasattr(layer, "styleManager"):
                layer.triggerRepaint()

        # sauvegarder les styles (1 seule fois !)
        #self.exporter_styles_couches()

    except Exception as e:
        raise Exception(f"Erreur mise à jour styles : {e}")

