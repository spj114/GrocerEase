import mysql.connector
import os

__cnx = None

def get_sql_connection():
    global __cnx
    if __cnx is None or not __cnx.is_connected():
        try:
            __cnx = mysql.connector.connect(
                user=os.environ.get('DB_USER', 'root'),
                password=os.environ.get('DB_PASSWORD', ''),
                host=os.environ.get('DB_HOST', '127.0.0.1'),
                database=os.environ.get('DB_NAME', 'grocery_store'),
                auth_plugin='mysql_native_password'
            )
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            __cnx = None
    return __cnx

if __name__ == '__main__':
    print("Running sql_connection.py as main script...")
    connection = get_sql_connection()
    if connection:
        print(f"__main__ test: Connection object received. Is connected: {connection.is_connected()}")
    else:
        print("__main__ test: Failed to get connection object.")