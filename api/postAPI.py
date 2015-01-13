from flask import abort
from flask.ext.restful import Resource, reqparse
from model.post import Post
from model.profile import Profile
from util.userAuth import auth_required
from util.serialize import posts_list_serialize

postParser = reqparse.RequestParser()
postParser.add_argument('content', type=str)
postParser.add_argument('page', type=int)


class PostAPI(Resource):

    @auth_required
    def get(self, user_id):
        args = postParser.parse_args()
        page = args['page']
        if page is None:
            page = 0

        posts = Post.objects().exclude('user')[10 * page: 10 * (page + 1)]
        if posts is None:
            return abort(400)

        return posts_list_serialize(posts)

    @auth_required
    def post(self, user_id):
        args = postParser.parse_args()
        content = args['content']

        profile = Profile.objects(user=user_id).first()
        post = Post(user=user_id, user_profile=profile, content=content)
        post.save()

        return {'status': 'success'}
