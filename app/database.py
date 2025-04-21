import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv
import os 


load_dotenv()

def create_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT", 8080),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        print("Connection to PostgreSQL is successful")
        return conn
    except OperationalError as e:
        print(f"Error: {e}")
        return None