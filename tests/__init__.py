""" Inintialisation file for tests"""
from database.app import app

#Test data
test_user_data = {
    "Username": "phiona",
    "Email": "phiona@example.com",
    "Password": "phii",
    "Role": "Admin"
}

test_sign_in = {
    "Username": "phiona",
    "Email": "phiona@example.com",
    "password": "phii"
}


wrong_test_user_data = {
    "Username": "phiona",
    "Email": "phiona@example.com",
    "Password": "phii",
    "Role": "Admin"
}

wrong_test_sign_in = {
   "Username": "phiona"
}

test_wrong_sign_in = {
   "Username": "phiona",
    "Email": "phiona@example.com",
    "password": "phii"
}
