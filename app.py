from flask import Flask, request, abort
from flask.ext.restful import Resource, Api
from model import db, bcrypt, redis_store
from userAPI import UserAPI, LoginAPI, FBUserAPI, FBLoginAPI
from profileAPI import ProfileAPI, ProfileIconAPI, SearchProfileAPI

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'flask-test',
    'host': 'ds027741.mongolab.com',
    'port': 27741,
    'username': 'flask-admin',
    'password': '123123'
}

app.config['REDIS_URL'] = "redis://:123123@pub-redis-17784.us-east-1-2.1.ec2.garantiadata.com:17784/0"
app.config['SECRET_KEY'] = 'flask is cool' 

db.init_app(app)
bcrypt.init_app(app)
redis_store.init_app(app)

api = Api(app)

api.add_resource(UserAPI, '/create_user')
api.add_resource(LoginAPI, '/login')
api.add_resource(FBUserAPI, '/fb_create_user')
api.add_resource(FBLoginAPI, '/fb_login')

api.add_resource(ProfileAPI, '/profile')
api.add_resource(ProfileIconAPI, '/upload_profile_icon')
api.add_resource(SearchProfileAPI, '/search_profile')

if __name__ == '__main__':
    app.run(debug=True)



