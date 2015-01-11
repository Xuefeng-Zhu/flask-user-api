import requests
import json

login_url = 'http://localhost:5000/login'
user_data = {'email': 'xzhu15@illinois.edu', 'password': '123'}

def login():
	r = requests.post(login_url, data=user_data)
	return json.loads(r.content)

def renew_token(token):
	headers = {'token': token}
	r = requests.get(login_url, headers=headers)
	return json.loads(r.content)

if __name__ == '__main__':
	result = login()
	token = result['token']
	print 'old token:', token

	result = renew_token(token)
	token = result['token']
	print 'new token:', token
	