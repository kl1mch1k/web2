import sys
from math import sin, cos, acos, radians
from yandex_requests import *

place = sys.argv[1]
earth_radius = 6371210
geocoder_params = {
    "geocode": place,
    "format": "json"}

toponym = GetGeoObjectsFromGeoCoderAPI(geocoder_params)["response"]["GeoObjectCollection"]["featureMember"][0][
    "GeoObject"]
toponym_coords = NormalizeCoords(toponym["Point"]["pos"])
toponym_longitude, toponym_latitude = [radians(float(i)) for i in toponym_coords.split(",")]
search_params = {
    "text": "аптека",
    "lang": "ru_RU",
    "ll": toponym_coords,
    "type": "biz"
}

json_response = GetObjectsFromGeoSearchAPI(search_params)
obj = json_response['features'][0]
obj_props = obj['properties']
obj_coords = NormalizeCoords(obj["geometry"]["coordinates"])
obj_longitude, obj_latitude = [radians(float(i)) for i in obj_coords.split(',')]
map_params = {
    "l": "sat",
    'pt': CreatePoints(((toponym_coords, 'ya_ru'), (obj_coords, 'pm2al')))
}
dist = acos(sin(obj_latitude) * sin(toponym_latitude) + cos(obj_latitude) * cos(toponym_latitude) * cos(
    obj_longitude - toponym_longitude)) * earth_radius
print(f'Название: {obj_props["name"]}', f'Адрес: {obj_props["description"]}',
      f'Время работы: {obj_props["CompanyMetaData"]["Hours"]["text"]}',
      f'Расстояние от заданной точки: {round(dist, 1)} м', sep='\n')
GetImageFromStaticAPI(map_params).show()
