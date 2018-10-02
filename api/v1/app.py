import datetime
from functools import wraps
import re
import jwt
from pyisemail import is_email
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, jsonify, make_response, request, redirect
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token,get_jwt_identity)

from models import DatabaseConnection
from menu import Menu
from orders import Orders
from users import Users


app = Flask(__name__)

db = DatabaseConnection()
db.create_users_table()
db.create_orders_table()
db.create_menu_table()

#set up the JWTExtended
app.config['SECRET_KEY'] = 'fast-food-fast'
jwt = JWTManager(app)

database_orders = Orders
database_users = Users
database_menu = Menu

@app.route('/')
def index():
    """
    End Point for the index page
    """
    return jsonify({'Hello': 'There'}), 200



@app.errorhandler(404)
def page_not_found(e):
    """
    End Point to catch 404s
    """
    return make_response(jsonify({'Message': 'Page not found'})), 404

def process_order_json(var):
    ''' Function to process json recieved from browser'''
    try:
        now = datetime.datetime.now()

        order = {
            'User_id': "User_id",
            'Restaurant': var["Restaurant"], 
            'Detail':var['Detail'],
            'Quantity': var["Quantity"], 
            'Date':now.strftime("%Y-%m-%d %H:%M"),
            'Actions': var["Actions"]
        }
        return order

    except:
        error = "parameter missing"
        return error


def process_edit_json(var):
    ''' Function to process order status update info from browser'''
    try:
        order = {
            'Actions': var['Actions']
        }
        return order

    except:
        error = "parameter missing"
        return error


def process_user_json(var):
    ''' Function to process user signup info from browser'''
    try:
        user = {
            'Username': var['Username'],
            'Email': var['Email'],
            'Password': var['Password']
        }
        return user
    except:
        error = "parameter missing"
        return error


def process_signin_json(var):
    ''' Function to process user login info from browser'''
    try:
        user = {
            'Email': var['Email'],
            'Password': var['Password']
        }
        return user

    except:
        error = "parameter missing"
        return error


def token_header(f):
    ''' Function to get the token using the header'''
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'token' in request.headers:
            token = request.headers['token']

        if not token:
            return make_response(jsonify({'message': 'No auth token'}), 401)
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            user = database_users.get_user_by_id(data['User_id'])
            User_id = user[0]['User_id']

        except:
            return make_response(jsonify({'message': 'Invalid token'}), 401)
        return f(User_id, *args, **kwargs)
    return decorated

@app.route('/api/v1/auth/signup', methods=['POST'])
def create_a_user():
    """
    End Point to create an account for a user
    """
    data = process_user_json(request.json)
    if data == "parameter missing":
        return make_response(jsonify({'message': 'parameter missing'}), 400)

    hashed_password = generate_password_hash(data['Password'], method='sha256')
    user = database_users.verify_new_user(data['Username'], data['Email'])

    if not user and is_email(data['Email']) and all(data.values()) and re.match("^[A-Za-z0-9_-]*$", data['Username']):
        database_users.add_new_user(
            data['username'], data['Role'], data['Email'], data['Created_at'], hashed_password)
        return make_response(jsonify({'Message': 'User created'})), 201

    if not all(data.values()) or not re.match("^[A-Za-z0-9_-]*$", data['Username']) or not is_email(data['Email']):
        return make_response(jsonify({'Message': 'invalid input'}), 400)
    return make_response(jsonify({'Message': 'User already exists'}), 400)



@app.route('/api/v1/auth/login', methods=['POST'])
def sign_in_a_user():
    """
    End Point to log a user into their account
    """
    data = process_signin_json(request.json)
    if data == "parameter missing":
        return make_response(jsonify({'message': 'Parameter missing'}), 400)

    user = database_users.get_user_by_id(data['Username'])
    if user:
        if check_password_hash(user[0]['Password'], data['Password']):
            token = jwt.encode({'User_id': user[0]['User_id'], 'exp': datetime.datetime.utcnow() +
                                datetime.timedelta(minutes=20)},
                               app.config['SECRET_KEY'])
            return make_response(jsonify({'Token': token.decode('UTF-8')}), 200)
    return make_response(jsonify({'Message': 'Invalid login'}), 401)


@app.route('/api/v1/orders', methods=['GET'])
@token_header
def get_all_orders(User_id):
    """
    End Point get all orders for a given user
    """
    resultlist = database_orders.get_all_orders(User_id)
    return make_response(jsonify({'orders': resultlist})), 200



if __name__ == "__main__":
    app.run(debug=True)