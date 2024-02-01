import mysql.connector
from mysql.connector import Error
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_PORT


def create_conn():
    conn = None
    kwargs = {
        "host": MYSQL_HOST,
        "user": MYSQL_USER,
        "password": MYSQL_PASSWORD,
        "database": MYSQL_DB,
    }
    if MYSQL_PORT:
        kwargs["port"] = MYSQL_PORT
    try:
        conn = mysql.connector.connect(**kwargs)
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return conn


def is_mysql_accessible():
    conn = create_conn()
    if conn is not None and conn.is_connected():
        conn.close()
        return True
    return False
