import datetime

import psycopg2




class Menu():
    def __init__(self, Item_ID, User_id, Food, Restaurant, Price, Detail):
        self.Item_ID = Item_ID
        self.User_id = User_id
        self.Food = Food
        self.Restaurant = Restaurant
        self.Price = Price
        self.Detail = Detail
        self.conn = psycopg2.connect(host="localhost", port="5434", database="fastfoodfast", user="postgres")

    

    def create_cursor(self):
        self.cur = self.conn.cursor()
        return self.cur


    def create_new_item(self):
        new_item = """INSERT INTO Menu(Food, Restaurant, Price, Detail, User_id)
        VALUES ('{}', '{}', '{}', '{}', {}');""".format(self.Food,self.Restaurant,self.Price, self.Detail, self.User_id)      
        self.cur.execute(new_item)
        self.conn.commit()
        return "This item has been added to the menu "

    def get_item_by_id(self):
        item = """SELECT FROM Menu where Item_ID = "{0}" """.format(self.Item_ID)
        self.cur.execute(item)
        single_item = self.cur.fetchone() 
        return single_item

        #added by a particular user
        item1 = """SELECT FROM Menu where Item_ID = '{0}" and User_id = '{}' """.format(self.Item_ID, self.User_id)
        self.cur.execute(item1)
        single_item1 = self.cur.fetchone
        return single_item1

    def get_all_items(self):
        all_items = """SELECT * FROM Menu WHERE Item_ID='{}'""".format(self.Item_ID)
        self.cur.execute(all_items)
        items = self.cur.fetchall() 
        return items

        #added by particular user
        items1 = """SELECT FROM Menu where Item_ID = '{}" and User_id = '{}' """.format(self.Item_ID, self.User_id)
        self.cur.execute(items1)
        users_items = self.cur.fetchall() 
        return users_items

