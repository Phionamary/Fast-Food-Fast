from copy import deepcopy
import unittest
import json

from app import model

from .model import orders, Orders

from app.views import app

test_order= {"Request_ID": 1,"Client_Name": "Client_Name",
                "Restaurant": "Restaurant", "Detail":"Detail", "Quantity": 1,   
                "Date":"Date", "Actions": "Actions"}


BASE_URL = 'http://127.0.0.1:5000/api/v1/orders'
BAD_ORDER_URL = '{}/5'.format(BASE_URL)
GOOD_ORDER_URL = '{}/3'.format(BASE_URL)


class TestFlaskApi(unittest.TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True


    #test if all orders are displayed
    def test_get_all_orders(self):
        test_user = app.test_client(self)
        response = test_user.get("/api/v1/orders", content_type="application/json")
        self.assertEqual(response.status_code,200)


    def test_empty_list(self):
        response = self.app.get(BASE_URL)
        data = json.loads(response.get_data())
        if len(data) == 0:
            self.assertIn("No orders have been placed yet", data["message"])

    def test_API_get_one_order(self):
        # Tests to show one  questions
        test_user = app.test_client(self)
        test_user.post('/api/v1/orders',data=json.dumps(test_order),content_type="application/json")
        response = test_user.get('/api/v1/orders/1',content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_order_does_not_exist(self):
        response = self.app.get(BAD_ORDER_URL)
        self.assertEqual(response.status_code, 404)

    def test_API_can_create_new_orders(self):
        test_user=app.test_client(self)
        response=test_user.post('/api/v1/orders',data=json.dumps(test_order),content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_post_validations(self):
        # missing value field = bad
        order = {"Client_Name": "some_name", "Restaurant": "some_restaurant", "Detail":"Detail", "Date":"Date", "Actions": "Actions"}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(order),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)


        # quantity field cannot take str
        order = {"Client_Name": "some_name", "Restaurant": "some_restaurant", "Detail":"Detail", "Quantity": "string", "Date":"Date"}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(order),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

        #empty string for client name 
        order = {"Client_Name": " ", "Restaurant": "some_restaurant", "Detail":"Detail", "Date":"Date"}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(order),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)


        # customer name cannot be int 

        order = {"Client_Name": 5867, "Restaurant": "some_restaurant", "Detail":"Detail", "Date":"Date"}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(order),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)


        #trailing space on client name
        order = {"Client_Name": " Some_Name", "Restaurant": "some_restaurant", "Detail":"Detail", "Date":"Date"}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(order),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # empty order details 
        order = {"Client_Name": "Some_Name", "Restaurant": "some_restaurant", "Detail":" ", "Date":"Date"}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(order),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)


        # order details cannot be int
        order = {"Client_Name": "Some_Name", "Restaurant": "some_restaurant", "Detail":586, "Quantity": 20}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(order),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)


        # quantity cannot be a string
        order = {"Client_Name": "Some Name", "Restaurant": "some_restaurant", "Detail":"Some_Details", "Quantity": "Some quantity","Date":"Date"}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(order),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # valid: all required fields, quantity takes int
        
        response = self.app.post(BASE_URL,
                                 data=json.dumps(test_order),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())


        # cannot add order with same order ID again
        order = {"Client_Name": "some_name", "Restaurant": "some_restaurant", "Detail":"Detail", "Quantity": 5, "Date":"Date", "Actions": "Actions"}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(order),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)


    def test_update(self):
        order = {"Actions": "Pending"}
        response = self.app.put(GOOD_ORDER_URL,
                                data=json.dumps(order),
                                content_type='application/json')
        self.assertEqual(response.status_code, 404)  


    def test_update_error(self):
        # cannot edit non-existing order
        order = {"Actions": "Pending"}
        response = self.app.put(BAD_ORDER_URL,
                                data=json.dumps(order),
                                content_type='application/json')
        self.assertEqual(response.status_code, 404)

        # Actions field cannot take int
        order = {"Actions": 5}
        response = self.app.put(GOOD_ORDER_URL,
                                data=json.dumps(order),
                                content_type='application/json')
        self.assertEqual(response.status_code, 404)


    def test_delete_order(self):
        test_user = app.test_client(self)
        test_user.delete('/api/v1/orders/<int:Request_ID>', data=json.dumps(test_order), content_type="application/json")
        response = test_user.delete('/api/v1/orders/1')
        ids = [order['Request_ID'] for order in orders]
        if 1 in ids:
            self.assertEqual(response.status_code, 200)



if __name__ == "__main__":
    unittest.main()


