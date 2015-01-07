from flask import abort
from flask.ext.restful import Resource, reqparse
from model.user import User
from model import redis_store
from userAuth import auth_required 


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

