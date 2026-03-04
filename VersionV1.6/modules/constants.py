from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsField

class Constants:
    # Seuils de consommation
    CONSUMPTION_THRESHOLDS = {
        'FAIBLE': {
            'min': 0,
            'max': 5,
            'label': 'Faible',
            'field_name': 'Q_EU_DOM'
        },
        'DOMESTIQUE': {
            'min': 5,
            'max': 500,
            'label': 'Domestique',
            'field_name': 'Q_EU_DOM'
        },
        'ENTREPRISE': {
            'min': 500,
            'max': float('inf'),
            'label': 'Entreprise',
            'field_name': 'Q_EU_ENT'
        }
    }

    # Ratios de calcul
    CALCULATION_RATIOS = {
        'RATIO_CONSO_DEFAULT': 0.8,
        'RATIO_HAB_DEFAULT': 2.5,
        'RATIO_JOUR_DOM': 365.0,
        'RATIO_JOUR_PRO': 200.0
    }

    # Champs de débit BV
    BV_FIELDS = {
        'Q_EU_DOM': QgsField('Q_EU_DOM', QVariant.Double, 'double', 10, 3),
        'Q_EU_ENT': QgsField('Q_EU_ENT', QVariant.Double, 'double', 10, 3),
        'Q_EU_SER': QgsField('Q_EU_SER', QVariant.Double, 'double', 10, 3)
    }

    # Formats d'export
    EXPORT_FORMATS = {
        'SHP': {
            'extension': '.shp',
            'driver': 'ESRI Shapefile',
            'encoding': 'UTF-8'
        },
        'GPKG': {
            'extension': '.gpkg',
            'driver': 'GPKG',
            'encoding': 'UTF-8'
        },
        'GEOJSON': {
            'extension': '.geojson',
            'driver': 'GeoJSON',
            'encoding': 'UTF-8'
        }
    }

    # Indicateurs statistiques
    STATS_INDICATORS = {
        'TOTAL_ENTITIES': 'Nombre total d\'entités',
        'TOTAL_CONSUMPTION': 'Consommation totale (m³)',
        'DOM_COUNT': 'Nombre d\'abonnés domestiques',
        'DOM_CONSUMPTION': 'Consommation domestique (m³)',
        'CONSUMPTION_PER_SUB': 'Consommation par abonné (m³)',
        'CONSUMPTION_PER_HAB': 'Consommation par habitant (l/j/hab)',
        'NONDOM_COUNT': 'Nombre d\'abonnés non domestiques',
        'NONDOM_CONSUMPTION': 'Consommation non domestique (m³)',
        'AVG_NONDOM_CONSUMPTION': 'Consommation moyenne non domestique (m³)'
    }

    # Chemins et fichiers
    PATHS = {
        'TABLE_DIR': 'table',
        'MO_FILE': 'MO.csv',
        'COUCHE_PREFIX': 'Nom_couche_'
    }

    # Messages d'erreur
    ERROR_MESSAGES = {
        'LAYER_NOT_FOUND': "La couche sélectionnée n'existe pas",
        'FIELD_NOT_FOUND': "Le champ spécifié n'existe pas",
        'INVALID_VALUE': "Valeur invalide",
        'CONVERSION_ERROR': "Erreur lors de la conversion",
        'NO_SELECTION': "Aucune entité sélectionnée"
    }
