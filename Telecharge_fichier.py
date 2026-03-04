

import os
import requests

# URL du PDF
url_pdf = "https://fichiers-publics.agriculture.gouv.fr/dgal/ListesOfficielles/lo_etbts_pisci.pdf"

# Dossier de destination
dossier_destination = r"Z:\sig\_Ibrahima_COLY"
# Nom du fichier
nom_fichier = "lo_etbts_pisci.pdf"

# Chemin complet du fichier
chemin_fichier = os.path.join(dossier_destination, nom_fichier)

try:
    # Vérifie si le dossier existe
    if not os.path.exists(dossier_destination):
        os.makedirs(dossier_destination)

    # Téléchargement du fichier
    reponse = requests.get(url_pdf, stream=True)
    reponse.raise_for_status()

    with open(chemin_fichier, "wb") as fichier:
        for bloc in reponse.iter_content(chunk_size=8192):
            fichier.write(bloc)

    print(f"Téléchargement terminé : {chemin_fichier}")

except Exception as erreur:
    print(f"Erreur lors du téléchargement : {erreur}")



