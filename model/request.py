from model import db


class Request(db.Document):
    user = db.ReferenceField('User')
    type = db.StringField(required=True)
    requests_list = db.ListField(db.ReferenceField('Profile'))
