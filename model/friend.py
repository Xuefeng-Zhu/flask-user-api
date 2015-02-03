from model import db


class Friend(db.Document):
    """
    Document to store list of a user's friends list
    """
    user = db.ReferenceField('User')
    friends_list = db.ListField(db.ReferenceField('Profile'))
