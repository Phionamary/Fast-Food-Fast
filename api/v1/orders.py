import datetime

import psycopg2
from api.v1.models import DatabaseConnection

class Orders():

    def __init__(self, Request_ID, Client_Name, Restaurant, Detail, Actions, Date):
        self.Request_ID = Request_ID
        self.Client_Name = Client_Name
        self.Restaurant = Restaurant
        self.Detail = Detail
        self.Actions = Actions
        self.Date = Date
        self.conn = psycopg2.connect(host="localhost", port="5434", database="phiona", user="postgres")

    def create_cursor(self):
        self.cur = self.conn.cursor()
        return self.cur

    def add_new_order(self):
        new_order = """INSERT INTO Events(Client_Name, Restaurant, Detail, Actions, Date) 
        VALUES ('{}','{}', '{}', '{}', {}')""".format(self.Client_Name, self.Restaurant, self.Detail, self.Actions, self.Date)        
        self.cur.execute(new_order)
        self.conn.commit()
        return True 

    def get_order_by_id(self): 
        order = """SELECT * FROM Orders WHERE Request_ID="{}" """.format(self.Request_ID)
        self.cur.execute(order)     
        return self.cur.fetchone() 

    def get_all_orders(self):
        all_orders = """SELECT * FROM Orders """
        self.cur.execute(all_orders)
        return self.cur.fetchall() 

    def update_order_status(self):
        edit_status = ("UPDATE Orders WHERE Request_ID= '{}' AND Actions='{}' ".format(self.Request_ID,self.Actions))
        self.cur.execute(edit_status)
        return self.cur.fetchone()


