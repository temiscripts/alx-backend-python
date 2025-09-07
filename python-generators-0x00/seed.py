import os
import uuid
import mysql.connector

def connect_db():
    """Connect to MySQL server"""
    try:
        mydb = mysql.connector.connect(
            host=os.environ.get("MY_DB_HOST", "localhost"),
            user=os.environ.get("MY_DB_USER", "root"),
            password=os.environ.get("MY_DB_PASSWORD", "")
        )
        return mydb
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL server: {err}")
        return None

def create_database(connection):
    """Create ALX_prodev database if it doesn't exist"""
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    connection.commit()
    cursor.close()

def connect_to_prodev():
    """Connect to ALX_prodev database"""
    try:
        mydb = mysql.connector.connect(
            host=os.environ.get("MY_DB_HOST", "localhost"),
            user=os.environ.get("MY_DB_USER", "root"),
            password=os.environ.get("MY_DB_PASSWORD", ""),
            database="ALX_prodev"
        )
        return mydb
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None

def create_table(connection):
    """Create user_data table"""
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL
        )
    """)
    connection.commit()
    cursor.close()

def insert_data(connection, csv_file):
    """Insert data from CSV into table"""
    cursor = connection.cursor()
    sql = "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)"
    try:
        with open(csv_file, 'r') as file:
            next(file)  # Skip header
            for line in file:
                name, email, age = line.strip().split(',')
                uid = str(uuid.uuid4())
                cursor.execute(sql, (uid, name, email, age))
        connection.commit()
    except FileNotFoundError:
        print(f"Error: {csv_file} not found.")
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()
