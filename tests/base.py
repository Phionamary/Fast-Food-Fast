"""Base module with test helper functions"""
import unittest
import json

from app.app import app
from app.models import DatabaseConnection
from app.menu import Menu
from app.orders import Orders
from app.users import Users

from tests import (test_user_data, test_sign_in,wrong_test_user_data, wrong_test_sign_in, test_wrong_sign_in, test_order, wrong_test_order)


database = DatabaseConnection()


class TestingClass(unittest.TestCase):

    """Base Class for Testing the API"""
    def create_app(self):
        app.config['DEBUG'] = True
        return app
    
    def setUp(self):
        self.client = app.test_client(self)

        self.conn = DatabaseConnection()
        self.conn.create_users_table()
        self.conn.create_orders_table()
        self.conn.create_menu_table()

        # self.cur = self.conn.cursor()

    def tearDown(self):
        pass
        # clear_user_table = "DELETE from Users CASCADE"
        # self.cur.execute(clear_user_table)


    def test_user_create_token(self):
        """Function to create login token"""
        test_user = app.test_client(self)
        test_user.post("/api/v1/auth/signup", data=json.dumps(test_user_data), content_type="application/json")
        response = test_user.post('/api/v1/auth/login', data=json.dumps(test_sign_in),content_type='application/json')
        token = response.json
        return token


    def test_user(self):
        """Function to signin"""
        test_user = app.test_client(self)
        test_user.post("/api/v1/auth/signup", data=json.dumps(test_user_data), content_type="application/json")
        response = test_user.post('/api/v1/auth/login',data=json.dumps(test_sign_in),content_type='application/json')
        return response


    def test_user_create(self):
        """Function to create a user"""
        test_user = app.test_client(self)
        response = test_user.post("/api/v1/auth/signup", data=json.dumps(test_user_data),content_type="application/json")
        return response


    def test_wrong_details(self):
        """Function test login with missing login info"""
        test_user = app.test_client(self)
        response = test_user.post("/api/v1/auth/login", data=json.dumps(wrong_test_sign_in),content_type="application/json")
        return response


    def test_wrong_user(self):
        test_user = app.test_client(self)
        """Function to test wrong user input"""
        response = test_user.post("/api/v1/auth/signup", data=json.dumps(wrong_test_user_data),content_type="application/json")
        return response


    def test_helo(self):
        """Function to test hello world"""
        test_user = app.test_client(self)
        response = test_user.get('/', content_type="application/json")
        return response


    def test_error_page(self):
        """Function to test 404 errors"""
        test_user = app.test_client(self)
        response = test_user.get('/3/', content_type="application/json")
        return response

    def test_create_order(self):
        "Function to test thata user can create an order"
        test_user = app.test_client(self)
        response = test_user.post('/api/v1/orders', data=json.dumps(test_order),content_type='application/json')
        return response

    def test_get_an_order(self):
        """Function to all get an order"""
        test_user = app.test_client(self)
        response = test_user.get("/api/v1/orders", content_type="application/json")
        return response