from flask import abort, current_app
from flask.ext.restful import reqparse
from model import redis_store
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from functools import wraps

authParser = reqparse.RequestParser()
authParser.add_argument('token', type=str)

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        args = authParser.parse_args()
        token = args['token']

        if token is None:
            abort(401)

        s = Serializer(current_app.config.get('SECRET_KEY'))
        try:
            email = s.loads(token)
        except SignatureExpired:
            abort(401)    # valid token, but expired
        except BadSignature:
            abort(401)    # invalid token

        if redis_store.get(email) == token:
            kwargs['email'] = email
            return f(*args, **kwargs)
        else:
            abort(401) 

    return decorated_function