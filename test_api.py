import requests
import json

# Base URL
BASE_URL = "http://localhost:8001"

print("=" * 60)
print("Testing MLOps API")
print("=" * 60)

# Test 1: Health check
print("\n1. Health Check Endpoint (/health)")
print("-" * 60)
try:
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

# Test 2: Root endpoint
print("\n2. Root Endpoint (/)")
print("-" * 60)
try:
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

# Test 3: Prediction with sample data
print("\n3. Prediction Endpoint (/predict)")
print("-" * 60)
try:
    payload = {
        "feature1": 0.496714,
        "feature2": 1.399355,
        "feature3": -0.675178,
        "feature4": -1.907808
    }
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    print(f"Input: {json.dumps(payload, indent=2)}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

# Test 4: Another prediction
print("\n4. Another Prediction Example")
print("-" * 60)
try:
    payload = {
        "feature1": 0.5,
        "feature2": 1.4,
        "feature3": -0.5,
        "feature4": -1.9
    }
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    print(f"Input: {json.dumps(payload, indent=2)}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 60)
print("Testing completed!")
print("=" * 60)
