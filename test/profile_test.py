import requests
import json
from login_test import login

profile_url = 'http://localhost:5000/profile'
search_profile_url = 'http://localhost:5000/search_profile'
profile_data = {
	'username': 'test',
	'school': 'UIUC',
	'intro': 'test intro',
	'profile_icon': None
}
search_data = {
	'school': 'UIUC'
}

def edit_profile(token):
	headers = {'token': token} 
	r = requests.post(profile_url, headers=headers, data = profile_data)
	result = json.loads(r.content)
	assert result == profile_data

def load_profile(token):
	headers = {'token': token} 
	r = requests.get(profile_url, headers=headers)
	result = json.loads(r.content)
	assert result == profile_data

def search_profile(token):
	headers = {'token': token} 
	r = requests.get(search_profile_url, headers=headers, data = search_data)
	result = json.loads(r.content)
	assert result[0]['school'] == search_data['school']

if __name__ == '__main__':
	login = login()
	token = login['token']

	edit_profile(token)
	load_profile(token)
	search_profile(token)

