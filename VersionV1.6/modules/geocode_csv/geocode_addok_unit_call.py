import requests
ADDOK_URL = 'https://api-adresse.data.gouv.fr/search/'
params = {
    'q': '24 Rue des Diables Bleus 73000 Chambéry',
    'limit': 5
}
response = requests.get(ADDOK_URL, params=params)
j = response.json()
if len(j.get('features')) > 0:
    first_result = j.get('features')[0]
    lon, lat = first_result.get('geometry').get('coordinates')
    first_result_all_infos = { **first_result.get('properties'), **{"lon": lon, "lat": lat}}
    print(first_result_all_infos)
else:
    print('No result')
