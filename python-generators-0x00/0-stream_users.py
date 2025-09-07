import mysql.connector
import os

def stream_users():
    """
    Generator that yields each row from the 'user_data' table one by one.
    """
    db_config = {
        "host": os.getenv("MY_DB_HOST"),
        "user": os.getenv("MY_DB_USER"),
        "password": os.getenv("MY_DB_PASSWORD"),
        "database": "ALX_prodev"
    }

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_data")

        # Single loop to yield rows one by one
        for row in iter(cursor.fetchone, None):
            yield row

    except mysql.connector.Error as e:
        print(f"Database error: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
