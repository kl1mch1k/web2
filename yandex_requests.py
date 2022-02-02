import requests


def GetObjectsFromGeoSearchAPI(params):
    params: dict
    params['apikey'] = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
    response = requests.get("https://search-maps.yandex.ru/v1/", params=params)
    check_request(response)
    return response.json()


def find_toponym_size(toponym):
    bounding_rect = [list(map(float, i.split())) for i in toponym['boundedBy']['Envelope'].values()]
    return str(bounding_rect[1][0] - bounding_rect[0][0]), str(bounding_rect[1][1] - bounding_rect[0][1])


def GetImageFromStaticAPI(params):
    params: dict
    import requests
    from PIL import Image
    from io import BytesIO
    response = requests.get("http://static-maps.yandex.ru/1.x/", params=params)
    check_request(response)
    return Image.open(BytesIO(response.content))


def GetGeoObjectsFromGeoCoderAPI(params):
    params: dict
    params['apikey'] = '40d1649f-0493-4b70-98ba-98533de7710b'
    response = requests.get("http://geocode-maps.yandex.ru/1.x/", params=params)

    check_request(response)

    return response.json()


def NormalizeCoords(coords: str) -> str:
    if isinstance(coords, tuple) or isinstance(coords, list):
        coords = [str(coord) for coord in coords]
        return ','.join(coords)
    elif isinstance(coords, str):
        return coords.replace(' ', ',')


def CreatePoints(points):
    return '~'.join([','.join(i) for i in points])


def check_request(request):
    if not request:
        raise ConnectionError
