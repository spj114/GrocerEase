def get_uoms(connection):
    cursor = connection.cursor()
    query = ("SELECT uom_id, uom_name FROM uom")
    cursor.execute(query)

    response = []
    for (uom_id, uom_name) in cursor:
        response.append({
            'uom_id': uom_id,
            'uom_name': uom_name
        })
    
    cursor.close()
    return response

if __name__ == '__main__':
    from sql_connection import get_sql_connection
    
    print("Testing uom_dao.py...")
    connection = get_sql_connection()
    if connection and connection.is_connected():
        print("Successfully connected for UOM test.")
        uoms = get_uoms(connection)
        print("Fetched UOMs:")
        for uom in uoms:
            print(uom)
    else:
        print("Failed to connect for UOM test.")