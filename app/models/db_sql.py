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
            values ('%s', '%s', '%s', '%s')"%(user_data)
        self.cursor.execute(q)
        self.db.commit()
        self.close_conn()
    
    def update_user(self, user_data):
        self.open_conn()
        q = "UPDATE users SET \
            username='%s', password='%s', nama_lengkap='%s', email='%s' \
            WHERE id='%s'"%(user_data)
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
        q = f"SELECT messages, received_at WHERE user_id='{user_id}'"
        self.cursor.execute(q)
        notifications = [(message, received_at) for message, received_at in self.cursor.fetchall()]
        self.close_conn()
        return notifications
    
    def create_notif(self, notif_data):
        self.open_conn()
        print(notif_data)
        q = "INSERT INTO notifications (user, messages, created_at) values ('%s', '%s', '%s')"%(notif_data)
        self.cursor.execute(q)
        self.db.commit()
        self.close_conn()
    
    def update_notif(self, notif_data):
        self.open_conn()
        q = "UPDATE notifications SET received_at='%s' WHERE user_id='%s'"%(notif_data)
        self.cursor.execute(q)
        self.db.commit()
        self.close_conn()

    # END NOTIFICATION
