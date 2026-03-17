import os
import math
import shutil
import requests
import csv

# Use http://localhost:7878 if you run a local instance.
#ADDOK_URL = 'https://wxs.ign.fr/essentiels/geoportail/geocodage/rest/0.1/search'
#ADDOK_URL = "https://api-adresse.data.gouv.fr/search/"
ADDOK_URL = "https://data.geopf.fr/geocodage/search"


print("Répertoire de travail actuel :", os.getcwd())

# pour géocoder un grand fichier CSV contenant plusieurs milliers d’adresses en une seule fois
def geocode(filepath_in, requests_options, filepath_out='geocoded.csv'):
    with open(filepath_in, 'rb') as f:
        filename, response = post_to_addok(filepath_in, f.read(), requests_options)
        write_response_to_disk(filepath_out, response)

# pour géocoder un grand fichier CSV contenant plusieurs milliers d’adresses par morceaux, pour éviter de saturer la mémoire ou le service.
def geocode_chunked(filepath_in, filename_pattern, chunk_by_approximate_lines, requests_options):
    b = os.path.getsize(filepath_in)
    output_files = []
    with open(filepath_in, 'r') as bigfile:
        row_count = sum(1 for row in bigfile)
    with open(filepath_in, 'r') as bigfile:
        headers = bigfile.readline()
        chunk_by = math.ceil(b / row_count * chunk_by_approximate_lines)
        current_lines = bigfile.readlines(chunk_by)
        i = 1
        # import ipdb;ipdb.set_trace()
        while current_lines:
            current_filename = filename_pattern.format(i)
            current_csv = ''.join([headers] + current_lines)
            # import ipdb;ipdb.set_trace()
            filename, response = post_to_addok(current_filename, current_csv, requests_options)
            write_response_to_disk(current_filename, response)
            current_lines = bigfile.readlines(chunk_by)
            i += 1
            output_files.append(current_filename)
    return output_files

# écrit cette réponse (fichier géocodé) sur le disque dur
def write_response_to_disk(filename, response, chunk_size=1024):
    with open(filename, 'wb') as fd:
        for chunk in response.iter_content(chunk_size=chunk_size):
            fd.write(chunk)

# envoie le fichier CSV à l’API IGN (méthode POST) et récupère la réponse.
def post_to_addok(filename, filelike_object, requests_options):
    #files = {'data': (filename, filelike_object)}
    #response = requests.post(ADDOK_URL, files=files, data=requests_options)
    response = requests.post(ADDOK_URL, files={'data': (filename, filelike_object)}, data=requests_options)

    # Vérifiez si la requête a réussi
    if response.status_code != 200:
        print(f"Erreur lors de l'appel à l'API : {response.status_code} - {response.text}")
        return None, None  # Retournez None si l'appel échoue

    # Vérifiez si l'en-tête 'content-disposition' est présent
    if 'content-disposition' not in response.headers:
        print("L'en-tête 'content-disposition' est manquant dans la réponse.")
        return None, response  # Retournez None si l'en-tête est manquant

    content_disposition = response.headers['content-disposition']
    filename = content_disposition[len('attachment; filename="'):-len('"')]
    return filename, response

# Fusionne tous les fichiers partiels géocodés en un seul grand CSV final. Supprime les doublons d’en-tête pour avoir un seul bloc de données cohérent.
def consolidate_multiple_csv(files, output_name):
    with open(output_name, 'wb') as outfile:
        for i, fname in enumerate(files):
            with open(fname, 'rb') as infile:
                if i != 0:
                    infile.readline()  # Throw away header on all but first file
                # Block copy rest of file from input to output without parsing
                shutil.copyfileobj(infile, outfile)

"""
# Geocode your file all at once if it is small.
geocode(
    'C:\\Users\\m.vincent\\Downloads\\32329a8557135f11cb5656e3bfd4d35c-9bd7883be31d2c9758d4393d72e9dc1ae4c5bed3 (1)\\32329a8557135f11cb5656e3bfd4d35c-9bd7883be31d2c9758d4393d72e9dc1ae4c5bed3\\annuaire-des-debits-de-tabac-2018-utf8.csv',
    {"columns": ['ADRESSE','CODE POSTAL','COMMUNE']},
    'annuaire-des-debits-de-tabac-2018-utf8.geocoded.csv'
)

# Alternatively, geocode it by chunks when it is big.
chunk_by = 1000  # approximative number of lines.
myfiles = geocode_chunked('./annuaire-des-debits-de-tabac-2018-utf8.csv', 'result-{}.csv', chunk_by, {"columns": ['ADRESSE','CODE POSTAL','COMMUNE']})
# Merge files
consolidate_multiple_csv(myfiles, 'myresult.csv')
# Clean files
[os.remove(f) for f in myfiles if os.path.isfile(f)]
"""