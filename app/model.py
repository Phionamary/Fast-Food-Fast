import datetime

orders = []


class Orders(object):

    

    def __init__(self, Request_ID, Client_Name, Restaurant, Detail, Quantity, Date, Actions):
        self.Request_ID = len(orders) + 1
        self.Client_Name = Client_Name
        self.Restaurant = Restaurant
        self.Detail = Detail
        self.Quantity = Quantity
        self.Date = datetime.datetime.now()
        self.Actions = Actions

    def to_json(self):
        
        data = {'Request_ID': self.Request_ID,"Client_Name":self.Client_Name,
        "Restaurant":self.Restaurant,"Detail":self.Detail, "Quantity": self.Quantity,
        "Date": self.Date,"Actions": self.Actions}

        return data


    def add_order(self, Request_ID, Client_Name, Restaurant, Detail, Quantity, Date, Actions):
        
        order = {'Request_ID': Request_ID,'Client_Name': Client_Name,'Restaurant': Restaurant, 'Detail':Detail, 'Quantity': Quantity, 'Date':Date, 'Actions': Actions}
        orders.append(order)
        return order

    









