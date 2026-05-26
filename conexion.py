import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

def conectar():
    connection = psycopg.connect(
        dbname = os.getenv('DB_NAME'),
        user = os.getenv('USER'),
        password = os.getenv('PASSWORD'),
        host = os.getenv('HOST'),
        port = os.getenv('PORT')
    )
    return connection