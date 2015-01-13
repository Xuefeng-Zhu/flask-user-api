from model import db


class Profile(db.Document):
    user = db.ReferenceField('User')
    username = db.StringField()
    profile_icon = db.URLField()
    school = db.StringField()
    intro = db.StringField()

    def checkInfo(self, username, school):
        if self.username != username:
            return False
        if self.school != school:
            return False
        return True
