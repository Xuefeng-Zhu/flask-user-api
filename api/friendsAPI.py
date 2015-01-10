from flask import request, abort
from flask.ext.restful import Resource, reqparse
from model.friends import Friends
from util.userAuth import auth_required
from util.serialize import friends_list_serialize

friendsParser = reqparse.RequestParser()
friendsParser.add_argument('profile_id', type=str)

class FriendsListAPI(Resource):
    @auth_required
    def get(self, user_id):
        # load profile 
        friends =  Friends.objects(user=user_id).only('friends_list').select_related()

        if len(friends) is 0:
            return {}

        return friends_list_serialize(friends[0].friends_list)

    @auth_required
    def post(self, user_id):
        args = friendsParser.parse_args()
        profile_id = args['profile_id']

        if profile_id is None:
            abort(400)

        success = Friends.objects(user=user_id).only('friends_list').update_one(add_to_set__friends_list=profile_id)

        if success is 0:
            friends = Friends(user=user_id, friends_list=[profile_id])
            friends.save()

        return {'status': 'success', 'message': 'The user has been added to your friend list'}


