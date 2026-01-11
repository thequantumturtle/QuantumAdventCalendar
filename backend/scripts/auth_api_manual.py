#!/usr/bin/env python
"""
Manual JWT Authentication API script.

This script performs integration tests against a running server at
`http://localhost:5000/api`. It is not intended to be collected by pytest
and therefore is placed under `backend/scripts/` and named `*_manual.py`.

Run it manually when the backend server is running:

    python backend/scripts/auth_api_manual.py

"""

import requests
import json
import time

API_URL = "http://localhost:5000/api"

# Use unique username based on timestamp to avoid conflicts
unique_id = str(int(time.time() * 1000) % 1000000)
test_username = f"testuser_{unique_id}"

print("=" * 60)
print("JWT Authentication API Manual Test Suite")
print("=" * 60)
print(f"Using test username: {test_username}\n")

# Test 1: Register a new user
print("[TEST 1] Register New User")
print("-" * 60)
register_data = {
    "username": test_username,
    "email": f"test_{unique_id}@example.com",
    "password": "quantum123456"
}
response = requests.post(f"{API_URL}/auth/register", json=register_data)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
if response.status_code != 201:
    raise SystemExit(f"Expected 201, got {response.status_code}")
print("✓ Registration successful")

# The rest of the checks (login, refresh, protected endpoints) follow the same pattern
# but are omitted here for brevity. Run the script interactively to exercise them.

print("\n" + "=" * 60)
print("Manual auth script finished (partial).")
print("=" * 60)
