import psycopg2

class DatabaseConnection():
    
    def __init__(self):
        self.conn = psycopg2.connect(host="localhost", port="5434", database="fastfoodfast", user="postgres")
        
    def create_cursor(self):
        self.cur = self.conn.cursor()
        return self.cur
        
        
    def create_users_table(self, User_id, Username, Email, Password, Created_at):
        Users = """CREATE TABLE IF NOT EXISTS UsersUsers(User_id serial PRIMARY KEY, 
        Username varchar (50) NOT NULL, 
        Email varchar (50) NOT NULL, 
        Password varchar (50) NOT NULL, 
        Created_at date)"""

        self.cur.execute(Users)


    def create_orders_table(self, Request_ID, User_id, Restaurant, Detail,  Actions, Date):
        Orders = """(Request_ID serial PRIMARY KEY, 
        User_id int REFERENCES Users(User_id), 
        Restaurant varchar (50) NOT NULL,  
        Detail varchar (50) NOT NULL, 
        Quantity int NOT NULL, 
        Actions varchar (50) NOT NULL, 
        Date date)"""

        self.cur.execute(Orders)

    def create_menu_table(self, Item_ID, Food, Restaurant, Price, Detail):
        Menu = """CREATE TABLE IF NOT EXISTS Menu(Item_ID serial PRIMARY KEY, 
        Food varchar (50) NOT NULL, 
        Restaurant varchar (50) NOT NULL,  
        Price int NOT NULL, 
        Detail varchar (50) NOT NULL)"""

        self.cur.exectute(Menu)

    
    def close_database_connection(self):
        self.conn.commit()
        self.conn.close()
