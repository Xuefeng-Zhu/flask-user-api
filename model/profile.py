from model import db


class Profile(db.Document):
    """
    Document for a user's profile information
    """
    user = db.ReferenceField('User')
    username = db.StringField()
    profile_icon = db.URLField()
    school = db.StringField()
    intro = db.StringField()

    def checkInfo(self, username, school):
        """
        check the information from user matches the
        informtion stored in the database
        """
        if self.username != username:
            return False
        if self.school != school:
            return False
        return True
