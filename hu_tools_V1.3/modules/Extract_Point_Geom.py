
from qgis.core import QgsGeometry, QgsPointXY, QgsWkbTypes
def extraire_dernier_point_geom(geom):
    """
    Retourne le dernier point d'une géométrie LineString ou MultiLineString.
    Gère aussi les géométries vides ou invalides.
    """
    if geom is None or geom.isEmpty():
        return None

    if geom.type() != QgsWkbTypes.LineGeometry:
        return None

    wkb_type = geom.wkbType()

    # Cas LINESTRING simple
    if QgsWkbTypes.isSingleType(wkb_type):
        pts = geom.asPolyline()
        if pts:
            return pts[-1]

    # Cas MULTILINESTRING
    elif QgsWkbTypes.isMultiType(wkb_type):
        lines = geom.asMultiPolyline()
        if lines:
            last_line = lines[-1]
            if last_line:
                return last_line[-1]

    return None
