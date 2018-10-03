import datetime

import psycopg2

class Menu:
    def __init__(self):
        self.conn = psycopg2.connect(host="localhost", port="5434", database="fastfoodfast", user="postgres")
        self.conn.autocommit = True
        self.cur = self.conn.cursor()


class Items: 
    cur = None  
    def create_item(self, Item_ID, Food, Restaurant, Price, Detail):
        self.Item_ID = Item_ID
        # self.User_id = User_id
        self.Food = Food
        self.Restaurant = Restaurant
        self.Price = Price
        self.Detail = Detail

    def to_json(self):
        return {"item_ID": self.Item_ID, "Food": self.Food, "Restaurant": self.Restaurant, "Price": self.Price, "Detail": self.Detail}
        

    def add_new_item(self):
        new_item = """INSERT INTO Menu(Food, Restaurant, Price, Detail)
        VALUES (%s, %s, %s, %s) RETURNING (Food, Restaurant, Price, Detail)"""  
        self.curr = Menu().cur    
        self.curr.execute(new_item, [self.Food,self.Restaurant,self.Price, self.Detail])
        print ("added")
        return self.curr.fetchone

    def get_item_by_id(self):
        item = """SELECT FROM Menu where Item_ID = "{0}" """.format(self.Item_ID)
        self.cur.execute(item)
        single_item = self.cur.fetchone() 
        return single_item


    def get_all_items(self):
        try:

            self.curr = Menu().cur
            all_items = """SELECT * FROM Menu """
            self.curr.execute(all_items)
            items = self.curr.fetchall() 
            # print(items)
            return items

        except:
            return "Failed"


