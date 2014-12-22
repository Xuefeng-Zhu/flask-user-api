from flask import abort
from flask.ext.restful import Resource, reqparse
from model.user import User
from model.redis import redis_store

userParser = reqparse.RequestParser()
userParser.add_argument('username', type=str)
userParser.add_argument('password', type=str)


class UserAPI(Resource):
    def post(self):
        args = userParser.parse_args()
        username = args['username']
        password = args['password']
        if username is None or password is None:
            abort(400)    # missing arguments
        user = User(username=username)
        user.hash_password(password)
        try:
            user.save()
        except:
            return {'status': 'error', 'message': 'username has already existed'}
        token = user.generate_auth_token(expiration=360000)
        redis_store.set(username, token)
        return ({'status': 'success', 'username': user.username, 'token': token}, 200)


class LoginAPI(Resource):
    def post(self):
        args = userParser.parse_args()
        username = args['username']
        password = args['password']
        if username is None or password is None:
            abort(400)
        user = User.objects(username=username)[0]
        if not user or not user.verify_password(password):
            abort(400)
        token = user.generate_auth_token(expiration=360000)
        redis_store.set(username, token)
        return {'token': token}