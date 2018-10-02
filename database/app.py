import datetime, timedelta
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

#set up the JWTExtended
app.config['SECRET_KEY'] = 'fast-food-fast'
# jwt = JWTManager(app)


@app.route('/')
def index():
    """
    End Point for the index page
    """
    return jsonify({'Message': 'Hello'}), 200

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
    now = datetime.datetime.now()

    try:
        user = {
            'Username': var['Username'],
            'Email': var['Email'],
            'Password': var['Password'],
            'Role': var['Role'],
            'Created_at': now.strftime("%Y-%m-%d %H:%M")
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
            'Username': var['Username'],
            'Password': var['Password']
        }
        return user

    except:
        error = "parameter missing"
        return error


def token_header(f):
    ''' Function to get the token in the header'''
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'token' in request.headers:
            token = request.headers['token']

        if not token:
            return make_response(jsonify({'message': 'No auth token'}), 401)
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            user = Users.add_new_user(data['Username'], data['Email'], data['Password'], data['Role'])
            desired_user = user.get_user_by_name(data['Username'])

        except:
            return make_response(jsonify({'message': 'Invalid token'}), 401)
        return f(desired_user, *args, **kwargs)
    return decorated

@app.route('/api/v1/auth/signup', methods=['POST'])
def create_a_user():
    """
    End Point to create an account for a user
    """
    data = process_user_json(request.json)

    hashed_password = generate_password_hash(data['Password'], method='sha256')
    user = Users()
    user.create_user("", data['Username'], data['Email'], hashed_password, data['Role'])

    username = user.get_user_by_name(data['Username'])

    if process_user_json(data) is "parameter missing":
        return make_response(jsonify({'message': 'parameter missing'}), 400)

    if username is not 'failed':
        return make_response(jsonify({'Message': 'User already exists'}), 400)

    else:
        if is_email(data['Email']) and re.match("^[A-Za-z0-9_-]*$", data['Username']):
            if user.add_new_user():
                return make_response(jsonify({'Message': 'User created'})), 201

            else:
                return make_response(jsonify({'Message': 'User not created'})), 400
        
        else:
            return make_response(jsonify({'Message': 'invalid input'}), 400)


@app.route('/api/v1/auth/login', methods=['POST'])
def sign_in_a_user():
    """
    End Point to log a user into their account
    """
    data = process_signin_json(request.json)
    if data == "parameter missing":
        return make_response(jsonify({'message': 'parameter missing'}), 400)

    user = Users()
    desired_user = user.get_user_by_name(data['Username'])
    print(desired_user)

    if desired_user is 'failed':
        return make_response(jsonify({'Message': 'User does not exist'}), 400)
    
    else:
        if check_password_hash(desired_user[3], data['Password']):
            token = jwt.encode({'Username': desired_user[1], 'exp': datetime.datetime.utcnow() +
                                datetime.timedelta(minutes=20)},
                               app.config['SECRET_KEY'])
            return make_response(jsonify({'Token': token.decode('UTF-8')}), 200)
    return make_response(jsonify({'Message': 'Invalid login'}), 401)

@app.route('/api/v1/orders', methods=['GET'])
@token_header
def get_all_orders():
    """
    End Point get all orders
    """

    data = process_order_json(request.json)
    if data == "parameter missing":
        return make_response(jsonify({'message': 'parameter missing'}), 400)

    resultlist = Orders()
    resultlist.create_order("", "", data['Restaurant'], data['Detail'],  data['Actions'], data['Date'])
    resultlist.get_all_orders()
    return make_response(jsonify({'orders': resultlist})), 200


@app.route('/api/v1/orders', methods=['POST'])
@token_header
def make_new_order(User_id):
    """
    End Point to create an order
    """
    if request.method == "POST":
        data = process_order_json(request.json)
        if data == "parameter missing" or not all(data.values()):
            return make_response(jsonify({'message': 'parameter missing'}), 400)


    order = Orders()
    order.create_order("", "", data['Restaurant'], data['Detail'],  data['Actions'], data['Date'])
    order.add_new_order()

    return make_response(jsonify({'Message': 'Order created'})), 201


@app.route('/api/v1/orders/<int:Request_ID>', methods=['GET'])
@token_header
def single_entry(Request_ID):
    """
    End Point to get an single order
    """

    if request.method == "GET":
        data = process_order_json(request.json)
        if data == "parameter missing" or not all(data.values()):
            return make_response(jsonify({'message': 'parameter missing'}), 400)

    order = Orders()
    desired_order = order.get_order_by_id(data['Request_ID'], data['User_id'])

    if desired_order:
        return make_response(jsonify({'Orders': desired_order})), 200
    else:
        return make_response(jsonify({'Message': 'No orders yet'})), 404


@app.route('/api/v1/entries/<int:entry_no>', methods=['PUT'])
@token_header
def update_order_status(Request_ID, Actions):
    """
    End Point to update the status of an order
    """
    data = process_edit_json(request.json)
    if data == "parameter missing":
        return make_response(jsonify({'message': 'parameter missing'}), 400)

    order = Orders()
    desired_order = order.get_order_by_id(data['Request_ID'], data['Actions'])
    desired_order.update_order_status

    if desired_order:
        desired_order.update_order_status(Request_ID, data['Actions'])
        return make_response(jsonify({'Message': 'Status updated'})), 200

    else:
        return make_response(jsonify({'Message': 'No such order'})), 404


@app.route('/api/v1/orders/<int:Request_ID>', methods=['DELETE'])
@token_header
def delete_an_order(Request_ID):
    """
    End Point to delete an existing order
    """

    order = Orders()
    desired_order = order.get_order_by_id(data['Request_ID']) 
    desired_order.delete_order
  
    return make_response(jsonify({'Message': desired_order})), 200



@app.route('/api/v1/profile', methods=['GET'])
@token_header
def view_profile(User_id):
    """
    End Point to view user profile
    """
    response = database_users.get_profile(User_id)
    return make_response(jsonify(response), 200)


   
if __name__ == '__main__':
    DatabaseConnection().create_users_table()
    DatabaseConnection().create_menu_table()
    DatabaseConnection().create_orders_table()
    
    app.run(debug=True)
