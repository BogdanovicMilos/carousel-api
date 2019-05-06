import requests
import json

BASE_URL = 'http://127.0.0.1:8000/'
ENDPOINT = 'api/users/'


def user_list(id=None):
    data = json.dumps({})
    if id is not None:
        data = json.dumps({'id': id})
    r = requests.get(BASE_URL + ENDPOINT, data=data)
    print(r.status_code)
    status_code = r.status_code
    if status_code != 200:
        print('Not good')
    data = r.json()
    return data


print(user_list())


def user_create():
    new_data = {
        'email': 'testuser6@company.com',
        'display_name': 'TestUser6',
        'image': ''
    }
    r = requests.post(BASE_URL + ENDPOINT, data=json.dumps(new_data))
    print(r.headers)
    print(r.status_code)
    if r.status_code == requests.codes.ok:
        return r.json()
    return r.text


# print(user_create())


def user_update():
    new_data = {
        'id': 5,
        'email': 'testuser999@company.com',
    }
    r = requests.put(BASE_URL + ENDPOINT, data=json.dumps(new_data))
    # print(r.headers)
    print(r.status_code)
    if r.status_code == requests.codes.ok:
        return r.json()
    return r.text


# print(user_update())


def user_delete():
    new_data = {
        'id': 5,
    }
    r = requests.delete(BASE_URL + ENDPOINT, data=json.dumps(new_data))
    # print(r.headers)
    print(r.status_code)
    if r.status_code == requests.codes.ok:
        return r.json()
    return r.text


# print(user_delete())
