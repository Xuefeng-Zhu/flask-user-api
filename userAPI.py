from flask import abort
from flask.ext.restful import Resource, reqparse
from mongoengine.errors import NotUniqueError, ValidationError
from model.user import User
from model import redis_store
from userAuth import auth_required, load_token
from emails import send_activate_account_email
import requests 


userParser = reqparse.RequestParser()
userParser.add_argument('email', type=str)
userParser.add_argument('password', type=str)

class UserAPI(Resource):
    def post(self):
        args = userParser.parse_args()
        email = args['email']
        password = args['password']
        if email is None or password is None:
            abort(400)    

        user = User(email=email)
        user.hash_password(password)
        try:
            user.save()
        except ValidationError, e:
            return {'status': 'error', 'message': e.message}  
        except NotUniqueError, e:
            return {'status': 'error', 'message': e.message}

        token = user.generate_auth_token(expiration=360000)
        send_activate_account_email(email, token)

        return ({'status': 'success', 'message': 'Please check your email to activate your account.'}, 201)


class LoginAPI(Resource):
    # renew token by using old valid token 
    @auth_required
    def get(self, user_id):
        user = User.objects(id=user_id).first()
        token = user.generate_auth_token(expiration=360000)
        redis_store.set(user_id, token)
        return {'token': token}

    def post(self):
        args = userParser.parse_args()
        email = args['email']
        password = args['password']
        if email is None or password is None:
            abort(400)
  
        user = User.objects(email=email).first()

        if not user or not user.verify_password(password):
            return {'status': 'error', 'message': 'The email does not exist or password is wrong'}
        if not user.is_activated:
            return {'status': 'error', 'message': 'The account has not been activated'}

        token = user.generate_auth_token(expiration=360000)
        redis_store.set(str(user.id), token)
        return {'token': token}


fbUserParser = reqparse.RequestParser()
fbUserParser.add_argument('fbid', type=str)
fbUserParser.add_argument('fbtoken', type=str)
fbUserParser.add_argument('fbemail', type=str)

class FBUserAPI(Resource):
    def post(self):
        args = fbUserParser.parse_args()
        fb_id = args['fbid']
        fb_token = args['fbtoken']
        fb_email = args['fbemail']
        if fb_id is None or fb_token is None or fb_email is None:
            abort(400)    # missing arguments
        
        fbuser_info = requests.get('https://graph.facebook.com/me?access_token=%s' %fb_token).json()
        if not fbuser_info.get('id') or fb_id != fbuser_info['id']:
            abort(406)
        
        user = User(email=fb_email, fb_id=fb_id)
        try:
            user.save()
        except:
            return {'status': 'error', 'message': 'FBname has already existed'}

        token = user.generate_auth_token(expiration=360000)
        redis_store.set(str(user.id), token)
        return ({'status': 'success', 'token': token}, 201)


class FBLoginAPI(Resource):
    def post(self):
        args = fbUserParser.parse_args()
        fb_id = args['fbid']
        fb_token = args['fbtoken']   
        if fb_id is None or fb_token is None:
           abort(400)

        fbuser_info = requests.get('https://graph.facebook.com/me?access_token=%s' %fb_token).json()
        if not fbuser_info.get('id') or fb_id != fbuser_info['id']:
            abort(406)

        fb_email = args['fbemail']
        user = User.objects(email=fb_email).first()
        
        if user is None:
            user = User(email=fb_email, fb_id=fbuser_info['id'])
            user.save()

        token = user.generate_auth_token(expiration=360000)
        redis_store.set(str(user.id), token)
        return {'token': token}


activateAccountParser = reqparse.RequestParser()
activateAccountParser.add_argument('token', type=str)
class ActivateAPI(Resource):
    def get(self):
        args = activateAccountParser.parse_args()
        token = args['token']
        if token is None:
            abort()

        user_id = load_token(token)
        user = User.objects(id=user_id).first()
        if user is None:
            abort(400)
        user.is_activated = True
        user.save()

        return "Your account has been activated!"

