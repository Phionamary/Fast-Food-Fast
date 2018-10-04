"""Module to test login/signup user activity """
import unittest


from tests.base import TestingClass

from tests import (test_user_data, test_sign_in,wrong_test_user_data, wrong_test_sign_in, test_wrong_sign_in, test_order, wrong_test_order)



class UserTests(TestingClass):
    """Class to test endpoints"""

    def test_user_signup(self):
        """Method to test signup"""
        response = self.user_create()
        self.assertEqual(response.status_code, 400)
        self.assertIn('User already exists', str(response.data))

    def test_user_signup_wrong(self):
        """Method to test wrong signup"""
        response = self.wrong_user()
        self.assertEqual(response.status_code, 400)
        self.assertIn('User already exists', str(response.data))

    def test_user_already_exists(self):
        """Method to test existing user"""
        response = self.user_create()
        self.assertEqual(response.status_code, 400)
        self.assertIn('User already exists', str(response.data))

    def test_can_login_user(self):
        """Method to test signin"""
        response = self.user()
        self.assertEqual(response.status_code, 400)

    def test_user_login_with_no_info(self):
        """Method to test sign in with missing parameter"""
        response = self.wrong_details()
        self.assertIn('parameter missing', str(response.data))

    def test_wrong_user_login(self):
        """Method to test sign in with wrong detail"""
        response = self.wrong_sign_in()
        self.assertEqual(response.status_code, 400)
        self.assertIn('parameter missing', str(response.data))

    def test_hello_world(self):
        """Method to test hello world"""
        response = self.helo()
        self.assertIn('Hello', str(response.data))
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
