# Documentation des Variables et Constantes

## Variables globales

### Interface utilisateur
```python
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'HU_tools_dialog_base.ui'))
```
- **Description** : Charge le fichier UI Qt Designer
- **Utilisation** : Définition de l'interface graphique
- **Type** : tuple(type, None)

## Constantes de configuration

### Seuils de consommation
```python
# Seuils pour la classification des consommations
SEUIL_FAIBLE = 5        # m³
SEUIL_DOMESTIQUE = 500  # m³
```
- Utilisés dans la fonction `pre_trier_consommation()`
- Définissent les limites des catégories de consommation

### Ratios de calcul
```python
# Ratios pour le calcul des débits
RATIO_JOUR_DOM = 365.0  # jours (consommation domestique)
RATIO_JOUR_PRO = 200.0  # jours (consommation professionnelle)
```
- Utilisés dans la fonction `calculer_debits_BV()`
- Facteurs de conversion pour les débits

## Variables d'instance (HU_projectDialog)

### Modèles de données
```python
self.conso_model: QStandardItemModel
self.champs_model: QStandardItemModel
self.proxy_model: QSortFilterProxyModel
```
- Gèrent l'affichage et le tri des données dans les tableaux

### Gestionnaires
```python
self.stats_manager: StatsManager
self.graph_manager: GraphManager
```
- Instances des classes de gestion des statistiques et graphiques

### État des graphiques
```python
self.current_graph: int
self.graphs: list
```
- Suivent l'état actuel des graphiques affichés

## Variables d'instance (GraphManager)

### Éléments matplotlib
```python
self.figure: Figure
self.canvas: FigureCanvas
```
- Gèrent l'affichage des graphiques

## Types de données

### Types de champs
```python
FIELD_TYPES = {
    'String': QVariant.String,
    'Integer': QVariant.Int,
    'Double': QVariant.Double
}
```
- Types de données disponibles pour la conversion des champs

### Types de consommation
```python
CONSO_TYPES = {
    'Faible': {'min': 0, 'max': 5},
    'Domestique': {'min': 5, 'max': 500},
    'Entreprise': {'min': 500, 'max': float('inf')}
}
```
- Définitions des catégories de consommation

## Chemins de fichiers

### Tables de correspondance
```python
# Chemins relatifs des fichiers de données
TABLE_DIR = 'table'
MO_FILE = 'MO.csv'
COUCHE_PREFIX = 'Nom_couche_'
```
- Utilisés pour la gestion des noms de couches

## Notes sur la gestion des variables

### Portée des variables
- Les variables globales sont minimisées
- Préférence pour les variables d'instance
- Utilisation de getters/setters pour l'accès aux données

### Conventions de nommage
- Variables en snake_case
- Constantes en MAJUSCULES
- Classes en PascalCase

### Gestion de la mémoire
- Nettoyage des références cycliques
- Libération des ressources matplotlib
- Optimisation des structures de données 