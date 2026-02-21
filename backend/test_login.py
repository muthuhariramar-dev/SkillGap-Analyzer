import requests
import json

# Test the login endpoint
url = "http://localhost:8000/login"

# Test credentials
test_cases = [
    {
        "email": "samykmottaya@gmail.com",
        "password": "Danger!123",
        "expected": "success"
    },
    {
        "email": "abs@gmail.com",
        "password": "Danger!123",
        "expected": "success"
    },
    {
        "email": "test@example.com",
        "password": "password123",
        "expected": "success"
    },
    {
        "email": "samykmottaya@gmail.com",
        "password": "WrongPassword",
        "expected": "failure"
    }
]

print("Testing Login Endpoint\n")
print("=" * 60)

for i, test in enumerate(test_cases, 1):
    print(f"\nTest {i}: {test['email']}")
    print(f"Password: {test['password']}")
    print(f"Expected: {test['expected']}")
    print("-" * 60)
    
    try:
        response = requests.post(
            url,
            json={"email": test["email"], "password": test["password"]},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if test["expected"] == "success" and response.status_code == 200:
            print("✓ Test PASSED")
        elif test["expected"] == "failure" and response.status_code == 401:
            print("✓ Test PASSED")
        else:
            print("✗ Test FAILED")
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")

print("\n" + "=" * 60)
print("Testing Complete!")
