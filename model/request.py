from model import db


class Request(db.Document):
    """
    Document for a user's friend request list
    """
    user = db.ReferenceField('User')
    type = db.StringField(required=True)
    requests_list = db.ListField(db.ReferenceField('Profile'))
