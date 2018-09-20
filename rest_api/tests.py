from copy import deepcopy
import unittest
import json

from rest_api import models

from .views import app


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

    def test_item_not_exist(self):
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
        order = {"Client_Name": "some_name", "Restaurant": "some_restaurant", "Detail":"Detail", "Quantity": "string", "Date":"Date", "Actions": "Actions"}
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
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.get_data())
        self.assertEqual(data["order"]["Actions"], "Pending")
        self.assertEqual(self.backup_orders["Pending"]['Actions'], "Approved")  

    def test_update_error(self):
        # cannot edit non-existing order
        order = {"Actions": "Pending"}
        response = self.app.put(BAD_ORDER_URL,
                                data=json.dumps(order),
                                content_type='application/json')
        self.assertEqual(response.status_code, 500)

        # Actions field cannot take int
        order = {"Actions": 5}
        response = self.app.put(GOOD_ORDER_URL,
                                data=json.dumps(order),
                                content_type='application/json')
        self.assertEqual(response.status_code, 500)


    def tearDown(self):
        # reset app.orders to initial state
        app.orders = self.backup_orders


if __name__ == "__main__":
    unittest.main()


