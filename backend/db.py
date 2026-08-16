# backend/db.py
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()  # loads credentials from .env file, never hard-coded

def get_connection():
    """Creates a database connection using credentials from .env"""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "northstar_chatbot"),
        use_pure=True
    )


def get_order_status(order_id):
    """
    Looks up an order by ID.
    Returns a dict with order info, or None if not found.
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        # Parameterized query — prevents SQL injection
        cursor.execute(
            "SELECT order_id, status, expected_delivery_date FROM orders WHERE order_id = %s",
            (order_id,)
        )
        result = cursor.fetchone()
        return result
    except Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def check_stock(product_name, size):
    """
    Looks up stock for a product + size combination.
    Returns a dict with quantity info, or None if not found.
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT product_name, size, quantity_available FROM inventory WHERE product_name = %s AND size = %s",
            (product_name, size)
        )
        result = cursor.fetchone()
        return result
    except Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()




def product_exists(product_name):
    """Checks if a product name exists at all in inventory (any size)."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT DISTINCT product_name FROM inventory WHERE product_name = %s LIMIT 1",
            (product_name,)
        )
        result = cursor.fetchone()
        return result is not None
    except Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def get_available_sizes(product_name):
    """Returns a list of sizes currently in stock (qty > 0) for a product."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT size FROM inventory WHERE product_name = %s AND quantity_available > 0",
            (product_name,)
        )
        results = cursor.fetchall()
        return [row["size"] for row in results]
    except Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def log_conversation(session_id, intent, query_type, was_successful):
    """
    Logs a chatbot interaction for audit/analytics purposes.
    Does NOT store the actual message text — only category-level info.
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO conversation_log (session_id, intent, query_type, was_successful) "
            "VALUES (%s, %s, %s, %s)",
            (session_id, intent, query_type, was_successful)
        )
        conn.commit()
    except Error as e:
        print(f"Database error while logging conversation: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()