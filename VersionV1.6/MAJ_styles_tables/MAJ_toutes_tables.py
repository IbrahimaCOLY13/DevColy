def mettre_a_jour_toutes_les_tables(self):
    """
    Rafraîchit toutes les tables dans les différents onglets du plugin.
    """
    try:
        if hasattr(self, "refresh_all_lists"):
            self.refresh_all_lists()

        if hasattr(self, "charger_liste_couches_lignes"):
            self.charger_liste_couches_lignes()
        
        if hasattr(self, "charger_liste_couches"):
            self.charger_liste_couches()
        
        if hasattr(self, "charger_liste_couches_polygones"):
            self.charger_liste_couches_polygones()
        
        if hasattr(self, "charger_liste_couches_points"):
            self.charger_liste_couches_points()
            

        # ajouter ici autant de tables qu'on veut

    except Exception as e:
        raise Exception(f"Erreur mise à jour tables : {e}")
