import re
from functools import wraps
import datetime, timedelta
import jwt
from pyisemail import is_email
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, jsonify, make_response, request, redirect
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token,get_jwt_identity)

from app.models import DatabaseConnection
from app.menu import Menu, Items
from app.orders import Orders
from app.users import Users


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
            'Request_ID': "Request_ID",
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


def process_menu_json(var):
    ''' Function to process adding menu item info from browser'''
    now = datetime.datetime.now()

    try:
        item = {
            'User_id': "User_id",
            'Restaurant': var["Restaurant"], 
            'Detail':var['Detail'],
            'Price': var["Price"], 
            'Food': var["Food"]
        }
        return item

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
            user = Users()
            user.get_user_by_name(data['Username'])
            username = user.get_user_by_name(user.Username)
            
        except:
            return make_response(jsonify({'message': 'Invalid token'}), 401)
        return f(username, *args, **kwargs)
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

    username = user.get_user_by_name(user.Username)
    

    if process_user_json(data) is "parameter missing":
        return make_response(jsonify({'message': 'parameter missing'}), 400)
    
    try:
        name = username[1]
        print(name)

        return make_response(jsonify({'Message': 'User already exists'}), 400)

       

    except:
        
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

    try:
        
        if check_password_hash(desired_user[3], data['Password']):
            token = jwt.encode({'Username': desired_user[1], 'exp': datetime.datetime.utcnow() +
                                datetime.timedelta(minutes=20)},
                               app.config['SECRET_KEY'])
            return make_response(jsonify({'Token': token.decode('UTF-8')}), 200)
        return make_response(jsonify({'Message': 'Invalid login'}), 401)
        

    except:
        
        if desired_user is 'failed':
            return make_response(jsonify({'Message': 'User does not exist'}), 400)




@app.route('/api/v1/orders/<int:User_id>', methods=['POST'])
# @token_header
def make_new_order(User_id):
    """
    End Point to create an order
    """
    if request.method == "POST":
        data = process_order_json(request.json)
        if data == "parameter missing" or not all(data.values()):
            return make_response(jsonify({'message': 'parameter missing'}), 400)


    new_order = Orders()
    new_order.create_order(None, "", data['Restaurant'], data['Detail'], data['Quantity'], data['Actions'], data['Date'])
    new_order.add_new_order()

    return jsonify(new_order.to_json()) , 201

@app.route('/api/v1/orders', methods=['GET'])

def get_all_orders():
    """
    End Point get all orders
    """

    resultlist = Orders()
    resultlist.get_orders()

    orders_list = resultlist.get_orders()
    
    return make_response(jsonify({'orders': orders_list})), 200



@app.route('/api/v1/orders/<int:Request_ID>', methods=['GET'])

def single_order(Request_ID):
    """
    End Point to get an single order
    """

    if request.method == "GET":

        your_order = Orders()
        desired_order = your_order.get_order_by_id(Request_ID)

        if desired_order:
            return make_response(jsonify({'Orders': desired_order})), 200

        else:
            return make_response(jsonify({'Message': 'Order does not exist'})), 404


@app.route('/api/v1/orders/<int:Request_ID>', methods=['PUT'])

def update_order_status(Request_ID):
    """
    End Point to update the status of an order
    """
    data = process_edit_json(request.json)
    if data == "parameter missing":
        return make_response(jsonify({'message': 'parameter missing'}), 400)

    order = Orders()
    desired_order = order.get_order_by_id(Request_ID)
    print (desired_order)
    # order.update_order_status(Request_ID, data["Actions"])

    if desired_order:
        # desired_order.update_order_status("", data['Actions'])
        order.update_order_status(Request_ID, data["Actions"])
        return make_response(jsonify({'Message': 'Status updated'})), 200

    else:
        return make_response(jsonify({'Message': 'No such order'})), 404

@app.route('/api/v1/menu', methods = ['GET'])

def get_all_menu_items():
    """Endpoint to retrieve the menu"""
    menu = Items()
    menu.get_all_items()

    menu_list = menu.get_all_items()
    
    return make_response(jsonify({'menu': menu_list})), 200

@app.route('/api/v1/menu', methods = ['POST'])

def add_menu_item():
    if request.method == "POST":
        data = process_menu_json(request.json)
        if data == "parameter missing" or not all(data.values()):
            return make_response(jsonify({'message': 'parameter missing'}), 400)

    menu_item = Items()
    menu_item.create_item(None, data['Food'], data['Restaurant'], data['Price'], data['Detail'])

    new_item = menu_item.add_new_item()

    return "item added successfully"

    # return jsonify(new_item.to_json()) , 201


if __name__ == '__main__':

    DatabaseConnection().create_users_table()
    DatabaseConnection().create_menu_table()
    DatabaseConnection().create_orders_table()
    
    app.run(debug=True)
