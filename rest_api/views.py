from flask import Flask, jsonify, abort, make_response, request
from models import orders 
import datetime

NOT_FOUND = 'Not found'
BAD_REQUEST = 'Bad request'

app = Flask(__name__)



def _get_order(Request_ID):
    return [order for order in orders if order['Request_ID'] == Request_ID]


def _record_exists(Request_ID):
    return [order for order in orders if order["Request_ID"] == Request_ID]


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': NOT_FOUND}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': BAD_REQUEST}), 400)


@app.route('/api/v1.0/orders', methods=['GET'])
def get_all_orders():
    return jsonify({'orders': orders})


@app.route('/api/v1.0/orders/<int:Request_ID>', methods=['GET'])
def get_particular_order(Request_ID):
    order = _get_order(Request_ID)
    if not order:
        abort(404)
    return jsonify({'orders': order})


@app.route('/api/v1.0/orders', methods=['POST'])
def create_new_order():
    if not request.json or 'Client_Name' not in request.json or 'Quantity' not in request.json:
        abort(400)
    order_id = orders[-1].get("Request_ID") + 1

    Request_ID = request.json.get('Request_ID')
    if _record_exists(Request_ID):
        abort(400)

    Client_Name = request.json.get('Client_Name')

    Quantity = request.json.get('Quantity')
    if type(Quantity) is not int:
        abort(400)

    Restaurant = request.json.get('Restaurant')

    Detail = request.json.get('Detail')

    #Date = request.json.get('Date')
    Date = datetime.datetime.now()
    '''if type(Date) is not datetime:
        abort(400)'''

    Actions = request.json.get('Actions')
    
    order = {'Request_ID': order_id,'Client_Name': Client_Name,'Restaurant': Restaurant, 'Detail':Detail, 'Quantity': Quantity, 'Date':Date, 'Actions': Actions}
    orders.append(order)
    return jsonify({'order': order}), 201


@app.route('/api/v1.0/orders/<int:Request_ID>', methods=['PUT'])
def update_order_status(Request_ID):
    order = _get_order(Request_ID)
    if len(order) == 0:
        abort(404)
    if not request.json:
        abort(400)
    Client_Name = request.json.get('Client_Name', order[0]['Client_Name'])
    Actions = request.json.get('Actions', order[0]['Actions'])

    Client_Name[0]['Client_Name'] = Client_Name
    Actions[0]['Actions'] = Actions
    return jsonify({'order': order[0]}), 200


@app.route('/api/v1.0/orders/<int:Request_ID>', methods=['DELETE'])
def delete_order(Request_ID):
    order = _get_order(Request_ID)
    if len(order) == 0:
        abort(404)
    orders.remove(order[0])
    return jsonify({}), 204

if __name__ == '__main__':
    app.run(debug=True)