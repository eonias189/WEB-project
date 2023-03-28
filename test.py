from pprint import pprint
from data.api_key_tools import create_key, get_keys
import requests

url = 'http://127.0.0.1:5000/api/users/5'
json = {'id': 6, 'login': 'eonias6', 'hashed_password': 'qwerty', 'score': 0}
params = {'key': create_key('DELETE')}
pprint(requests.delete(url, params=params, json=json).json())
