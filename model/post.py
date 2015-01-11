from model import db
from datetime import datetime

class Post(db.Document):
	user = db.ReferenceField('User')
	user_profile = db.ReferenceField('Profile')
	date = db.DateTimeField(default=datetime.now)
	content = db.StringField()