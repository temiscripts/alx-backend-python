#!/usr/bin/python3
seed = __import__('seed')

def paginate_users(page_size, offset):
    """
    Fetches a page of users from the user_data table.
    Returns a list of dictionaries.
    """
    conn = seed.connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (page_size, offset))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def lazy_paginate(page_size):
    """
    Generator that lazily fetches pages of user_data.
    Fetches the next page only when needed.
    """
    # Get total number of rows
    conn = seed.connect_to_prodev()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM user_data")
    total_rows = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    offset = 0
    # Single loop to yield pages one by one
    while offset < total_rows:
        yield paginate_users(page_size, offset)
        offset += page_size

__all__ = ['paginate_users', 'lazy_paginate']
