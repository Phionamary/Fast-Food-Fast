import psycopg2

class DatabaseConnection():
    
    def __init__(self):
        self.conn = psycopg2.connect(host="127.0.0.1", port="5434", database="fastfoodfast", user="postgres")
        
    # def create_cursor(self):
        self.cur = self.conn.cursor()
        # return self.cur
        
        
    def create_users_table(self):
        Users = """CREATE TABLE IF NOT EXISTS Users(User_id serial PRIMARY KEY, 
        Username varchar (50) NOT NULL, 
        Email varchar (50) NOT NULL, 
        Password varchar NOT NULL, 
        Role varchar (50) NOT NULL,
        Created_at date)"""

        self.cur.execute(Users)


    def create_orders_table(self):
        Orders = """CREATE TABLE IF NOT EXISTS Orders(Request_ID serial PRIMARY KEY, 
        User_id INTEGER, 
        Restaurant varchar (50) NOT NULL,  
        Detail varchar (50) NOT NULL, 
        Quantity int NOT NULL, 
        Actions varchar (50) NOT NULL, 
        Date date,
        FOREIGN KEY (User_id) REFERENCES Users (User_id) ON DELETE CASCADE)"""

        self.cur.execute(Orders)

    def create_menu_table(self):
        Menu = """CREATE TABLE IF NOT EXISTS Menu(Item_ID serial PRIMARY KEY, 
        Food varchar (50) NOT NULL, 
        Restaurant varchar (50) NOT NULL,  
        Price int NOT NULL, 
        Detail varchar (50) NOT NULL)"""

        self.cur.execute(Menu)

    
    def close_database_connection(self):
        self.conn.commit()
        self.conn.close()
