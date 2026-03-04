# Guide de démarrage - HU_tools

## Installation

1. Ouvrir QGIS
2. Menu Extensions > Installer/Gérer les extensions
3. Rechercher "HU_tools"
4. Cliquer sur "Installer"

## Interface principale

### Onglets disponibles

1. **Conversion des champs**
   - Modification des types de données
   - Gestion des longueurs et précisions

2. **Consommations AEP**
   - Analyse des consommations
   - Calcul des débits par bassin versant

3. **Statistiques réseau**
   - Analyses statistiques
   - Visualisation graphique

### Barre d'outils

- ![refresh](../images/refresh.png) Actualiser les listes
- ![export](../images/export.png) Exporter les résultats
- ![help](../images/help.png) Aide

## Premiers pas

### 1. Préparation des données

1. Charger vos couches dans QGIS
2. Vérifier que les couches sont bien visibles
3. Cliquer sur "Actualiser les listes"

### 2. Conversion des champs

1. Sélectionner la couche à modifier
2. Choisir le(s) champ(s) à convertir
3. Définir les paramètres (longueur, précision)
4. Cliquer sur le type de conversion souhaité

### 3. Analyse des consommations

1. Sélectionner la couche de points
2. Choisir les champs de consommation
3. Lancer le pré-tri
4. Visualiser les résultats

### 4. Statistiques et graphiques

1. Sélectionner les couches à analyser
2. Choisir les champs d'analyse
3. Configurer l'affichage des graphiques
4. Naviguer entre les résultats

## Astuces

### Performance
- Indexer les champs fréquemment utilisés
- Filtrer les données avant analyse
- Utiliser les options de mise en cache

### Interface
- Double-clic pour éditer les valeurs
- Ctrl+clic pour sélection multiple
- Drag & drop pour réorganiser les colonnes

### Graphiques
- Clic droit pour options d'export
- Molette pour zoom
- Ctrl+molette pour rotation

## Dépannage

### Problèmes courants

1. **Les listes sont vides**
   - Vérifier que des couches sont chargées
   - Actualiser les listes
   - Vérifier les types de géométrie

2. **Erreurs de conversion**
   - Vérifier la compatibilité des données
   - Ajuster la longueur/précision
   - Vérifier les valeurs nulles

3. **Graphiques non affichés**
   - Vérifier la sélection des champs
   - Rafraîchir l'affichage
   - Vérifier la mémoire disponible

### Support

Pour toute assistance :
- Documentation : [lien]
- Support technique : m.vincent@nca.fr
- Forum QGIS : [lien]

## Bonnes pratiques

### Organisation des données
- Nommer clairement les couches
- Structurer les champs de manière cohérente
- Sauvegarder régulièrement

### Analyse
- Vérifier les données source
- Valider les résultats intermédiaires
- Documenter les paramètres utilisés

### Export
- Choisir des formats adaptés
- Inclure les métadonnées
- Vérifier les fichiers exportés 