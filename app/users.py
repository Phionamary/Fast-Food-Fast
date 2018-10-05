import datetime

import psycopg2

now = datetime.datetime.now()


class Users():

    def __init__(self):
        self.conn = psycopg2.connect(host="localhost", port="5434", database="fastfoodfast", user="postgres")
        self.conn.autocommit = True
        self.cur = self.conn.cursor()
  
    def create_user(self, User_id, Username, Email, Password, Role):
        self.User_id = User_id
        self.Username = Username
        self.Email = Email
        self.Password = Password
        self.Role = Role
        self.Created_at = now.strftime("%Y-%m-%d %H:%M")
        

    def add_new_user(self):
        print (self.Password)
        try:
            new_user = """INSERT INTO Users(User_id, Username, Email, Password, Role, Created_at) 
            VALUES (DEFAULT,%s, %s, %s, %s, %s) RETURNING User_id, Username, Email, Password, Role, Created_at;"""
            self.cur.execute(new_user, [self.Username,self.Email, self.Password, self.Role, self.Created_at])

            return self.cur.fetchone()
        except:
            return "failed"

    def get_user_by_name(self, Username):
        try:
            user = """SELECT * FROM Users WHERE Username = %s """
            self.cur.execute(user, [Username])
            return self.cur.fetchone()
            
        except:
            return "failed"


    def get_all_user(self):
        users = """SELECT * FROM Users;"""
        self.cur.execute(users)
        all_users = self.cur.fetchall() 
        return all_users 

    def get_user_by_role(self, User_id):
        try:

            user = """SELECT * FROM Users WHERE User_id = %s and Role = 'Admin';"""
            self.cur.execute(user, [User_id])
            return self.cur.fetchall()

        except:
            return "failed"


    def verify_new_user(self, Username, Email):
        """Method to verify a user"""
        signin = (
            "SELECT * FROM Users WHERE Username='{}' \
            or Email='{}'".format(self.Username, self.Email))
        self.cur.execute(signin)
        user = self.cur.fetchall()
        return user

    def select_user_id(self, User_id):
        """Method to get a user-id"""
        signin = ("SELECT * FROM users WHERE User_id='{}'"
                  .format(self.User_id))
        self.cur.execute(signin)
        user = self.cur.fetchall()
        return user

        