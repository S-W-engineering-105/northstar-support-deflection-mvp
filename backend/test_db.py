# backend/test_db.py
from db import get_order_status, check_stock

print("=== Testing order-status lookup ===")

# Test 1: valid order ID
result = get_order_status("NS-1001")
print(f"NS-1001 -> {result}")

# Test 2: invalid/non-existent order ID
result = get_order_status("NS-9999")
print(f"NS-9999 -> {result}")

print("\n=== Testing stock-availability lookup ===")

# Test 3: valid product + size
result = check_stock("Nike Air Force 1", "42")
print(f"Nike Air Force 1, size 42 -> {result}")

# Test 4: valid product, out-of-stock size
result = check_stock("Nike Air Force 1", "43")
print(f"Nike Air Force 1, size 43 -> {result}")

# Test 5: non-existent product
result = check_stock("Fake Shoe Brand", "42")
print(f"Fake Shoe Brand, size 42 -> {result}")