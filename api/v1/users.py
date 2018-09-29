import datetime

import psycopg2
from api.v1.models import DatabaseConnection

class Users():

    def __init__(self, User_id, First_name, Last_name, Email, Password, Created_at):
        self.User_id = User_id
        self.First_name = First_name
        self.Last_name = Last_name
        self.Email = Email
        self.Password = Password
        self.Created_at = Created_at
        self.conn = psycopg2.connect(host="localhost", port="5434", database="phiona", user="postgres")

    def create_cursor(self):
        self.cur = self.conn.cursor()
        return self.cur

    def add_new_user(self):
        new_user = """INSERT INTO Users(First_name, Last_name, Email, Password, Created_at) 
        VALUES ('{}', '{}', '{}', '{}', '{}');""".format(self.First_name, self.Last_name, 
        self.Email, self.Password, self.Created_at)
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


    def verify_new_user(self, First_name, Last_name, Email):
        """Method to verify a user"""
        signin = ("SELECT * FROM Users WHERE First_Name='{}' and Last_Name = '{}' and Email='{}'".format(First_name, Last_name, Email))
        self.cur.execute(signin)
        
        user = self.cur.fetchall()
        return user