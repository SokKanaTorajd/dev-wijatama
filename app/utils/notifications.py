from flask import session
from app.tasks.notification import db


def notif():
    notifikasi=db.get_notif(session['id'])
    n = sum(map(lambda x: x[3]!=True, notifikasi))
    session['notifikasi'] = n
