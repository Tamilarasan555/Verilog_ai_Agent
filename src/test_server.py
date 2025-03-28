import requests

try:
    response = requests.post('http://localhost:9000/analyze', json={'description': 'test'})
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except requests.exceptions.ConnectionError:
    print("Error: Could not connect to the server. Make sure it's running on port 9000.")
except Exception as e:
    print(f"Error: {str(e)}") 