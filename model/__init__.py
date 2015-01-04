from flask_redis import Redis
from flask.ext.mongoengine import MongoEngine
from flask.ext.bcrypt import Bcrypt

redis_store = Redis()
db = MongoEngine()
bcrypt = Bcrypt()
