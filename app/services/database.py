import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=os.getenv('HOST'),
            user=os.getenv('USER'),
            password=os.getenv('PASSWORD'),
            database=os.getenv('DATABASE'),
            ssl_ca=os.getenv('SSL_CA_PATH')
        )
        if connection.is_connected():
            print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_query(connection, query=None, procedure=None, params=None):
    cursor = connection.cursor(buffered=True)
    result = None
    try:
        if procedure:
            cursor.callproc(procedure, params)
            for result_set in cursor.stored_results():
                result = result_set.fetchall()
        elif query:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
        connection.commit()
        result = cursor.fetchall()
    except Error as e:
        print(f"The error '{e}' occurred")
    return result

def fetch_query(connection, query, params=None):
    cursor = connection.cursor(dictionary=True)
    result = None
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
        return result