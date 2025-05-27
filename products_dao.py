def get_all_product(connection):
    cursor = connection.cursor()
    query = (
        "SELECT p.product_id, p.name, p.uom_id, p.price_per_unit, u.uom_name "
        "FROM products p "
        "INNER JOIN uom u ON u.uom_id = p.uom_id"
    )
    cursor.execute(query)

    response = []
    for (product_id, name, uom_id, price_per_unit, uom_name) in cursor:
        response.append({
            'product_id': product_id,
            'name': name,
            'uom_id': uom_id,
            'price_per_unit': float(price_per_unit),
            'uom_name': uom_name
        })
    
    cursor.close()
    return response

def insert_new_product(connection, product):
    cursor = connection.cursor()
    query = ("INSERT INTO products (name, uom_id, price_per_unit) VALUES (%s, %s, %s)")
    
    try:
        data = (
            str(product['name']), 
            int(product['uom_id']), 
            float(product['price_per_unit'])
        )
        cursor.execute(query, data)
        connection.commit()
        last_id = cursor.lastrowid
        cursor.close()
        return last_id
    except Exception as e:
        connection.rollback()
        cursor.close()
        print(f"Error in insert_new_product: {e}")
        raise

def delete_product(connection, product_id):
    cursor = connection.cursor()
    query = ("DELETE FROM products WHERE product_id = %s")
    
    try:
        pid = int(product_id)
        cursor.execute(query, (pid,))
        connection.commit()
        row_count = cursor.rowcount
        cursor.close()
        return row_count
    except Exception as e:
        connection.rollback()
        cursor.close()
        print(f"Error in delete_product: {e}")
        raise

if __name__ == "__main__":
    from sql_connection import get_sql_connection

    print("Testing products_dao.py...")
    connection = get_sql_connection()

    if connection and connection.is_connected():
        print("Successfully connected for products DAO test.")
        print("\n--- Testing get_all_product ---")
        products = get_all_product(connection)
        if products:
            for p in products[:2]: 
                 print(p)
        else:
            print("No products found or error fetching products.")
    else:
        print("Failed to connect for products DAO test.")