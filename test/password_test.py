import requests
import json
from login_test import login

password_url = 'http://localhost:5000/change_password'
new_password_data = {
	'old_password': '123',
	'new_password': '1234'
}

old_password_data = {
	'old_password': '1234',
	'new_password': '123'	
}

def change_password(token, data):
	headers = {'token': token} 
	r = requests.post(password_url, headers=headers, data = data)
	return json.loads(r.content)
	assert json.loads(r.content)['status'] == 'success'

if __name__ == '__main__':
	login_result = login()
	token = login_result['token']

	result = change_password(token, new_password_data)
	assert result['status'] == 'success'

	result = change_password(token, new_password_data)
	assert result['status'] == 'error'

	result = change_password(token, old_password_data)
	assert result['status'] == 'success'
