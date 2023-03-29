import requests
import os
import math
import pygame
from io import BytesIO
from PIL import Image

API_KEY_GEOCODER = "40d1649f-0493-4b70-98ba-98533de7710b"


def get_coords(toponym_name, api_key):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": api_key,
        "geocode": toponym_name,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        return False
    json_resp = response.json()
    toponym = json_resp['response']["GeoObjectCollection"][
        "featureMember"]
    if len(toponym) == 0:
        return False
    toponym = toponym[0]["GeoObject"]
    ll = ','.join(toponym["Point"]["pos"].split())
    envelope = toponym['boundedBy']['Envelope']
    l, d = envelope['lowerCorner'].split(' ')
    r, u = envelope['upperCorner'].split(' ')
    geo = [float(i) for i in [r, l, u, d]] + [tuple([float(i) for i in ll.split(',')])]
    return (ll, geo)


def get_spn(geo):
    r, l, u, d, ll = geo
    dx = abs(r - l) / 4
    dy = abs(u - d) / 4
    return f'{dx},{dy}'


def get_dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    sy = abs(y2 - y1) * 111
    l_x = 111 * math.cos(math.radians(abs(y1 + y1) / 2))
    sx = l_x * abs(x2 - x1)
    return math.sqrt(sx ** 2 + sy ** 2)


def get_image(coords, type='map', point=None, spn=None):
    if not spn:
        ll, geo = coords
    else:
        ll = coords
    if not spn:
        spn = get_spn(geo)
    map_params = {
        "ll": ll,
        "spn": spn,
        "l": type}
    if point:
        map_params['pt'] = f'{point},comma'
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    if not response:
        return 'Ошибка получения изображения'
    return response.content


if __name__ == '__main__':
    coords = get_coords('Ы', API_KEY_GEOCODER)
    im = get_image(coords, type='sat,skl', point=coords[0])
    with open('static/img/image.png', 'wb') as f:
        f.write(im)
