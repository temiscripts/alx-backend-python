import os
import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows from 'user_data' in batches.
    Each batch is a list of dictionaries.
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
        cursor.execute("SELECT COUNT(*) FROM user_data")
        total_rows = cursor.fetchone()[0]

        for offset in range(0, total_rows, batch_size):
            cursor.execute(
                "SELECT user_id, name, email, age FROM user_data LIMIT %s OFFSET %s",
                (batch_size, offset)
            )
            rows = cursor.fetchall()
            # Convert tuples to dicts
            batch = [dict(zip(['user_id','name','email','age'], row)) for row in rows]
            yield batch

    except mysql.connector.Error as e:
        print(f"Database error: {e}")

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()


def batch_processing(batch_size):
    """
    Processes each batch from stream_users_in_batches,
    filtering users older than 25.
    """
    for batch in stream_users_in_batches(batch_size):
        filtered = [user for user in batch if user['age'] > 25]
        yield filtered  # Yield each filtered batch instead of returning immediately


__all__ = ['stream_users_in_batches', 'batch_processing']
