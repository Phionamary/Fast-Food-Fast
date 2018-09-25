from flask import Flask, jsonify, abort, make_response, request
import datetime


from .models import orders

NOT_FOUND = 'Not found'
BAD_REQUEST = 'Bad request'


app = Flask (__name__)

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


@app.route('/api/v1/orders', methods=['GET'])
def get_all_orders():
    
    response = jsonify({'orders': orders})
    if len(orders) == 0:
        return jsonify({"message": "No orders have been placed yet"})
    return response


@app.route('/api/v1/orders/<int:Request_ID>', methods=['GET'])
def get_particular_order(Request_ID):
    order = _get_order(Request_ID)
    if not order:
        abort(404)
    return jsonify({'orders': order})


@app.route('/api/v1/orders', methods=['POST'])
def create_new_order():
    if len(orders) == 0:
        abort(400)
    if not request.json or 'Client_Name' not in request.json or 'Quantity' not in request.json:
        abort(400)
    order_id = orders[-1].get("Request_ID") + 1

    Request_ID = request.json.get('Request_ID')
    if _record_exists(Request_ID):
        abort(400)

    Client_Name = request.json.get('Client_Name')
    if len (Client_Name) ==0:
        abort(400)
    if Client_Name == " ":
        abort(400)
    if Client_Name ==  "Some_Name":
        abort(400)

    Quantity = request.json.get('Quantity')
    if type(Quantity) is not int:
        abort(400)

    Restaurant = request.json.get('Restaurant')
    if type(Restaurant) is not str:
        abort(400)

    Detail = request.json.get('Detail')
    if type(Detail) is not str:
        abort(400)
    if Detail == " ":
        abort(400)

    #Date = request.json.get('Date')
    Date = datetime.datetime.now()
    '''if type(Date) is not datetime:
        abort(400)'''

    Actions = request.json.get('Actions')
    
    order = {'Request_ID': order_id,'Client_Name': Client_Name,'Restaurant': Restaurant, 'Detail':Detail, 'Quantity': Quantity, 'Date':Date, 'Actions': Actions}
    orders.append(order)
    return jsonify({'order': order}), 201


@app.route('/api/v1/orders/<int:Request_ID>', methods=['PUT'])
def update_order_status(Request_ID):
    order = _get_order(Request_ID)
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
    order = _get_order(Request_ID)
    if len(order) == 0:
        abort(404)
    orders.remove(order[0])
    return jsonify({}), 204


if __name__ == '__main__':
    app.run(debug=True)