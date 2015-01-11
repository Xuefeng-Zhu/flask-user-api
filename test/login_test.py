import requests
import json

login_url = 'http://localhost:5000/login'
user_data = {'email': 'xzhu15@illinois.edu', 'password': '123'}

def login():
	r = requests.post(login_url, data=user_data)
	return json.loads(r.content)

if __name__ == '__main__':
	result = login()
	print result['token']