import requests
import json

URL="http://127.0.0.1:8000/student/"

myData={
    'name':'John Doe',
    'roll':123, 
    'city':'New York'
}

json_data=json.dumps(myData)

r=requests.post(url=URL, json=myData) # you can use data=json_data as well 
#instead of json=myData but that will not set the header to json/application

data=r.json()
print(data)

