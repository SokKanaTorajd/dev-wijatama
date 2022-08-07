import os

BROKER_URL = os.environ.get('CLOUDAMQP_URL')
MONGODB_URI = os.environ.get('MONGODB_URI')
BACKEND_URI = os.environ.get('BACKEND_URI')
DB_NAME = os.environ.get('DB_NAME')
IG_POSTS_COLL = 'ig-posts'

SQL_DB_HOST = os.environ.get('SQL_DB_HOST')
SQL_DB_USER = os.environ.get('SQL_DB_USER')
SQL_DB_PWD = os.environ.get('SQL_DB_PWD')
SQL_DB_NAME = os.environ.get('SQL_DB_NAME')

SECRET_KEY = os.environ.get('SECRET_KEY')
