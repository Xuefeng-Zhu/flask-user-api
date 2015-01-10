from flask import Flask, request, abort
from flask.ext.restful import Resource, Api
from flask_mail import Mail
from model import db, bcrypt, redis_store
from api.userAPI import UserAPI, LoginAPI, FBUserAPI, FBLoginAPI, ActivateAPI
from api.profileAPI import ProfileAPI, ProfileIconAPI, SearchProfileAPI
from api.friendsAPI import FriendsListAPI, FriendsRequestAPI
from api.passwordAPI import ChangePasswordAPI, ForgetPasswordAPI

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)
bcrypt.init_app(app)
redis_store.init_app(app)
mail = Mail(app)

api = Api(app)

api.add_resource(UserAPI, '/create_user')
api.add_resource(LoginAPI, '/login')
api.add_resource(FBUserAPI, '/fb_create_user')
api.add_resource(FBLoginAPI, '/fb_login')
api.add_resource(ActivateAPI, '/activate_account')


api.add_resource(ChangePasswordAPI, '/change_password')
api.add_resource(ForgetPasswordAPI, '/forget_password')

api.add_resource(ProfileAPI, '/profile')
api.add_resource(ProfileIconAPI, '/upload_profile_icon')
api.add_resource(SearchProfileAPI, '/search_profile')

api.add_resource(FriendsListAPI, '/friends_list')
api.add_resource(FriendsRequestAPI, '/friends_request')

if __name__ == '__main__':
    app.run(debug=True)



