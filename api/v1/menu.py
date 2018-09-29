import datetime

import psycopg2
from api.v1.models import DatabaseConnection


class Menu():
    def __init__(self, Item_ID, Food, Restaurant, Price, Detail):
        self.Item_ID = Item_ID
        self.Food = Food
        self.Restaurant = Restaurant
        self.Price = Price
        self.Detail = Detail
        self.conn = psycopg2.connect(host="localhost", port="5434", database="phiona", user="postgres")
        
    def create_cursor(self):
        self.cur = self.conn.cursor()
        return self.cur


    def create_new_item(self):
        new_item = """INSERT INTO Menu(Food, Restaurant, Price, Detail)
        VALUES ('{}', '{}', '{}', '{}');""".format(self.Food,self.Restaurant,self.Price, self.Detail)      
        self.cur.execute(new_item)
        self.conn.commit()
        return "Thisitem has been added to the menu "

    def get_item_by_id(self):
        item = """SELECT FROM Menu where Item_ID_id="{0}" """.format(self.Item_ID)
        self.cur.execute(item)
        single_item = self.cur.fetchone() 
        return single_item

    def get_all_items(self):
        all_items = """SELECT * FROM Menu WHERE Item_ID='{}'""".format(self.Item_ID)
        self.cur.execute(all_items)
        items = self.cur.fetchall() 
        return items