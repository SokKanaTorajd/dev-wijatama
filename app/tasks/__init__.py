from celery import Celery
from app import config

worker = Celery(__name__)
worker.conf.broker_url = config.BROKER_URL
worker.conf.result_backend = config.BACKEND_URI
worker.conf.mongodb_backend_settings = {
        'database': 'celery_system_log',
        'taskmeta_collection': 'task_log',
        'connect': False
    }
