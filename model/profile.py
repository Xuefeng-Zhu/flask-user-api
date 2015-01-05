from model import db

class Profile(db.Document):
	user = db.ReferenceField('User')
	username = db.StringField()
	profile_icon = db.URLField()
	school = db.StringField()
	intro = db.StringField()
	game_info = db.ReferenceField('GameInfo')