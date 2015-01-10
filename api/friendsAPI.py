from flask import request, abort
from flask.ext.restful import Resource, reqparse
from model.friends import Friends
from model.profile import Profile
from model.request import Request
from util.userAuth import auth_required
from util.serialize import friends_list_serialize

friendsParser = reqparse.RequestParser()
friendsParser.add_argument('profile_id', type=str)

class FriendsListAPI(Resource):
    @auth_required
    def get(self, user_id):
        # load profile 
        friends =  Friends.objects(user=user_id).only('friends_list').first()
        if friends is None:
            return {}

        return friends_list_serialize(friends.friends_list)

    @auth_required
    def post(self, user_id):
        args = friendsParser.parse_args()
        profile_id = args['profile_id']

        if profile_id is None:
            abort(400)

        friend_profile = Profile.objects(id=profile_id).first()
        if friend_profile is None:
            abort(400)

        success = Friends.objects(user=user_id).only('friends_list').update_one(add_to_set__friends_list=profile_id)
        if success is 0:
            friends = Friends(user=user_id, friends_list=[profile_id])
            friends.save()

        user_profile = Profile.objects(user=user_id).first()
        success = Request.objects(user=friend_profile.user).update_one(add_to_set__requests_list=user_profile)
        if success is 0:
            friend_request = Request(user=friend_profile.user, type='friends', requests_list=[user_profile])
            friend_request.save()

        return {'status': 'success', 'message': 'The user has been added to your friend list'}

    @auth_required
    def delete(self, user_id):
        args = friendsParser.parse_args()
        profile_id = args['profile_id']

        if profile_id is None:
            abort(400)

        success = Friends.objects(user=user_id).only('friends_list').update_one(pull__friends_list=profile_id)
        if success is 0:
            abort(400)

        return {'status': 'success', 'message': 'The user has been delete from your friend list'}

