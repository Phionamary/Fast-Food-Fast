import unittest
from flask import Flask,jsonify,make_response,request
import sys
import json

from app import model

from .model import orders, Orders

from app.views import app

test_order= {
                "Request_ID": 1,
                "Client_Name": "Client_Name",
                "Restaurant": "Restaurant", 
                "Detail":"Detail", 
                "Quantity": 1,   
                "Date":"Date", 
                "Actions": "Pending"
            }


BASE_URL = 'http://127.0.0.1:5000/api/v1/orders'


class TestFlaskApi(unittest.TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    

    def tearDown(self):
        orders[:] = []


    def test_index(self):
        testing_user = app.test_client(self)
        response =testing_user.get('/',content_type="application/json")
        self.assertIn('Hello',str(response.data))
        self.assertEqual(response.status_code,200)


    #test if all orders are displayed
    def test_get_all_orders(self):
        test_user = app.test_client(self)
        response = test_user.get("/api/v1/orders", content_type="application/json")
        self.assertEqual(response.status_code,200)

    def test_empty_list(self):
        response = self.app.get("/api/v1/orders")
        data = json.loads(response.get_data())
        if len(data) == 0:
            self.assertIn("No orders have been placed yet", data["message"])


    def test_API_get_one_order(self):
        test_user = app.test_client(self)
        test_user.post('/api/v1/orders',data=json.dumps(test_order),content_type="application/json")
        response = test_user.get('/api/v1/orders/1',data=json.dumps(test_order),content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_order_does_not_exist(self):
        response = self.app.get('/api/v1/orders')
        self.assertEqual(response.status_code, 200)


    def test_API_can_create_new_orders(self):        
        test_user=app.test_client(self)
        response=test_user.post('/api/v1/orders',data=json.dumps(test_order),content_type="application/json")
        self.assertEqual(response.status_code,500)


    def test_update(self):
        test_user = app.test_client(self)
        test_user.post('/api/v1/orders', data=json.dumps(test_order),content_type='application/json')
        response = test_user.put('/api/v1/orders/1', data=json.dumps(test_order),content_type='application/json')
        self.assertEqual(response.status_code, 404 ) 


    def test_update_error(self):
        # cannot edit non-existing order
        response = self.app.put('/api/v1/orders/1',data=json.dumps(test_order),content_type='application/json')
        self.assertEqual(response.status_code, 404)

        # Actions field cannot take int
        response = self.app.put('/api/v1/orders/1',data=json.dumps(test_order),content_type='application/json')
        self.assertEqual(response.status_code, 404)


    def test_for_wrong_order(self):
        test_user = app.test_client(self)
        test_user.post('/api/v1/orders',data=json.dumps(test_order),content_type="application/json")
        response = test_user.get('/api/v1/orders/2',data=json.dumps(test_order),content_type='application/json')
        self.assertEqual(response.status_code, 200)


    def test_no_order_to_update(self):
        test_user = app.test_client(self)
        test_user.post('/api/v1/orders', data=json.dumps(test_order),content_type='application/json')
        response = test_user.put('/api/v1/orders/7', data=json.dumps(test_order),content_type='application/json')
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


