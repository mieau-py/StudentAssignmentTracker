
import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "",
    "database": "student_assignment_db",
}


def get_connection():
    """Connect to the student assignment database."""
    return mysql.connector.connect(**DB_CONFIG)


def test_connection():
    """Test the MySQL connection."""
    connection = None

    try:
        connection = get_connection()

        if connection.is_connected():
            print("Connected to MySQL successfully!")
            return True

    except Error as error:
        print(f"Could not connect to MySQL: {error}")
        print("Check that MySQL is running and schema.sql has been imported.")
        return False

    finally:
        if connection is not None and connection.is_connected():
            connection.close()
