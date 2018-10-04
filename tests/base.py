"""Base module with test helper functions"""

import unittest
import json

from app.app import app
from app.models import DatabaseConnection
from app.users import Users


database = DatabaseConnection()
db = Users()
cursor = db.cur

from tests import (test_user_data, test_sign_in,wrong_test_user_data, wrong_test_sign_in, test_wrong_sign_in, test_order, wrong_test_order, test_menu, wrong_test_menu)


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
        
    # def tearDown(self):

        # clear_user_table = "DELETE from Users CASCADE"
        # cursor.execute(clear_user_table)
        # clear_user_table = "DELETE from Users"
        # cursor.execute(clear_user_table)


    def user_create_token(self):
        """Function to create login token"""
        test_user = app.test_client(self)
        test_user.post("/api/v1/auth/signup", data=json.dumps(test_user_data), content_type="application/json")
        response = test_user.post('/api/v1/auth/login', data=json.dumps(test_sign_in),content_type='application/json')
        token = response.json
        return token


    def user(self):
        """Function to signin"""
        test_user = app.test_client(self)
        test_user.post("/api/v1/auth/signup", data=json.dumps(test_user_data), content_type="application/json")
        response = test_user.post('/api/v1/auth/login',data=json.dumps(test_sign_in),content_type='application/json')
        return response


    def user_create(self):
        """Function to create a user"""
        test_user = app.test_client(self)
        response = test_user.post("/api/v1/auth/signup", data=json.dumps(test_user_data),content_type="application/json")
        return response


    def wrong_details(self):
        """Function test login with missing login info"""
        test_user = app.test_client(self)
        response = test_user.post("/api/v1/auth/login", data=json.dumps(wrong_test_sign_in),content_type="application/json")
        return response


    def wrong_user(self):
        """Function to test wrong user input"""
        test_user = app.test_client(self)
        response = test_user.post("/api/v1/auth/signup", data=json.dumps(wrong_test_user_data),content_type="application/json")
        return response
    
    def wrong_sign_in(self):
        """Function to test sign in with wrong details"""
        test_user = app.test_client(self)
        response = test_user.post("/api/v1/auth/login", data=json.dumps(test_wrong_sign_in),content_type="application/json")
        return response


    def helo(self):
        """Function to test hello world"""
        test_user = app.test_client(self)
        response = test_user.get('/', content_type="application/json")
        return response


    def error_page(self):
        """Function to test 404 errors"""
        test_user = app.test_client(self)
        response = test_user.get('/3/', content_type="application/json")
        return response

    def create_order(self):
        """Function to test that a user can create an order"""
        test_user = app.test_client(self)
        response = test_user.post('/api/v1/orders', headers = self.user_create_token(), data=json.dumps(test_order),content_type='application/json')
        return response

    def get_an_order(self):
        """Function to all get an order"""
        test_user = app.test_client(self)
        response = test_user.get("/api/v1/orders", headers=self.user_create_token(), content_type="application/json")
        return response


    def create_wrong_entry(self):
        """Function to test wrong user order input"""
        test_user = app.test_client(self)
        response = test_user.post('/api/v1/orders',headers=self.user_create_token(), data=json.dumps(wrong_test_order),content_type='application/json')
        return response

    def no_existing_entry(self):
        """Function to test non exisitng order"""
        test_user = app.test_client(self)
        response = test_user.get("/api/v1/order/1", headers=self.user_create_token(),content_type="application/json")
        return response

    def create_menu_item(self):
        """Function to test that a user can add an item to the menu"""
        test_user = app.test_client(self)
        response = test_user.post("/api/v1/menu", headers = self.user_create_token(), data = json.dumps(test_menu), content_type = "application/json")
        return response

    def create_wrong_menu_item(self):
        "Function to test wrong menu item input"
        test_user = app.test_client(self)
        response = test_user.post("/api/v1/menu", headers = self.user_create_token(), data = json.dumps(wrong_test_menu), content_type = "application/json")
        return response

    def add_menu_authentication(self):
        '''Function to test whether only the admin is able to add an item to the menu'''
        test_user = app.test_client(self)
        response = test_user.post('/api/v1/menu', eaders = self.user_create_token(), data=json.dumps(test_menu),content_type='application/json')
        return response
        


