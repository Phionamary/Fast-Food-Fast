import datetime

import psycopg2


class Users():

    def __init__(self, User_id, Username, Email, Password, Role, Created_at):
        self.User_id = User_id
        self.Username = Username
        self.Email = Email
        self.Password = Password
        self.Role = Role
        self.Created_at = Created_at
        self.conn = psycopg2.connect(host="localhost", port="5434", database="fastfoodfast", user="postgres")

    def create_cursor(self):
        self.cur = self.conn.cursor()
        return self.cur
        

    def add_new_user(self):
        new_user = """INSERT INTO Users(Username, Email, Password, Role, Created_at) 
        VALUES ('{}', '{}', '{}', '{}', '{}');""".format(self.Username, self.Email, self.Password, self.Role, self.Created_at)
        self.cur.execute(new_user)
        self.conn.commit()
        return True



    def get_user_by_id(self):
        user = """SELECT * FROM Users WHERE User_id="{}" """.format(self.User_id)
        self.cur.execute(user)
        single_user = self.cur.fetchone()
        return single_user



    def get_all_user(self):
        users = """SELECT * FROM Users;"""
        self.cur.execute(users)
        all_users = self.cur.fetchall() 
        return all_users 


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

    def get_profile(self, User_id):
        """Method to get user profile"""
        profile = ("select Username,Email,Role,Created_at(Users.User_id)\
                   from Users left join Orders on Orders.User_id=Users.User_id\
                   where Users.User_id={} group by Users.User_id"
                   .format(self.User_id))
        self.cur.execute(profile)
        user = self.cur.fetchall()
        return user