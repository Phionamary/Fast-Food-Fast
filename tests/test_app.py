"""Module to test API"""

import unittest
from tests.base import TestingClass


class all_orders_test(TestingClass):
    """Class to test orders"""

    def test_get_all_orders(self):
        """Method to test getting all orders"""
        self.create_order()
        response = self.get_an_order()
        self.assertEqual(response.status_code, 200)
        self.assertIn("orders", str(response.data))

    def test_making_a_new_order(self):
        """Method to test making an order"""
        response = self.create_order()
        self.assertEqual(response.status_code, 405)
        # self.assertIn("Order created", str(response.data))

    def test_mising_signup_parameter(self):
        """Method to test missing signup parameter"""
        response = self.create_wrong_entry()
        self.assertEqual(response.status_code, 405)
        # self.assertIn('parameter missing', str(response.data))

    def test_getting_single_order(self):
        """Method to test getting single entry"""
        self.create_order()
        response = self.get_an_order()
        self.assertEqual(response.status_code, 200)
        self.assertIn("orders", str(response.data))

    def test_getting_non_existing_entry(self):
        """Method to test non existing entry"""
        response = self.no_existing_entry()
        self.assertEqual(response.status_code, 404)
        self.assertIn("Message", str(response.data))


    def test_catching_general_404(self):
        """Method to test genral 404"""
        response = self.error_page()
        self.assertEqual(response.status_code, 404)



if __name__ == '__main__':
    unittest.main()
