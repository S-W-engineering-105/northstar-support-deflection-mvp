# backend/app.py
from flask import Flask, request, jsonify, render_template
from db import get_order_status, check_stock, product_exists, get_available_sizes, log_conversation
import re

app = Flask(__name__)

SESSIONS = {}

KNOWN_PRODUCTS = [
    "Nike Air Force 1", "Adidas Ultraboost", "Puma RS-X",
    "New Balance 550", "Converse Chuck Taylor", "Vans Old Skool"
]


@app.route("/")
def index():
    return render_template("index.html")


def detect_intent(message):
    msg = message.lower()
    if any(word in msg for word in ["order", "ship", "track", "delivery", "arrive"]):
        return "order_status"
    if any(word in msg for word in ["stock", "size", "available", "have"]):
        return "stock_availability"
    if msg.strip() in ["hi", "hello", "hey"]:
        return "greeting"
    if msg.strip() in ["bye", "thanks", "thank you", "that's all"]:
        return "goodbye"
    return "fallback"


def extract_order_id(message):
    match = re.search(r"NS-\d{4}", message.upper())
    return match.group(0) if match else None


def normalize_order_id(message):
    """
    Used only when we already know we're expecting an order number
    (i.e., inside the awaiting_order_id state).
    Accepts: 'NS-1001', 'ns1001', '1001', '1'
    """
    digits = re.sub(r"\D", "", message)
    if not digits:
        return None
    padded = digits.zfill(4)
    return f"NS-{padded}"


def extract_size(message):
    match = re.search(r"\bsize\s*(\d{1,2})\b", message.lower())
    if match:
        return match.group(1)
    match = re.search(r"\b(\d{2})\b", message)
    return match.group(1) if match else None


def extract_product_name(message):
    for product in KNOWN_PRODUCTS:
        if product.lower() in message.lower():
            return product
    return None


def handle_order_lookup(order_id):
    order = get_order_status(order_id)
    if order:
        return (f"Order {order['order_id']} is currently {order['status']}. "
                f"Expected delivery: {order['expected_delivery_date']}.")
    return "I couldn't find an order with that number. Please check the order number again and try again."


def handle_stock_lookup(product, size):
    item = check_stock(product, size)
    if item:
        if item["quantity_available"] > 0:
            return (f"Yes, {item['product_name']} in size {item['size']} is available. "
                    f"Quantity available: {item['quantity_available']}.")
        else:
            return f"Sorry, {product} in size {size} is currently out of stock."
    else:
        if product_exists(product):
            other_sizes = get_available_sizes(product)
            if other_sizes:
                sizes_list = ", ".join(other_sizes)
                return f"We don't have that size available. Available sizes are: {sizes_list}."
            else:
                return f"We don't have that size available, and no other sizes are currently in stock for {product}."
        else:
            return "We could not find that product, please check the name and try again."


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    session_id = data.get("session_id", "default")
    message = data.get("message", "")

    session = SESSIONS.get(session_id, {"state": None, "product": None})

    # ---------- Continue: awaiting order number ----------
    if session["state"] == "awaiting_order_id":
        order_id = extract_order_id(message) or normalize_order_id(message)
        SESSIONS[session_id] = {"state": None, "product": None}
        if not order_id:
            log_conversation(session_id, "order_status", "order_status", False)
            return jsonify({"reply": "I couldn't recognize that as an order number. Please try again, e.g. NS-1001."})
        order = get_order_status(order_id)
        log_conversation(session_id, "order_status", "order_status", order is not None)
        return jsonify({"reply": handle_order_lookup(order_id)})

    # ---------- Continue: awaiting product name ----------
    if session["state"] == "awaiting_product":
        product = extract_product_name(message)
        if not product:
            log_conversation(session_id, "stock_availability", "stock_availability", False)
            return jsonify({"reply": "We could not find that product, please check the name and try again."})
        session["product"] = product
        session["state"] = "awaiting_size"
        SESSIONS[session_id] = session
        return jsonify({"reply": "What size are you looking for?"})

    # ---------- Continue: awaiting size ----------
    if session["state"] == "awaiting_size":
        size = extract_size(message) or message.strip()
        product = session["product"]
        SESSIONS[session_id] = {"state": None, "product": None}
        item = check_stock(product, size)
        log_conversation(session_id, "stock_availability", "stock_availability", item is not None)
        return jsonify({"reply": handle_stock_lookup(product, size)})

    # ---------- Fresh message: detect intent ----------
    intent = detect_intent(message)

    if intent == "order_status":
        order_id = extract_order_id(message)
        if order_id:
            order = get_order_status(order_id)
            log_conversation(session_id, "order_status", "order_status", order is not None)
            return jsonify({"reply": handle_order_lookup(order_id)})
        else:
            session["state"] = "awaiting_order_id"
            SESSIONS[session_id] = session
            return jsonify({"reply": "Please provide your order number."})

    elif intent == "stock_availability":
        product = extract_product_name(message)
        size = extract_size(message)
        if product and size:
            item = check_stock(product, size)
            log_conversation(session_id, "stock_availability", "stock_availability", item is not None)
            return jsonify({"reply": handle_stock_lookup(product, size)})
        elif product:
            session["state"] = "awaiting_size"
            session["product"] = product
            SESSIONS[session_id] = session
            return jsonify({"reply": "What size are you looking for?"})
        else:
            session["state"] = "awaiting_product"
            SESSIONS[session_id] = session
            return jsonify({"reply": "What product are you looking for?"})

    elif intent == "greeting":
        log_conversation(session_id, "greeting", "greeting", True)
        return jsonify({"reply": "Hi! I'm Northstar's support assistant. I can help you check your order status or product availability. How can I help?"})

    elif intent == "goodbye":
        log_conversation(session_id, "goodbye", "goodbye", True)
        return jsonify({"reply": "You're welcome! Have a great day."})

    else:
        log_conversation(session_id, "fallback", "fallback", False)
        return jsonify({"reply": "I'm currently able to help with order status and stock availability. What would you like to check?"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)