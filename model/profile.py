from model import db

class Profile(db.Document):
	user_email = db.EmailField(unique=True)
	username = db.StringField()
	profile_icon = db.URLField()
	school = db.StringField()
	intro = db.StringField()
	game_info = db.ReferenceField('GameInfo')