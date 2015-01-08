from flask import Flask, request, abort
from flask.ext.restful import Resource, Api
from model import db, bcrypt, redis_store
from userAPI import UserAPI, LoginAPI, FBUserAPI, FBLoginAPI
from profileAPI import ProfileAPI, ProfileIconAPI, SearchProfileAPI
from FriendsAPI import FriendsListAPI
from PasswordAPI import ChangePasswordAPI

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)
bcrypt.init_app(app)
redis_store.init_app(app)

api = Api(app)

api.add_resource(UserAPI, '/create_user')
api.add_resource(LoginAPI, '/login')
api.add_resource(FBUserAPI, '/fb_create_user')
api.add_resource(FBLoginAPI, '/fb_login')

api.add_resource(ChangePasswordAPI, '/change_password')

api.add_resource(ProfileAPI, '/profile')
api.add_resource(ProfileIconAPI, '/upload_profile_icon')
api.add_resource(SearchProfileAPI, '/search_profile')

api.add_resource(FriendsListAPI, '/friends_list')

if __name__ == '__main__':
    app.run(debug=True)



