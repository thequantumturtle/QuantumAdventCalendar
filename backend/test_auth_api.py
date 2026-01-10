#!/usr/bin/env python
"""
Test JWT Authentication API Endpoints
"""

import requests
import json
import time

API_URL = "http://localhost:5000/api"

# Use unique username based on timestamp to avoid conflicts
unique_id = str(int(time.time() * 1000) % 1000000)
test_username = f"testuser_{unique_id}"

print("=" * 60)
print("JWT Authentication API Test Suite")
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
assert response.status_code == 201, f"Expected 201, got {response.status_code}"
print("✓ Registration successful")

# Test 2: Try to register duplicate user (should fail)
print("\n[TEST 2] Register Duplicate User (should fail)")
print("-" * 60)
response = requests.post(f"{API_URL}/auth/register", json=register_data)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
assert response.status_code == 409, f"Expected 409, got {response.status_code}"
print("✓ Duplicate user correctly rejected")

# Test 3: Login with correct credentials
print("\n[TEST 3] Login with Correct Credentials")
print("-" * 60)
login_data = {
    "username": test_username,
    "password": "quantum123456"
}
response = requests.post(f"{API_URL}/auth/login", json=login_data)
print(f"Status: {response.status_code}")
login_response = response.json()
access_token = login_response.get("access_token")
refresh_token = login_response.get("refresh_token")
print(f"Access Token: {access_token[:20]}...")
print(f"Refresh Token: {refresh_token[:20]}...")
assert response.status_code == 200, f"Expected 200, got {response.status_code}"
print("✓ Login successful")

# Test 4: Get current user info with valid token
print("\n[TEST 4] Get Current User (with valid token)")
print("-" * 60)
headers = {"Authorization": f"Bearer {access_token}"}
response = requests.get(f"{API_URL}/auth/me", headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
assert response.status_code == 200, f"Expected 200, got {response.status_code}"
print("✓ User info retrieved successfully")

# Test 5: Try to access protected endpoint without token (should fail)
print("\n[TEST 5] Access Protected Endpoint Without Token (should fail)")
print("-" * 60)
response = requests.get(f"{API_URL}/auth/me")
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
assert response.status_code == 401, f"Expected 401, got {response.status_code}"
print("✓ Correctly blocked unauthorized access")

# Test 6: Refresh token to get new access token
print("\n[TEST 6] Refresh Access Token")
print("-" * 60)
refresh_headers = {"Authorization": f"Bearer {refresh_token}"}
response = requests.post(f"{API_URL}/auth/refresh", headers=refresh_headers)
print(f"Status: {response.status_code}")
new_access_token = response.json().get("access_token")
print(f"New Access Token: {new_access_token[:20]}...")
assert response.status_code == 200, f"Expected 200, got {response.status_code}"
print("✓ Token refresh successful")

# Test 7: Use new access token
print("\n[TEST 7] Use New Access Token")
print("-" * 60)
new_headers = {"Authorization": f"Bearer {new_access_token}"}
response = requests.get(f"{API_URL}/auth/me", headers=new_headers)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
assert response.status_code == 200, f"Expected 200, got {response.status_code}"
print("✓ New access token works")

# Test 8: Login with wrong password (should fail)
print("\n[TEST 8] Login with Wrong Password (should fail)")
print("-" * 60)
wrong_login = {
    "username": test_username,
    "password": "wrongpassword"
}
response = requests.post(f"{API_URL}/auth/login", json=wrong_login)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
assert response.status_code == 401, f"Expected 401, got {response.status_code}"
print("✓ Wrong password correctly rejected")

# Test 9: Submit code to challenge (should require JWT)
print("\n[TEST 9] Submit Code to Challenge (requires JWT)")
print("-" * 60)
submission_data = {
    "day": 1,
    "code": """from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

def create_hadamard_circuit():
    q = QuantumRegister(1, 'q')
    c = ClassicalRegister(1, 'c')
    circuit = QuantumCircuit(q, c)
    circuit.h(q[0])
    circuit.measure(q[0], c[0])
    return circuit

def run_circuit():
    qc = create_hadamard_circuit()
    simulator = AerSimulator()
    result = simulator.run(qc, shots=1000).result()
    counts = result.get_counts(qc)
    return counts
"""
}

# Try without token (should fail)
print("  a) Without token (should fail):")
response = requests.post(f"{API_URL}/submissions/", json=submission_data)
print(f"     Status: {response.status_code}")
assert response.status_code == 401, f"Expected 401, got {response.status_code}"
print("     ✓ Correctly blocked without token")

# Try with token (should succeed)
print("  b) With token (should succeed):")
headers = {"Authorization": f"Bearer {access_token}"}
response = requests.post(f"{API_URL}/submissions/", json=submission_data, headers=headers)
print(f"     Status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print(f"     Passed: {result.get('passed')}")
    print("     ✓ Submission accepted")
else:
    print(f"     Error: {response.json()}")

print("\n" + "=" * 60)
print("✓ ALL TESTS PASSED!")
print("=" * 60)
