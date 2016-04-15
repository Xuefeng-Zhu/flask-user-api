from flask import current_app
from model import db
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer)
import hashlib


class User(db.Document):
    """
    Document for a user's account information
    """
    email = db.EmailField(unique=True)
    password_hash = db.StringField()
    fb_id = db.IntField()
    is_activated = db.BooleanField(default=False)

    def hash_password(self, password):
        """
        crypt the raw password and store it into database
        """
        self.password_hash = hashlib.sha224(password).hexdigest()

    def verify_password(self, password):
        """
        check if the password from user matches
        the password stored in the database
        """
        return hashlib.sha224(password).hexdigest() == self.password_hash

    def generate_auth_token(self, expiration=3600):
        """
        generate an authorization token used for API accesss
        """
        s = Serializer(
            current_app.config.get('SECRET_KEY'), expires_in=expiration)
        return s.dumps(str(self.id))
