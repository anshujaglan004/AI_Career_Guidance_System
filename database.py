import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config


def get_connection():
    """
    Create and return a MySQL database connection.
    """

    return mysql.connector.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME
    )


def register_user(full_name, email, password):
    """
    Register a new user.
    """

    try:
        connection = get_connection()
        cursor = connection.cursor()

        hashed_password = generate_password_hash(password)

        query = """
        INSERT INTO users(full_name, email, password)
        VALUES (%s, %s, %s)
        """

        cursor.execute(
            query,
            (full_name, email, hashed_password)
        )

        connection.commit()

        return True

    except mysql.connector.Error as err:
        print("Database Error:", err)
        return False

    finally:
        if 'cursor' in locals():
            cursor.close()

        if 'connection' in locals() and connection.is_connected():
            connection.close()


def get_user_by_email(email):
    """
    Find a user by email.
    """

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT * FROM users
        WHERE email = %s
        """

        cursor.execute(query, (email,))

        return cursor.fetchone()

    except mysql.connector.Error as err:
        print("Database Error:", err)
        return None

    finally:
        if 'cursor' in locals():
            cursor.close()

        if 'connection' in locals() and connection.is_connected():
            connection.close()


def login_user(email, password):
    """
    Verify login credentials.
    """

    user = get_user_by_email(email)

    if user and check_password_hash(user["password"], password):
        return user

    return None