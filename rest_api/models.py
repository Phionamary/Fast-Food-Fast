orders = []

class Orders(object):

    def __init__(self, Request_ID, Client_Name, Restaurant, Detail, Quantity, Date, Actions):
        self.Request_ID = Request_ID
        self.Client_Name = Client_Name
        self.Restaurant = Restaurant
        self.Detail = Detail
        self.Quantity = Quantity
        self.Date = Date
        self.Actions = Actions

    def to_json(self):
        return{'Request_ID': self.Request_ID,'Client_Name': self.Client_Name,'Restaurant': self.Restaurant, 'Detail':self.Detail, 'Quantity': self.Quantity, 'Date':self.Date, 'Actions': self.Actions}


order1 = Orders(1, "Mulindwa Joshua", "Pizza Hut", "Large Chicken Pizza with extra toppings", 2, "10/10/2018", "Delivered")
orders.append(order1.to_json())

order2 = Orders(2, "Nalwooga Mistress",	"Roosters_The FoodHub",	"Quarter Chicken with lots of barbeque sauce, Fries, Krest", 1, "10/10/2018", "Delivered")
orders.append(order2.to_json())

order3 = Orders(3, "Kimuli Rogers", "Pizza Bond", "Large steak pizza. Lots of toppings", 3, "10/10/2018", "Approved")
orders.append(order3.to_json())

order4 = Orders(4, "Rosemary Nakitte", "KFC Bukoto", "A large bucket of chicken wings, family size fries and a large coke", 2, "10/09/2018", "Approved")
orders.append(order4.to_json())

order5 = Orders(5, "Nassanga Ann", "Pizza Bond", "Large steak pizza. Lots of toppings", 5, "10/10/2018", "Pending")
orders.append(order5.to_json())

order6 = Orders(6, "Phiona Mary Kigai",	"KFC Bukoto", "A large bucket of chicken wings, family size fries and a large coke", 1, "10/09/2018", "Pending")
orders.append(order6.to_json())







