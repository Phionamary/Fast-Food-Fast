import datetime

import psycopg2

class Menu():
    def __init__(self):
        self.conn = psycopg2.connect(host="localhost", port="5434", database="fastfoodfast", user="postgres")

        self.cur = self.conn.cursor()


    
    def create_item(self, Item_ID, User_id, Food, Restaurant, Price, Detail):
        self.Item_ID = Item_ID
        self.User_id = User_id
        self.Food = Food
        self.Restaurant = Restaurant
        self.Price = Price
        self.Detail = Detail
        

    def add_new_item(self):
        new_item = """INSERT INTO Menu(Food, Restaurant, Price, Detail, User_id)
        VALUES (%s, %s, %s, %s, %s) RETURNING (Food, Restaurant, Price, Detail, User_id)"""      
        self.cur.execute(new_item, [self.Food,self.Restaurant,self.Price, self.Detail, self.User_id])
        
        return self.cur.fetchone

    def get_item_by_id(self):
        item = """SELECT FROM Menu where Item_ID = "{0}" """.format(self.Item_ID)
        self.cur.execute(item)
        single_item = self.cur.fetchone() 
        return single_item


    def get_all_items(self):
        all_items = """SELECT * FROM Menu WHERE Item_ID='{}'""".format(self.Item_ID)
        self.cur.execute(all_items)
        items = self.cur.fetchall() 
        return items


