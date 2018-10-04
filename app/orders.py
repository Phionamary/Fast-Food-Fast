import datetime

import psycopg2
from psycopg2.extras import RealDictCursor

now = datetime.datetime.now()


class Orders():

    def __init__(self):
        self.conn = psycopg2.connect(host="localhost", port="5434", database="fastfoodfast", user="postgres")
        self.conn.autocommit = True
        self.cur = self.conn.cursor(cursor_factory = RealDictCursor)


    def create_order(self, Request_ID, User_id, Restaurant, Detail, Quantity, Actions, Date):
        self.Request_ID = Request_ID
        self.User_id = User_id
        self.Restaurant = Restaurant
        self.Detail = Detail
        self.Quantity = Quantity
        self.Actions = Actions
        self.Date = now.strftime("%Y-%m-%d %H:%M")
    
    def to_json(self):
        return {"Request_ID": self.Request_ID, "User_id": self.User_id, "Restaurant":self.Restaurant, "Detail": self.Detail, "Quantity": self.Quantity, "Actions": self.Actions, "Date": self.Date}

    def add_new_order(self):
        new_order = """INSERT INTO Orders(Request_ID, User_id, Restaurant, Detail, Quantity, Actions, Date) 
        VALUES (DEFAULT, %s, %s, %s, %s, %s, %s) RETURNING Request_ID, User_id, Restaurant, Quantity, Detail, Actions, Date"""        
        self.cur.execute(new_order, (self.User_id, self.Restaurant, self.Detail, self.Quantity, self.Actions, self.Date))
        return self.cur.fetchone()
        

    def get_order_by_id(self, Request_ID): 
        #obtaining order for a particular user
        order = ("SELECT * FROM Orders WHERE Request_ID={}".format(Request_ID))
        self.cur.execute(order)  
        your_order = self.cur.fetchone() 
        # print(your_order)
        return your_order 
        
    def get_orders(self):
        orders = """SELECT * FROM Orders;"""
        self.cur.execute(orders)
        all_orders = self.cur.fetchall() 
        return all_orders 
     
    def get_all_orders(self, User_id):
        """Method to get all orders for a particluar user"""
        orders = ("SELECT Request_ID,Restaurant, Detail, Quantity, Actions, Date FROM Orders \
        WHERE User_id='{}'".format(User_id))
        self.cur.execute(orders)
        return self.cur.fetchall

    def update_order_status(self, Request_ID, Actions, User_id):
        edit_status = ("UPDATE Orders SET Actions = '{}' WHERE Request_ID= {} and User_id = '{}'".format(Actions, User_id, Request_ID))
        self.cur.execute(edit_status)
        return "Successfully updated"

    def delete_order(self, User_id, Request_ID):
        """Method to delete an entry"""
        delete = ("DELETE FROM Orders WHERE Request_ID={} and \
                  User_id='{}'".format(
                      self.Request_ID, self.User_id))
        self.cur.execute(delete)
        return 'Order Successfully deleted'


