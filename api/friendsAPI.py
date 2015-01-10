from flask import request, abort
from flask.ext.restful import Resource, reqparse
from model.friend import Friend
from model.profile import Profile
from model.request import Request
from util.userAuth import auth_required
from util.serialize import friends_list_serialize, requests_list_serialize

friendsParser = reqparse.RequestParser()
friendsParser.add_argument('profile_id', type=str)

class FriendsListAPI(Resource):
    @auth_required
    def get(self, user_id):
        # load profile 
        friends =  Friend.objects(user=user_id).only('friends_list').first()
        if friends is None:
            return abort(400)

        return friends_list_serialize(friends.friends_list)

    @auth_required
    def post(self, user_id):
        args = friendsParser.parse_args()
        profile_id = args['profile_id']

        if profile_id is None:
            abort(400)

        friend_profile = Profile.objects(id=profile_id).only('user').first()
        if friend_profile is None:
            abort(400)

        success = Friend.objects(user=user_id).only('friends_list').update_one(add_to_set__friends_list=profile_id)
        if success is 0:
            friends = Friend(user=user_id, friends_list=[profile_id])
            friends.save()

        user_profile = Profile.objects(user=user_id).only('id').first()
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

        success = Friend.objects(user=user_id).only('friends_list').update_one(pull__friends_list=profile_id)
        if success is 0:
            abort(400)

        return {'status': 'success', 'message': 'The user has been delete from your friend list'}

class FriendsRequestAPI(Resource):
    @auth_required
    def get(self, user_id):
        print user_id
        request =  Request.objects(user=user_id).only('requests_list').first()
        if request is None:
            return {}

        return requests_list_serialize(request.requests_list)  

    @auth_required
    def delete(self, user_id):
        args = friendsParser.parse_args()
        profile_id = args['profile_id']

        if profile_id is None:
            abort(400)

        success = Request.objects(user=user_id).only('requests_list').update_one(pull__requests_list=profile_id)
        if success is 0:
            abort(400)

        return {'status': 'success', 'message': 'The user has been delete from your friends requests list'}



