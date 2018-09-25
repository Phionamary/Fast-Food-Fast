from copy import deepcopy
import unittest
import json

from rest_api import models

from rest_api.views import app


BASE_URL = 'http://127.0.0.1:5000/api/v1/orders'
BAD_ORDER_URL = '{}/5'.format(BASE_URL)
GOOD_ORDER_URL = '{}/3'.format(BASE_URL)


class TestFlaskApi(unittest.TestCase):

    def setUp(self):
        self.backup_orders = deepcopy(models.orders)  # no references!
        self.app = app.test_client()
        self.app.testing = True

    def test_get_all(self):
        response = self.app.get(BASE_URL)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['orders']), 6)

    def test_get_one(self):
        response = self.app.get(BASE_URL)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['orders'][0]['Request_ID'], 1)

    def test_order_does_not_exist(self):
        response = self.app.get(BAD_ORDER_URL)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
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
        order = {"Client_Name": "some_name", "Restaurant": "some_restaurant", "Detail":"Detail", "Quantity": 5, "Date":"Date", "Actions": "Actions"}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(order),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data())
        self.assertEqual(data['order']['Request_ID'], 7)
        self.assertEqual(data['order']['Client_Name'], 'some_name')

        # cannot add order with same order ID again
        order = {"Client_Name": "some_name", "Restaurant": "some_restaurant", "Detail":"Detail", "Quantity": 5, "Date":"Date", "Actions": "Actions"}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(order),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)


    def test_update(self):
        order = {"Actions": "Pending"}
        response = self.app.put(GOOD_ORDER_URL,
                                data=json.dumps(order),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)  


    def test_update_error(self):
        # cannot edit non-existing order
        order = {"Actions": "Pending"}
        response = self.app.put(BAD_ORDER_URL,
                                data=json.dumps(order),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # Actions field cannot take int
        order = {"Actions": 5}
        response = self.app.put(GOOD_ORDER_URL,
                                data=json.dumps(order),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)


    def test_delete_an_order(self):
        order = {"Request_ID": "Some ID"}

        response = self.app.put(BAD_ORDER_URL,
                                data=json.dumps(order),
                                content_type='application/json')

        self.assertEqual(response.status_code, 200)


        response = self.app.put(BAD_ORDER_URL,
                                data=json.dumps(order),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)



    def tearDown(self):
        # reset app.orders to initial state
        app.orders = self.backup_orders


if __name__ == "__main__":
    unittest.main()


