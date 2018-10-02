import datetime

import psycopg2


class Orders():

    def __init__(self, Request_ID, User_id, Restaurant, Detail,  Actions, Date):
        self.Request_ID = Request_ID
        self.User_id = User_id
        self.Restaurant = Restaurant
        self.Detail = Detail
        self.Actions = Actions
        self.Date = Date
        self.conn = psycopg2.connect(host="localhost", port="5434", database="fastfoodfast", user="postgres")

    def create_cursor(self):
        self.cur = self.conn.cursor()
        return self.cur

    def add_new_order(self):
        new_order = """INSERT INTO Events(User_id, Restaurant, Detail, Actions, Date) 
        VALUES ('{}','{}', '{}', '{}', {}')""".format(self.User_id, self.Restaurant, self.Detail, self.Actions, self.Date)        
        self.cur.execute(new_order)
        self.conn.commit()
        return True 

    def get_order_by_id(self): 
        #obtaining order for a particular user
        order = """SELECT * FROM Orders WHERE Request_ID="{}" and User_id = "{}" """.format(self.Request_ID, self.User_id)
        self.cur.execute(order)     
        return self.cur.fetchone() 

    def get_all_orders(self):
        all_orders = """SELECT * FROM Orders """
        self.cur.execute(all_orders)
        return self.cur.fetchall() 

        #for a particular user
        users_orders = """SELECT * FROM Orders WHERE User_id = "{}" """.format(self.User_id)
        self.cur.execute(users_orders)
        return self.cur.fetchall

    def update_order_status(self):
        edit_status = ("UPDATE Orders WHERE Request_ID= '{}' AND Actions='{}' ".format(self.Request_ID,self.Actions))
        self.cur.execute(edit_status)
        return self.cur.fetchone()

    def delete_order(self, User_id, Request_ID):
        """Method to delete an entry"""
        delete = ("DELETE FROM Orders WHERE Request_ID={} and \
                  User_id='{}'".format(
                      self.Request_ID, self.User_id))
        self.cur.execute(delete)
        return 'Order Successfully deleted'


