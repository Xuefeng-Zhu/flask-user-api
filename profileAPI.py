from flask import request, abort
from flask.ext.restful import Resource, reqparse
from model.redis import redis_store
from model.profile import Profile
import boto
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
    print redis_store.get(email)
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
        profile =  Profile.objects(user_email=email)
        if profile.first() is None:
        	return {}

        result = {}
        for key in profile:
        	if key != "id":
           	    result[key] = profile[key]
        return result


    def post(self):
    	args = profileParser.parse_args()
        token = args['token']

        # verify token 
        if token is None:
        	abort(400)
        email = verify_auth_token(token) 
        if email is None:
            abort(400)

        school = args['school']
        lol_id = args['lolid']
        dota_id = args['dotaid']

        profile = Profile.objects(user_email=email)
        if profile.first() is None:
            profile = Profile(user_email=email, school=school, lol_id=lol_id, dota_id=dota_id)
            profile.save()
        else:
            profile = profile[0]
            profile.school = school
            profile.lol_id = lol_id
            profile.dota_id = dota_id
            profile.save()
       
        result = {}
        for key in profile:
        	if key != "id":
        		result[key] = profile[key]
        return result

class ProfileIconAPI(Resource):
    def post(self):
        uploaded_file = request.files['upload']

        for file in uploaded_file:
            return uploaded_file[file].filename
        return "success"
        # conn = boto.connect_s3('AKIAI6Y5TYNOTCIHK63Q', 'mmIpQx6mX/oFjZC6snQ7anO0yTOhEbpqPf2pcr0E')
        # bucket = conn.get_bucket('profile-icon')
        # key = bucket.new_key(uploaded_file.filename)
        # key.set_contents_from_file(uploaded_file)
        # return {'file': uploaded_file.filename}
