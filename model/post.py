from model import db
from datetime import datetime


class Post(db.Document):
    """
    Document for a user's posts
    """
    user = db.ReferenceField('User')
    user_profile = db.ReferenceField('Profile')
    date = db.DateTimeField(default=datetime.now)
    content = db.StringField()
