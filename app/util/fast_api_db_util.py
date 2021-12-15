import psycopg2
from psycopg2.extras import RealDictCursor
import time


def get_db_cursor():
    while True:
        try:
            conn = psycopg2.connect(host='localhost', database='fastapi',
                                    user='postgres', password='postgres', cursor_factory=RealDictCursor)
            cursor = conn.cursor()
            print("Database connection successfuly established")
            break
        except Exception as err:
            print(f"Connecting to database failed with error {err}")
            time.sleep(5)
    return conn, cursor
