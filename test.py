from pprint import pprint
import requests

url = 'http://127.0.0.1:5000/api/question'
params = {'key': "ER*los]NtTW:G14SH@"}
response = requests.get(url, params=params).json()
varinats, content, encoding, country = response['variants'], response['content'], response['encoding'], response[
    'country']
content = bytes(content, encoding)
with open('static/img/image.png', 'wb') as f:
    f.write(content)
print(varinats)
print(country)
