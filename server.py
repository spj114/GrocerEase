from flask import Flask, request, jsonify
from sql_connection import get_sql_connection
import products_dao
import uom_dao
import orders_dao
import json
from datetime import datetime
import traceback

db_connection = None

def get_db_connection_for_request():
    global db_connection
    if db_connection is None or not db_connection.is_connected():
        db_connection = get_sql_connection()
    
    if db_connection is None or not db_connection.is_connected():
        print("CRITICAL: Database connection is not available for the request.")
        return None
    return db_connection

app = Flask(__name__)

@app.errorhandler(503)
def service_unavailable_error(e):
    return jsonify(error=str(e), message="Database connection is currently unavailable."), 503

@app.errorhandler(Exception)
def handle_generic_exception(e):
    error_details = traceback.format_exc()
    print(f"An unhandled exception occurred: {e}\n{error_details}")
    return jsonify(error="An internal server error occurred.", message=str(e)), 500


@app.route('/getProducts', methods=['GET'])
def get_products_route():
    conn = get_db_connection_for_request()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 503
    try:
        products = products_dao.get_all_product(conn)
        response = jsonify(products)
        response.headers.add("Access-Control-Allow-Origin", '*')
        return response
    except Exception as e_route:
        print(f"Error in /getProducts: {e_route}\n{traceback.format_exc()}")
        return jsonify({"error": "Failed to retrieve products", "details": str(e_route)}), 500

@app.route('/getUOM', methods=['GET'])
def get_uom_route():
    conn = get_db_connection_for_request()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 503
    try:
        uoms = uom_dao.get_uoms(conn)
        response = jsonify(uoms)
        response.headers.add("Access-Control-Allow-Origin", '*')
        return response
    except Exception as e_route:
        print(f"Error in /getUOM: {e_route}\n{traceback.format_exc()}")
        return jsonify({"error": "Failed to retrieve UOMs", "details": str(e_route)}), 500

@app.route('/insertProduct', methods=['POST'])
def insert_product_route():
    conn = get_db_connection_for_request()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 503
    try:
        request_payload = json.loads(request.form['data'])
        product_id = products_dao.insert_new_product(conn, request_payload)
        response = jsonify({'product_id': product_id})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 201
    except KeyError:
        return jsonify({"error": "Missing 'data' field in form"}), 400
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format in 'data' field"}), 400
    except Exception as e_route:
        print(f"Error in /insertProduct: {e_route}\n{traceback.format_exc()}")
        return jsonify({"error": "Failed to insert product", "details": str(e_route)}), 500

@app.route('/deleteProduct', methods=['POST'])
def delete_product_route():
    conn = get_db_connection_for_request()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 503
    try:
        product_id_to_delete = request.form['product_id']
        rows_affected = products_dao.delete_product(conn, product_id_to_delete)
        if rows_affected > 0:
            response_data = {'message': 'Product deleted successfully', 'product_id': product_id_to_delete, 'rows_affected': rows_affected}
            status_code = 200
        else:
            response_data = {'message': 'Product not found or not deleted', 'product_id': product_id_to_delete, 'rows_affected': rows_affected}
            status_code = 404
        response = jsonify(response_data)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, status_code
    except KeyError:
        return jsonify({"error": "Missing 'product_id' field in form"}), 400
    except Exception as e_route:
        print(f"Error in /deleteProduct: {e_route}\n{traceback.format_exc()}")
        return jsonify({"error": "Failed to delete product", "details": str(e_route)}), 500

@app.route('/insertOrder', methods=['POST'])
def insert_order_route():
    conn = get_db_connection_for_request()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 503
    try:
        request_payload = json.loads(request.form['data'])
        if 'datetime' not in request_payload or not request_payload['datetime']:
             request_payload['datetime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        order_id = orders_dao.insert_order(conn, request_payload)
        response = jsonify({'order_id': order_id})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 201
    except KeyError:
        return jsonify({"error": "Missing 'data' field in form or required sub-fields in order data"}), 400
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format in 'data' field"}), 400
    except Exception as e_route:
        print(f"Error in /insertOrder: {e_route}\n{traceback.format_exc()}")
        return jsonify({"error": "Failed to insert order", "details": str(e_route)}), 500

@app.route('/getAllOrders', methods=['GET'])
def get_all_orders_route():
    conn = get_db_connection_for_request()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 503
    try:
        orders = orders_dao.get_all_orders(conn)
        response = jsonify(orders)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e_route:
        print(f"Error in /getAllOrders: {e_route}\n{traceback.format_exc()}")
        return jsonify({"error": "Failed to retrieve orders", "details": str(e_route)}), 500

if __name__ == '__main__':
    print("Starting Python Flask Server for Grocery Store Management System")
    app.run(host='0.0.0.0', port=5000, debug=True)