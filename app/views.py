from flask import Flask, jsonify, abort, make_response, request
import datetime

from .data import orders

from .model import Orders



NOT_FOUND = 'Not found'
BAD_REQUEST = 'Bad request'


app = Flask (__name__)

def Order(var):
    order = {'Request_ID': len(orders)+1,
            'Client_Name': var["Client_Name"],
            'Restaurant': var["Restaurant"], 
            'Detail':var['Detail'],
            'Quantity': var["Quantity"], 
            'Date':var["Date"],
            'Actions': var["Actions"]
            }

    return order

def get_single_order(Request_ID):
    return [order for order in orders if order['Request_ID'] == Request_ID]

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': NOT_FOUND}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': BAD_REQUEST}), 400)

@app.route("/")
def index():
    return jsonify({"Hello":"There"})


@app.route('/api/v1/orders', methods=['GET'])
def get_all_orders():
    
    response = jsonify({'orders': orders})

    if len(orders) == 0:
        return jsonify({"message": "No orders have been placed yet"})
    return response


@app.route('/api/v1/orders/<int:Request_ID>', methods=['GET'])
def get_particular_order(Request_ID):
    if request.method=='GET':
        result = [d for d in orders if d.get('Request_ID', '') == Request_ID]
        if result:
            return make_response(jsonify({'orders':result[0]})),200 
        else:
            return make_response(jsonify({'Message':'Order not found'})),404

@app.route('/api/v1/orders', methods=['POST'])
def create_new_order():
    
    if request.method=="POST":
        data=request.json
        new_order = order (data)
        orders.append(new_order)
        return make_response(jsonify({'Message':order})),201


@app.route('/api/v1/orders/<int:Request_ID>', methods=['PUT'])

def update_order_status(Request_ID):
    order = get_single_order(Request_ID)
    if len(order) == 0:
        abort(404)
    if not request.json:
        abort(400)

    Detail = request.json.get('Detail', order[0]['Detail'])
    Actions = request.json.get('Actions', order[0]['Actions'])

    order[0]['Detail'] = Detail
    order[0]['Actions'] = Actions
    return jsonify({'order': order[0]}), 200

@app.route('/api/v1/orders/<int:Request_ID>', methods=['DELETE'])
def delete_order(Request_ID):
    order = get_single_order(Request_ID)

    if len(order) == 0:
        abort(404)
    orders.remove(order[0])
    return jsonify({}), 204



if __name__ == '__main__':
    app.run(debug=True)
