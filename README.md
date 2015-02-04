flask-user-api
==============
Flask User API is built on Flask-restful to provide simple user management functionality. 

Such as
+ User creation 
+ User Login
+ Facebook Login
+ Password management 
+ Profile management
+ Friend List management 
+ Simple Post

## Demo 
The API is currently deployed on Heroku

[Demo](http://floating-retreat-4846.herokuapp.com/login)

## Usage

#### Install dependency 
	pip install -r requirements.txt

#### Config
	change the arguments in config.py	
	
#### Run 
	python app.py
	
#### Manual
```
Create User 
curl localhost:5000/create_user -X POST -d "email=123@gmail.com" -d "password=123"

Login 
curl localhost:5000/login -X POST -d "email=123@gmail.com" -d "password=123"

FB Login 
curl localhost:5000/fb_login -X POST -d "fbtoken=" -d "fbid="

Renew Token 
curl localhost:5000/login -X GET --header "token: from login api"

Change Password 
curl localhost:5000/change_password -X POST --header "token: from login api" -d "old_password=123" -d "new_password=1234"

Forget Password
curl localhost:5000/forget_password -X POST -d "email=123@gmail.com" -d "username=test" -d "school=UIUC"

Load Profile 
curl localhost:5000/profile -X GET --header "token: from login api"  

Edit Profile 
curl localhost:5000/profile -X POST --header "token: from login api" -d "username=test" -d "school=UIUC" -d "intro=I am Frank"

Upload Profile Icon 
curl --form upload=@icon.png --form press=OK localhost:5000/upload_profile_icon -X POST --header "token: from login api"

Search Profile
curl localhost:5000/search_profile -X GET --header "token: from login api" -d "school=UIUC"

Get Friends List 
curl localhost:5000/friends_list -X GET --header "token: from login api"

Add to Friends List 
curl localhost:5000/friends_list -X POST --header "token: from login api" -d "profile_id= "

Delete from Friends List 
curl localhost:5000/friends_list -X DELETE --header "token: from login api" -d "profile_id= "

Get Friends Request List 
curl localhost:5000/friends_request -X GET --header "token: from login api"

Post a Friend Post
curl localhost:5000/post -X POST --header "token: from login api" -d "content=I want to find someone to talk"

Get posts
curl localhost:5000/post -X GET --header "token: from login api" 
```		
	
#### Deployment on Heroku
Just create a new heroku application, and push the code to heroku

## Acknowledgements
This project is built on following libraries
+ [boto](https://github.com/boto/boto)
+ [Flask](https://github.com/mitsuhiko/flask)
+ [flask-bcrypt](https://github.com/maxcountryman/flask-bcrypt)
+ [Flask-Mail](https://github.com/mattupstate/flask-mail)
+ [flask-mongoengine](https://github.com/MongoEngine/flask-mongoengine)
+ [flask-redis](https://github.com/rhyselsmore/flask-redis)
+ [Flask-RESTful](https://github.com/flask-restful/flask-restful)
+ [gunicorn](https://github.com/benoitc/gunicorn)
+ [itsdangerous](https://github.com/mitsuhiko/itsdangerous)
+ [requests](https://github.com/kennethreitz/requests)