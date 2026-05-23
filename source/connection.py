import os
import psycopg
from dotenv import load_dotenv

def connect():
    load_dotenv()

    connection = psycopg.connect(
        dbname = os.getenv('DB_NAME'),
        user = os.getenv('USER'),
        password = os.getenv('PASSWORD'),
        host = os.getenv('HOST'),
        port = os.getenv('PORT')
    )

    return connection