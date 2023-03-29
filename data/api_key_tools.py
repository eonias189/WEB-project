import json
import secrets

SYMBOLS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '_', '-', '+', '=',
           '!', '@', '$', '%', '^', '*', '(', ')', '[', ']', '{', '}', '"', '№', ';', ':', '?', '/']
METHODS = ['GET', 'POST', 'DELETE', 'PUT', 'LOGIN']
URL = 'api_key.json'


def generate_key(n=15):
    return ''.join([secrets.choice(SYMBOLS) for _ in range(n)])


def get_keys(method=None, from_data=False):
    full_url = URL if from_data else 'data/' + URL
    with open(full_url, 'r') as f:
        data = json.load(f)
    if method is not None and method in METHODS:
        return data[method]
    return data


def create_key(method, from_data=False):
    data = get_keys(method=None, from_data=from_data)
    key = generate_key()
    data[method] += [key]
    full_url = URL if from_data else 'data/' + URL
    with open(full_url, 'w') as f:
        json.dump(data, f, indent=2)
    return key


def check_key(method, key, from_data=False):
    full_url = URL if from_data else 'data/' + URL
    data = get_keys(method=None, from_data=from_data)
    if key in data[method]:
        data[method].remove(key)
        with open(full_url, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    return False


if __name__ == '__main__':
    print(get_keys(from_data=True))
