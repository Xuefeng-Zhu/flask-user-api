from flask import abort, current_app, request
from model import redis_store
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from functools import wraps

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('token')
        if token is None:
            abort(401)

        s = Serializer(current_app.config.get('SECRET_KEY'))
        try:
            user_id = s.loads(token)
        except SignatureExpired:
            abort(401)    # valid token, but expired
        except BadSignature:
            abort(401)    # invalid token

        if redis_store.get(user_id) == token:
            kwargs['user_id'] = user_id
            return f(*args, **kwargs)
        else:
            abort(401) 

    return decorated_function