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

GCP_PROJECT_ID = os.environ.get('PROJECT_ID')
GCP_BUCKET_NAME = os.environ.get('GCP_BUCKET_NAME')
GCP_KEY_ID = os.environ.get('Key_ID')
GCP_KEY = os.environ.get('KEY')
GCP_CLIENT_EMAIL = os.environ.get('CLIENT_EMAIL')
GCP_CLIENT_ID = os.environ.get('CLIENT_ID')
GCP_AUTH_URI = os.environ.get('AUTH_URI')
GCP_TOKEN_URI = os.environ.get('TOKEN_URI')
GCP_AUTH_PROVIDER_CERT_URL = os.environ.get('AUTH_PROVIDER_URL')
GCP_CLIENT_CERT_URL = os.environ.get('CLIENT_CERT_URL')
GCP_CREDS = os.environ.get('GCP_CREDS')