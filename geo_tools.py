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


if __name__ == '__main__':
    print(get_coords('Бразилия', API_KEY_GEOCODER))
