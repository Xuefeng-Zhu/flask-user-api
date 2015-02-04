from flask import request, abort
from flask.ext.restful import Resource, reqparse
from model.profile import Profile
from util.userAuth import auth_required
from util.serialize import serialize, profile_search_serialize
import boto
import os

profileParser = reqparse.RequestParser()
profileParser.add_argument('username', type=str)
profileParser.add_argument('school', type=str)
profileParser.add_argument('intro', type=str)
profileParser.add_argument('page', type=int)


class ProfileAPI(Resource):

    @auth_required
    def get(self, user_id):
        """
        Load the user's profile
        """
        profile = Profile.objects(user=user_id).first()
        if profile is None:
            return {}

        return serialize(profile)

    @auth_required
    def post(self, user_id):
        """
        Edit the user's profile if the profile exists
        Otherwise, create a new profile document
        """
        args = profileParser.parse_args()
        username = args['username']
        school = args['school']
        intro = args['intro']

        profile = Profile.objects(user=user_id).first()
        if profile is None:
            profile = Profile(
                user=user_id, username=username, school=school, intro=intro)
            profile.save()
        else:
            profile.username = username
            profile.school = school
            profile.intro = intro
            profile.save()

        return serialize(profile)


class ProfileIconAPI(Resource):

    @auth_required
    def post(self, user_id):
        """
        Upload user's profile icon
        """
        uploaded_file = request.files['upload']
        filename = "_".join([user_id, uploaded_file.filename])

        # upload the file to S3 server
        conn = boto.connect_s3(os.environ['S3_KEY'], os.environ['S3_SECRET'])
        bucket = conn.get_bucket('profile-icon')
        key = bucket.new_key(filename)
        key.set_contents_from_file(uploaded_file)

        # update the user's profile document
        profile = Profile.objects(user=user_id).first()
        if profile is None:
            profile = Profile(user=user_id, profile_icon=
                              'https://s3-us-west-2.amazonaws.com/profile-icon/%s' % filename)
            profile.save()
        else:
            profile.profile_icon = 'https://s3-us-west-2.amazonaws.com/profile-icon/%s' % filename
            profile.save()

        return serialize(profile)


class SearchProfileAPI(Resource):

    @auth_required
    def get(self, user_id):
        """
        Search users with either username or school
        """
        args = profileParser.parse_args()
        username = args['username']
        school = args['school']
        page = args['page']
        if (username is None and school is None):
            abort(400)
        if page is None:
            page = 0

        profiles = Profile.objects.only('username', 'profile_icon', 'school')
        if username is not None:
            profiles = profiles.filter(username__icontains=username)
        if school is not None:
            profiles = profiles.filter(school=school)

        return profile_search_serialize(profiles[10 * page:10 * (page + 1)])
