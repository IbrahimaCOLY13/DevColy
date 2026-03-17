# Documentation des Fonctions Principales

## Gestion des couches

### charger_liste_couches()
```python
def charger_liste_couches(self):
    """
    Charge la liste des couches vectorielles du projet dans la liste déroulante.
    
    Utilisation:
        - Appelé au démarrage du plugin
        - Appelé lors du rafraîchissement de la liste des couches
    
    Retourne:
        None
    """
```

### charger_liste_couches_points()
```python
def charger_liste_couches_points(self):
    """
    Charge uniquement les couches de points dans la liste déroulante Couche_geocode_conso.
    
    Filtres:
        - Uniquement les couches vectorielles
        - Uniquement la géométrie de type point
    
    Retourne:
        None
    """
```

## Gestion des champs

### afficher_champs()
```python
def afficher_champs(self):
    """
    Affiche les champs de la couche sélectionnée.
    
    Colonnes affichées:
        - Nom du champ
        - Type de données
        - Longueur
        - Précision
    
    Retourne:
        None
    """
```

### convertir_champ()
```python
def convertir_champ(self, type_field, type_name, need_precision=False):
    """
    Convertit un ou plusieurs champs vers le type spécifié.
    
    Arguments:
        type_field (QVariant): Type de champ QVariant
        type_name (str): Nom du type de données
        need_precision (bool): Si True, utilise la précision spécifiée
    
    Processus:
        1. Vérifie la sélection
        2. Crée un champ temporaire
        3. Copie et convertit les données
        4. Supprime l'ancien champ
        5. Renomme le nouveau champ
    
    Retourne:
        None
    
    Lève:
        QgsException: Si la modification échoue
    """
```

## Gestion des consommations

### pre_trier_consommation()
```python
def pre_trier_consommation(self):
    """
    Ajoute les champs Conso_ret et type_conso et les remplit selon les critères.
    
    Critères de classification:
        - Faible: < 5
        - Domestique: 5-500
        - Entreprise: > 500
    
    Champs créés:
        - Conso_ret (Double): Valeur de consommation
        - type_conso (String): Classification
    
    Retourne:
        None
    """
```

### calculer_debits_BV()
```python
def calculer_debits_BV(self):
    """
    Calcule les débits pour chaque bassin versant.
    
    Formules:
        - Q_EU_DOM = (sum_dom / 365.0) * ratio
        - Q_EU_ENT = (sum_ent / 200.0) * ratio
        - Q_EU_SER = (sum_ser / 200.0) * ratio
    
    Champs créés:
        - Q_EU_DOM (Double)
        - Q_EU_ENT (Double)
        - Q_EU_SER (Double)
    
    Retourne:
        None
    """
```

## Statistiques et graphiques

### update_graphs()
```python
def update_graphs(self):
    """
    Met à jour les graphiques avec les options sélectionnées.
    
    Options:
        - Type de graphique (camembert/linéaire)
        - Affichage légende
        - Affichage valeurs
        - Affichage pourcentages
    
    Process:
        1. Réinitialise les graphiques
        2. Calcule les statistiques
        3. Crée les nouveaux graphiques
        4. Met à jour l'affichage
    
    Retourne:
        None
    """
```

### create_pie_chart()
```python
def create_pie_chart(self, data, title, show_legend=True, show_values=True, show_percentages=True):
    """
    Crée un graphique en camembert avec les options spécifiées.
    
    Arguments:
        data (dict): Données à représenter
        title (str): Titre du graphique
        show_legend (bool): Afficher la légende
        show_values (bool): Afficher les valeurs
        show_percentages (bool): Afficher les pourcentages
    
    Retourne:
        matplotlib.figure.Figure: Figure créée
    """
```

## Notes d'implémentation

### Gestion des erreurs
- Toutes les fonctions incluent une gestion des erreurs appropriée
- Les messages d'erreur sont affichés à l'utilisateur via QMessageBox
- Les opérations critiques sont effectuées dans des blocs try/except

### Performance
- Les opérations sur les couches sont optimisées pour les grands jeux de données
- Utilisation de QgsFeatureRequest pour filtrer les entités
- Mise en cache des résultats de calcul quand possible

### Interface utilisateur
- Les fonctions de mise à jour de l'interface sont non bloquantes
- Utilisation de signaux Qt pour la communication entre composants
- Validation des entrées utilisateur avant traitement 