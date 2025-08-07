import requests
import json

URL = "http://127.0.0.1:8000/Employees/5/"

myData = {
    'id':5, 
    'name': 'John Doe update3',
    'age': 30,
    'salary': 50000
}

r = requests.delete(url=URL)


# Print raw response to debug
print("Status Code:", r.status_code)
print("Raw Response Text:", r.text)

# Then try parsing if it's not empty
if r.text.strip():  # check if response body is not empty
    data = json.loads(r.text)
    print("Parsed JSON:", data)
else:
    print("Empty or non-JSON response")
