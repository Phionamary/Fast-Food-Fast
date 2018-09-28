orders = []

#The function loops orders and returns an order with a particluar id

def get_single_order(Request_Id):

    for order in orders:
        if order.Request_Id == Request_Id:
            return order