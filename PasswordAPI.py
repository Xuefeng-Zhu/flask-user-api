from flask import abort
from flask.ext.restful import Resource, reqparse
from model.user import User
from model.profile import Profile
from userAuth import auth_required 
import random


passwordParser = reqparse.RequestParser()
passwordParser.add_argument('old_password', type=str)
passwordParser.add_argument('new_password', type=str)

class ChangePasswordAPI(Resource):
    @auth_required
    def post(self, user_id):
        args = passwordParser.parse_args()
        old_password = args['old_password']
        new_password = args['new_password']
        if old_password is None or new_password is None:
            abort(400)    

        user = User.objects(id=user_id).first()
        if not user.verify_password(old_password):
            return {'status': 'error', 'message': 'old password is not correct'}
        user.hash_password(new_password)
        user.save()

        return {'status': 'success'}


forgetPasswordParser = reqparse.RequestParser()
forgetPasswordParser.add_argument('email', type=str)
forgetPasswordParser.add_argument('username', type=str)
forgetPasswordParser.add_argument('school', type=str)

class ForgetPasswordAPI(Resource):
    def post(self):
        args = forgetPasswordParser.parse_args()
        email = args['email']
        username = args['username']
        school = args['school']

        if email is None or username is None or school is None:
            abort(400, message="missing required arguments")

        user = User.objects(email=email).first()
        if user is None:
            return {'status': 'error', 'message': 'There is no user associated with the email'}

        profile = Profile.objects(user=user).first()

        if not profile.checkInfo(username, school):
            return {'status': 'error', 'message': 'The information does not match the record'}

        temp_password = (''.join(random.choice(string.ascii_uppercase) for x in range(8)))
        user.hash_password(temp_password)

        return {'status': 'success', 'message': 'A temperate password has been emailed to you'}





