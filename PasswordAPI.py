from flask import abort
from flask.ext.restful import Resource, reqparse
from model.user import User
from model.profile import Profile
from userAuth import auth_required, load_token
from emails import send_forget_password_email
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
forgetPasswordParser.add_argument('token', type=str)
forgetPasswordParser.add_argument('email', type=str)
forgetPasswordParser.add_argument('username', type=str)
forgetPasswordParser.add_argument('school', type=str)

class ForgetPasswordAPI(Resource):
    def get(self):
        args = forgetPasswordParser.parse_args()
        token = args['token']

        if token is None:
            abort(400)

        user_id = load_token(token)
        user = User.objects(id=user_id).first()
        if user is None:
            return {'status': 'error', 'token': 'Token is not valid'}

        temp_password = (''.join(str(random.randint(0, 9)) for x in range(8)))
        user.hash_password(temp_password)
        user.save()
        
        return "Your temperate password is: %s" %temp_password

    def post(self):
        args = forgetPasswordParser.parse_args()
        email = args['email']
        username = args['username']
        school = args['school']

        if email is None or username is None or school is None:
            abort(400)

        user = User.objects(email=email).first()
        if user is None:
            return {'status': 'error', 'message': 'There is no user associated with the email'}

        profile = Profile.objects(user=user).first()
        if not profile.checkInfo(username, school):
            return {'status': 'error', 'message': 'The information does not match the record'}

        token = user.generate_auth_token(expiration=360000)
        send_forget_password_email(email, token)

        return {'status': 'success', 'message': 'An email has been sent to you letting you reset password'}





