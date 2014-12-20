from flask import request, abort
from flask.ext.restful import Resource
from model.redis import redis_store
from model.todo import Todo
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


SECRET_KEY = 'flask is cool'

def verify_auth_token(token):
    s = Serializer(SECRET_KEY)
    try:
        username = s.loads(token)
    except SignatureExpired:
        return False    # valid token, but expired
    except BadSignature:
        return False    # invalid token
    if redis_store.get(username) == token:
        return True
    else:
        return False


class TodoAPI(Resource):
    def get(self):
        token = request.form['token']
        if not verify_auth_token(token):
            abort(400)
        todos =  Todo.objects.all()
        result = []
        for todo in todos:
            result.append({'todo': todo.text})
        return result


    def put(self):
        todo = Todo(text=request.form['data'])
        todo.save()
        return {'status': 'success'}
