from pprint import pprint
from data.api_key_tools import create_key, get_keys
import requests

url = 'http://127.0.0.1:5000/api/users'
json = {'login': 'eonias6', 'hashed_password': 'qwerty'}
params = {'key': create_key('POST')}
pprint(requests.post(url, params=params, json=json).json())
