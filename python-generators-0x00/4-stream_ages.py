#!/usr/bin/python3
seed = __import__('seed')

def stream_user_ages():
    """
    Generator that yields ages of users one by one.
    """
    conn = seed.connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    
    for row in cursor:
        yield row['age']  # Yield age directly
    
    cursor.close()
    conn.close()


def calculate_average_age():
    """
    Calculates the average age using the generator without loading all data at once.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():  # Loop 1
        total_age += age
        count += 1

    if count == 0:
        return 0
    return total_age // count


if __name__ == '__main__':
    avg_age = calculate_average_age()  # Loop 2 is optional if we used another iteration inside main
    print(f"Average age of users: {avg_age}")
