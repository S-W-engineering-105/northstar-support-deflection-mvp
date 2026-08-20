"""
Inventory endpoint for Northstar Support Deflection MVP.

Deliverable: GET /inventory/<product_id>

ASSUMPTIONS (update once you confirm docs/db-schema.sql):
  Table:  inventory
  Columns:
    product_id    VARCHAR / INT   - primary key, matches what the chatbot passes in
    product_name  VARCHAR         - human-readable name, e.g. "Nike Air Force 1"
    size          VARCHAR/NULL    - product variant, e.g. "42" (nullable for non-sized items)
    quantity      INT             - units currently in stock
    updated_at    DATETIME        - last sync timestamp

If your actual table/columns differ, only the SQL query and the response
mapping below need to change — the route logic stays the same.
"""

from flask import Blueprint, jsonify
import mysql.connector
from mysql.connector import Error
import os

inventory_bp = Blueprint("inventory", __name__)


def get_db_connection():
    """Opens a new DB connection using the same env vars as the rest of the app."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "northstar_chatbot"),
    )


@inventory_bp.route("/inventory/<product_id>", methods=["GET"])
def get_inventory(product_id):
    """
    Returns stock info for a single product.

    Success (200):
      {
        "product_id": "NS-1001",
        "product_name": "Nike Air Force 1",
        "size": "42",
        "quantity": 6,
        "available": true,
        "updated_at": "2026-08-19T14:32:00"
      }

    Not found (404):
      { "error": "Product not found", "product_id": "NS-1001" }

    Server/DB error (500):
      { "error": "Could not retrieve inventory data" }
    """
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT product_id, product_name, size, quantity, updated_at
            FROM inventory
            WHERE product_id = %s
        """
        cursor.execute(query, (product_id,))
        row = cursor.fetchone()

        if row is None:
            return jsonify({
                "error": "Product not found",
                "product_id": product_id
            }), 404

        response = {
            "product_id": row["product_id"],
            "product_name": row["product_name"],
            "size": row["size"],
            "quantity": row["quantity"],
            "available": row["quantity"] > 0,
            "updated_at": row["updated_at"].isoformat() if row["updated_at"] else None,
        }
        return jsonify(response), 200

    except Error as e:
        print(f"[inventory] DB error: {e}")
        return jsonify({"error": "Could not retrieve inventory data"}), 500

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
