from flask import request, abort
from flask.ext.restful import Resource, reqparse
from model.redis import redis_store
from model.todo import Profile
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


SECRET_KEY = 'flask is cool'

def verify_auth_token(token):
    s = Serializer(SECRET_KEY)
    try:
        email = s.loads(token)
    except SignatureExpired:
        return None    # valid token, but expired
    except BadSignature:
        return None    # invalid token
    if redis_store.get(email) == token:
        return email
    else:
        return None


profileParser = reqparse.RequestParser()
profileParser.add_argument('token', type=str)
profileParser.add_argument('school', type=str)
profileParser.add_argument('lolid', type=str)
profileParser.add_argument('dotaid', type=str)

class ProfileAPI(Resource):
    def get(self):
    	args = profileParser.parse_args()
        token = args['token']

        # verify token 
        if token is None:
        	abort(400)
        email = verify_auth_token(token) 
        if email is None:
            abort(400)

        # load profile 
        profile =  profile.objects(email=email)
        if len(profile) == 0:
        	return {}

        result = {}
        for key in profile:
        	result[key] = profile[key]

        return result


    def post(self):
    	args = profileParser.parse_args()
        token = args['token']
        school = args['school']
        lol_id = args['lolid']
        dota_id = args['dotaid']
        todo = Todo(text=request.form['data'])
        todo.save()
        return {'status': 'success'}

