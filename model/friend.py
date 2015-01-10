from model import db

class Friend(db.Document):
	user = db.ReferenceField('User')
	friends_list = db.ListField(db.ReferenceField('Profile'))