from app.models import SQLDatabase
from app.tasks import worker


db = SQLDatabase()


@worker.task(name='notification.send_notif')
def send_notif(data):
    db.create_notif(data)
