# backend/test_chat.py
import requests

URL = "http://127.0.0.1:5000/chat"

def send(session_id, message):
    response = requests.post(URL, json={"session_id": session_id, "message": message})
    print(f"You: {message}")
    print(f"Bot: {response.json()['reply']}\n")

# --- Test 1: Order status, ID given right away ---
send("s1", "Where is order NS-1001?")

# --- Test 2: Order status, ID missing then provided ---
send("s2", "Where's my order?")
send("s2", "NS-1002")

# --- Test 3: Order that doesn't exist ---
send("s3", "Track order NS-9999")

# --- Test 4: Stock check, everything given at once ---
send("s4", "Do you have Nike Air Force 1 in size 42?")

# --- Test 5: Stock check, step by step ---
send("s5", "Is this available?")
send("s5", "Nike Air Force 1")
send("s5", "size 42")

# --- Test 6: Stock check, size not available (should suggest other sizes) ---
send("s6", "Do you have Nike Air Force 1 in size 39?")

# --- Test 7: Greeting ---
send("s7", "Hi")

# --- Test 8: Out of scope ---
send("s8", "Can I get a refund?")