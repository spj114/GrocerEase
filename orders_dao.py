from datetime import datetime

def insert_order(connection, order_data_from_request):
    cursor = connection.cursor()

    try:
        order_query = (
            'INSERT INTO orders (customer_name, total_cost, datetime) '
            'VALUES (%s, %s, %s)'
        )
        
        order_datetime_str = order_data_from_request['datetime']

        order_payload = (
            str(order_data_from_request['customer_name']),
            float(order_data_from_request['grand_total']),
            order_datetime_str
        )
        cursor.execute(order_query, order_payload)
        order_id = cursor.lastrowid

        order_details_query = (
            'INSERT INTO order_details (order_id, product_id, quantity, total_price) '
            'VALUES (%s, %s, %s, %s)'
        )
        
        order_details_payload = []
        for detail_record in order_data_from_request['order_details']:
            order_details_payload.append([
                order_id,
                int(detail_record['product_id']),
                float(detail_record['quantity']),
                float(detail_record['total_price'])
            ])
        
        if order_details_payload:
            cursor.executemany(order_details_query, order_details_payload)

        connection.commit()
        cursor.close()
        return order_id

    except Exception as e:
        connection.rollback()
        cursor.close()
        print(f"Error in insert_order: {e}")
        raise

def get_all_orders(connection):
    cursor = connection.cursor()
    query = "SELECT order_id, customer_name, total_cost, datetime FROM orders ORDER BY datetime DESC"
    cursor.execute(query)

    orders_list = []
    for (order_id, customer_name, total_cost, dt) in cursor:
        orders_list.append({
            "order_id": order_id,
            "customer_name": customer_name,
            'total_cost': float(total_cost),
            'datetime': dt.strftime('%Y-%m-%d %H:%M:%S') if isinstance(dt, datetime) else str(dt)
        })
    
    cursor.close()
    return orders_list

if __name__ == '__main__':
    from sql_connection import get_sql_connection
    
    print("Testing orders_dao.py...")
    connection = get_sql_connection()

    if connection and connection.is_connected():
        print("Successfully connected for orders DAO test.")
        print("\n--- Testing get_all_orders ---")
        orders = get_all_orders(connection)
        if orders:
            for o in orders[:2]:
                print(o)
        else:
            print("No orders found or error fetching orders.")
    else:
        print("Failed to connect for orders DAO test.")