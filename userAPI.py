from flask import request, abort
from flask.ext.restful import Resource
from model.user import User
from model.redis import redis_store


class UserAPI(Resource):
    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')
        if username is None or password is None:
            abort(400)    # missing arguments
        user = User(username=username)
        user.hash_password(password)
        try:
            user.save()
        except:
            return {'status': 'error', 'message': 'username has already existed'}
        return ({'username': user.username}, 201)


class LoginAPI(Resource):
    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')
        if username is None or password is None:
            abort(400)
        user = User.objects(username=username)[0]
        if not user or not user.verify_password(password):
            abort(400)
        token = user.generate_auth_token(expiration=360000)
        redis_store.set(username, token)
        return {'token': token}