from pprint import pprint
from data.api_key_tools import create_key, get_keys
import requests

url = 'http://127.0.0.1:5000/api/login'
json = {'login': 'eonias', 'password': 'qwerty'}
params = {'key': create_key('LOGIN')}
pprint(requests.get(url, params=params, json=json).json())
