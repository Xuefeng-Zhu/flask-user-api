"""
This file stores all flask configuration information
"""

REDIS_URL = "redis://:123123@pub-redis-16551.us-east-1-2.3.ec2.garantiadata.com:16551/0"
MONGODB_SETTINGS = {
    'db': 'flask-test',
    'host': 'ds027741.mlab.com',
    'port': 27741,
    'username': 'flask-test',
    'password': '123123'
}
SECRET_KEY = 'flask is cool'
MAIL_SERVER = 'smtp.mandrillapp.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'zhuxuefeng1994@126.com'
MAIL_PASSWORD = 'GP4r-n8kVAILVe8NepkenQ'
MAIL_DEFAULT_SENDER = 'flaskAPI@github.com'
