from model import db

class Friends(db.Document):
	user = db.ReferenceField('User')
	friends_list = db.ListField(db.ReferenceField('Profile'))