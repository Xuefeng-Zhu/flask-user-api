import requests
import json
from login_test import login
from profile_test import search_profile

friends_url = 'http://localhost:5000/friends_list'


def get_friends_list(token):
    headers = {'token': token}
    r = requests.get(friends_url, headers=headers)
    return json.loads(r.content)


def add_friends_list(token, profile_id):
    headers = {'token': token}
    data = {'profile_id': profile_id}
    r = requests.post(friends_url, headers=headers, data=data)
    assert json.loads(r.content)['status'] == 'success'


def delete_friends_list(token, profile_id):
    headers = {'token': token}
    data = {'profile_id': profile_id}
    r = requests.delete(friends_url, headers=headers, data=data)
    assert json.loads(r.content)['status'] == 'success'

if __name__ == '__main__':
    login = login()
    token = login['token']

    result = search_profile(token)
    profile_id = result[0]['profile_id']

    add_friends_list(token, profile_id)
    prev = get_friends_list(token)

    delete_friends_list(token, profile_id)
    curr = get_friends_list(token)

    assert len(prev) == len(curr) + 1
