# import sqlite3
# from app.core.config import DB_PATH

# def get_connection():
#     DB_PATH.parent.mkdir(parents=True, exist_ok=True)
#     return sqlite3.connect(DB_PATH)


import pymysql
import os
import ssl

def get_connection():
    return pymysql.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB"),
        cursorclass=pymysql.cursors.DictCursor,
        # ssl={"ca": os.getenv("MYSQL_SSL_CA_PATH")}
    )
