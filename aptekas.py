import sys
from pprint import pprint

from yandex_requests import *

# place = sys.argv[1]
place = 'Лицей 79, Набережные Челны'
earth_radius = 6371210
geocoder_params = {
    "geocode": place,
    "format": "json"}

toponym = GetGeoObjectsFromGeoCoderAPI(geocoder_params)["response"]["GeoObjectCollection"]["featureMember"][0][
    "GeoObject"]
toponym_coords = NormalizeCoords(toponym["Point"]["pos"])
search_params = {
    "text": "аптека",
    "lang": "ru_RU",
    "ll": toponym_coords,
    "type": "biz"
}

json_response = GetObjectsFromGeoSearchAPI(search_params)
objects = json_response['features']
obj_coords = []
for obj in objects[:10]:
    obj_coords.append([NormalizeCoords(obj["geometry"]["coordinates"])])
    if 'Hours' in obj['properties']['CompanyMetaData'].keys():
        if 'TwentyFourHours' in obj['properties']['CompanyMetaData']['Hours']['Availabilities'][0].keys():
            obj_coords[-1].append('pm2gnm')
        else:
            obj_coords[-1].append('pm2blm')
    else:
        obj_coords[-1].append('pm2grm')

obj_coords.append([toponym_coords, 'ya_ru'])
print(CreatePoints(obj_coords))
map_params = {
    "l": "sat",
    'pt': CreatePoints(obj_coords)
}


GetImageFromStaticAPI(map_params).show()
