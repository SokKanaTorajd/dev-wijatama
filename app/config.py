import os

BROKER_URL = os.environ.get('CLOUDAMQP_URL')
MONGODB_URI = os.environ.get('MONGODB_URI')
BACKEND_URI = os.environ.get('BACKEND_URI')
DB_NAME = os.environ.get('DB_NAME')