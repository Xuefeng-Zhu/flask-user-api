from flask import Flask, request, abort
from flask.ext.restful import Resource, Api
from model.user import db, bcrypt
from model.redis import redis_store
from flask_redis import Redis
from userAPI import UserAPI, LoginAPI
from todoAPI import TodoAPI

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'flask-test',
    'host': 'ds027741.mongolab.com',
    'port': 27741,
    'username': 'flask-admin',
    'password': '123123'
}

app.config['REDIS_URL'] = "redis://:123123@pub-redis-17784.us-east-1-2.1.ec2.garantiadata.com:17784/0"

db.init_app(app)
bcrypt.init_app(app)
redis_store.init_app(app)

api = Api(app)


api.add_resource(TodoAPI, '/todos')
api.add_resource(UserAPI, '/users')
api.add_resource(LoginAPI, '/login')

if __name__ == '__main__':
    app.run(debug=True)



