import requests
import json
from login_test import login

if __name__ == '__main__':
	login = login()
	token = login['token']
	print token
