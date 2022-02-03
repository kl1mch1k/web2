from yandex_requests import *
import sys

place = ''.join(sys.argv[1:])

geocoder_params = {
    "geocode": place,
    "format": "json"}

toponym = GetGeoObjectsFromGeoCoderAPI(geocoder_params)["response"]["GeoObjectCollection"]["featureMember"][0][
    "GeoObject"]
toponym_coords = NormalizeCoords(toponym["Point"]["pos"])

geocoder_params = {
    "geocode": NormalizeCoords(toponym_coords),
    "format": "json",
    "kind": "district"}
try:
    district = GetGeoObjectsFromGeoCoderAPI(geocoder_params)["response"]["GeoObjectCollection"]["featureMember"][0][
        "GeoObject"]['metaDataProperty']['GeocoderMetaData']['text']
except IndexError:
    print('Данных о районе нет.')
    exit(0)
print(district)
