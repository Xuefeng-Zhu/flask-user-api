from user import db

class Profile(db.Document):
	user_email = db.EmailField(unique=True)
	profile_icon = db.URLField()
	school = db.StringField()
	lol_id = db.StringField()
	dota_id = db.StringField()
	hh_stone_id = db.StringField()

