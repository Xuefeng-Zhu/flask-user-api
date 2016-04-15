from flask_redis import Redis
from flask.ext.mongoengine import MongoEngine

redis_store = Redis()
db = MongoEngine()