from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsField,
    QgsCategorizedSymbolRenderer,
    QgsGraduatedSymbolRenderer,
    QgsSingleSymbolRenderer
)
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QMessageBox

def ajout_couleurs_rgb(iface):
    """Exporte la couleur de la symbologie dans un champ 'color_rgb'."""

    layer = iface.activeLayer()

    if not layer:
        QMessageBox.critical(None, "Erreur", "Aucune couche active sélectionnée !")
        return

    field_name = "color_rgb"
    provider = layer.dataProvider()

    # Ajout du champ s’il n’existe pas
    if field_name not in [f.name() for f in layer.fields()]:
        layer.startEditing()
        provider.addAttributes([QgsField(field_name, QVariant.String)])
        layer.updateFields()
        layer.commitChanges()

    renderer = layer.renderer()
    layer.startEditing()
    idx = layer.fields().indexFromName(field_name)

    try:
        if isinstance(renderer, QgsSingleSymbolRenderer):
            color = renderer.symbol().color()
            rgb_value = f"{color.red()},{color.green()},{color.blue()}"
            count = 0
            for feature in layer.getFeatures():
                layer.changeAttributeValue(feature.id(), idx, rgb_value)
                count += 1
            QMessageBox.information(None, "Succès", f"Rendu simple : couleur '{rgb_value}' appliquée à {count} entités.")

        elif isinstance(renderer, QgsCategorizedSymbolRenderer):
            value_to_color = {cat.value(): cat.symbol().color() for cat in renderer.categories()}
            field_used = renderer.classAttribute()
            if not field_used:
                QMessageBox.critical(None, "Erreur", "Impossible de déterminer le champ de symbologie.")
                layer.rollBack()
                return
            updates = []
            for feature in layer.getFeatures():
                value = feature[field_used]
                color = value_to_color.get(value)
                if color:
                    rgb_value = f"{color.red()},{color.green()},{color.blue()}"
                    updates.append((feature.id(), rgb_value))
            if updates:
                for fid, rgb in updates:
                    layer.changeAttributeValue(fid, idx, rgb)
                QMessageBox.information(None, "Succès", f"Rendu catégorisé : couleurs exportées pour {len(updates)} entités.")
            else:
                QMessageBox.warning(None, "Info", "Aucune couleur n’a été appliquée. Vérifiez vos catégories.")

        elif isinstance(renderer, QgsGraduatedSymbolRenderer):
            value_to_color = {r.label(): r.symbol().color() for r in renderer.ranges()}
            field_used = renderer.classAttribute()
            if not field_used:
                QMessageBox.critical(None, "Erreur", "Impossible de déterminer le champ de symbologie.")
                layer.rollBack()
                return
            updates = []
            for feature in layer.getFeatures():
                value = feature[field_used]
                color = value_to_color.get(value)
                if color:
                    rgb_value = f"{color.red()},{color.green()},{color.blue()}"
                    updates.append((feature.id(), rgb_value))
            if updates:
                for fid, rgb in updates:
                    layer.changeAttributeValue(fid, idx, rgb)
                QMessageBox.information(None, "Succès", f"Rendu gradué : couleurs exportées pour {len(updates)} entités.")
            else:
                QMessageBox.warning(None, "Info", "Aucune couleur n’a été appliquée. Vérifiez vos classes graduées.")

        else:
            QMessageBox.warning(None, "Info", f"Type de symbologie '{type(renderer).__name__}' non géré automatiquement. Utilisez un rendu simple, catégorisé ou gradué.")
            layer.rollBack()
            return

        layer.commitChanges()

    except Exception as e:
        layer.rollBack()
        QMessageBox.critical(None, "Erreur", f"Échec lors de l'exécution : {str(e)}")
