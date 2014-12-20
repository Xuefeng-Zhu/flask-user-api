from flask.ext.mongoengine import MongoEngine
from flask.ext.bcrypt import Bcrypt
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

SECRET_KEY = 'flask is cool'

db = MongoEngine()
bcrypt = Bcrypt()

class User(db.Document):
    username = db.StringField(unique=True)
    password_hash = db.StringField()

    def hash_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=3600):
        s = Serializer(SECRET_KEY, expires_in=expiration)
        return s.dumps(self.username)


