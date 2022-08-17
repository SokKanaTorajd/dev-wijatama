from app import config
import pymysql

class SQLDatabase():
    def __init__(self):
        self.db = None
        self.cursor = None
        self.host = config.SQL_DB_HOST
        self.user = config.SQL_DB_USER
        self.pwd = config.SQL_DB_PWD
        self.db_name = config.SQL_DB_NAME

    def open_conn(self):
        """
        open database connection
        """
        self.db = pymysql.connect(
            host=self.host,user=self.user,
            password=self.pwd,db=self.db_name
        )
        self.cursor = self.db.cursor()
    
    def close_conn(self):
        """
        close database connection
        """
        self.db.close()
    
    def login(self, username, password):
        self.open_conn()
        q = f"SELECT id, username, password, nama_lengkap FROM users \
                WHERE username='{username}' and password='{password}'"
        self.cursor.execute(q)
        login_data = self.cursor.fetchone()
        self.close_conn()
        return login_data
    
    # USER

    def get_user_by_id(self, user_id):
        self.open_conn()
        q = f"SELECT id, username, password, nama_lengkap, email \
             FROM users WHERE id='{user_id}'"
        self.cursor.execute(q)
        user_data = self.cursor.fetchone()
        self.close_conn()
        return user_data
    
    def add_user(self, user_data):
        self.open_conn()
        q = "INSERT INTO \
            users (username, password, nama_lengkap, email) \
            values ('{}', '{}', '{}', '{}')".format(user_data[0], \
                user_data[1], user_data[2], user_data[3])
        self.cursor.execute(q)
        self.db.commit()
        self.close_conn()
    
    def update_user(self, user_data):
        self.open_conn()
        q = "UPDATE users SET \
            username='{}', password='{}', nama_lengkap='{}', email='{}' \
            WHERE id='{}'".format(user_data[0], user_data[1], \
                user_data[2], user_data[3], user_data[4])
        self.cursor.execute(q)
        self.db.commit()
        self.close_conn()
    
    def delete_user(self, user_id):
        self.open_conn()
        q = f"DELETE FROM users WHERE id='{user_id}'"
        self.cursor.execute(q)
        self.db.commit()
        self.close_conn()

    # END USER

    # NOTIFICATION

    def get_notif(self, user_id):
        self.open_conn()
        q = f"SELECT message, created_at FROM notifications \
            WHERE user='{user_id} ORDER BY created_at DESC LIMIT 5'"
        self.cursor.execute(q)
        notifications = [(message, created_at) for message, created_at in self.cursor.fetchall()]
        self.close_conn()
        return notifications
    
    def create_notif(self, notif_data):
        self.open_conn()
        q = "INSERT INTO notifications (user, message, created_at) \
            values ('{}', '{}', '{}')".format(notif_data[0], notif_data[1], notif_data[2])
        self.cursor.execute(q)
        self.db.commit()
        self.close_conn()
    
    def update_notif(self, notif_data):
        self.open_conn()
        q = "UPDATE notifications SET updated_at='{}', is_read=true \
            WHERE user='{}' AND is_read=false".format(notif_data[0], notif_data[1])
        self.cursor.execute(q)
        self.db.commit()
        self.close_conn()

    # END NOTIFICATION
