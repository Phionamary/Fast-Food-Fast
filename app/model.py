import datetime


class Orders(object):

    orders = []

    def __init__(self, Request_ID, Client_Name, Restaurant, Detail, Quantity, Date, Actions):
        self.Request_ID = len(self.orders) + 1
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
        if not type(Quantity) == int:
            raise ValueError('Quantity must be an Integer!!')

        if not type(Request_ID) == int:
            raise ValueError('Request_ID must be an Integer!!')

        if not type(Actions) == str:
            raise ValueError('Actions must be a string!!')
        if not Actions.strip():
            raise ValueError('status cannot be empty!')

        if not type(Client_Name) == str:
            raise ValueError('Client Name must be a string!!')
        if not Client_Name.strip():
            raise ValueError('Client_Name cannot be empty!')

        if not type(Restaurant) == str:
            raise ValueError("Restaurant must be a string")
        if not Restaurant.strip():
            raise ValueError('Restaurant cannot be empty!')

        if not type(Detail) == str:
            raise ValueError('Detail must be a string!!')
        if not Detail.strip():
            raise ValueError('Detail cannot be empty!')

        if not type(Date) == datetime:
            raise ValueError('Enter valid Date!!')
        if not Date.strip():
            raise ValueError('Date cannot be empty!')
        

        order = {'Request_ID': Request_ID,'Client_Name': Client_Name,'Restaurant': Restaurant, 'Detail':Detail, 'Quantity': Quantity, 'Date':Date, 'Actions': Actions}
        self.orders.append(order)
        return order

    









