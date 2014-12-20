from user import db

class Todo(db.Document):
    text = db.StringField()
