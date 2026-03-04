
def trouver_element_par_nom(parent_item, name):
    """
    Retourne un enfant du parent portant le nom donné.
    Si non trouvé, retourne le parent lui-même.
    """
    for i in range(parent_item.rowCount()):
        child = parent_item.child(i)
        if child.text() == name:
            return child
    return parent_item
