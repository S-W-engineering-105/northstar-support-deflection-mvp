# backend/app.py (routing logic, simplified)
from flask import Flask, request, jsonify
from db import get_order_status, check_stock

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")

    # Very basic intent routing (Task 12) — improve later with better matching
    if "order" in user_message.lower() or "ship" in user_message.lower():
        # extract order_id from message — placeholder logic, refine as needed
        order_id = extract_order_id(user_message)
        if not order_id:
            return jsonify({"reply": "Sure. Please provide your order number."})
        
        order = get_order_status(order_id)
        if order:
            return jsonify({
                "reply": f"Order {order['order_id']} is currently {order['status']}. "
                         f"Expected delivery: {order['expected_delivery_date']}."
            })
        else:
            return jsonify({"reply": "I couldn't find an order with that number. Please check the order ID and try again."})

    elif "stock" in user_message.lower() or "size" in user_message.lower() or "available" in user_message.lower():
        product_name, size = extract_product_and_size(user_message)  # placeholder
        item = check_stock(product_name, size)
        if item:
            if item["quantity_available"] > 0:
                return jsonify({
                    "reply": f"Yes. {item['product_name']}, size {item['size']} is currently in stock. "
                             f"We have {item['quantity_available']} units available."
                })
            else:
                return jsonify({"reply": f"{item['product_name']}, size {item['size']} is currently out of stock."})
        else:
            return jsonify({"reply": "I couldn't find that product. Please check the product name and try again."})

    else:
        return jsonify({"reply": "I'm currently able to help with order status and product availability."})