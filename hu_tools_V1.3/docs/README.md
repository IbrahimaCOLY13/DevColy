# Documentation du Plugin HU_tools

## Table des matières

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Structure du projet](#structure)
4. [Documentation technique](#technique)
5. [Guide utilisateur](#utilisateur)

## Introduction <a name="introduction"></a>

HU_tools est un plugin QGIS développé pour faciliter la gestion et l'analyse des réseaux hydrauliques. Il offre des fonctionnalités avancées pour la manipulation des données, les calculs statistiques et la visualisation des résultats.

## Installation <a name="installation"></a>

### Prérequis
- QGIS 3.x
- Python 3.x
- PyQt5
- matplotlib

### Procédure d'installation
1. Télécharger le plugin
2. Extraire dans le dossier des plugins QGIS
3. Activer le plugin dans QGIS

## Structure du projet <a name="structure"></a>

```
hu_tools/
├── __init__.py
├── metadata.txt
├── HU_tools_dialog.py       # Interface principale
├── table/                   # Tables de correspondance
│   ├── MO.csv
│   └── Nom_couche_*.csv
└── docs/                    # Documentation
    ├── technique/
    └── utilisateur/
```

## Documentation technique <a name="technique"></a>

- [Classes et méthodes](technique/classes.md)
- [Fonctions principales](technique/fonctions.md)
- [Variables et constantes](technique/variables.md)
- [Gestion des données](technique/donnees.md)
- [Architecture](technique/architecture.md)

## Guide utilisateur <a name="utilisateur"></a>

- [Prise en main](utilisateur/demarrage.md)
- [Conversion des champs](utilisateur/conversion.md)
- [Gestion des consommations](utilisateur/consommations.md)
- [Statistiques et graphiques](utilisateur/statistiques.md)
- [Gestion des noms de couches](utilisateur/noms_couches.md) 