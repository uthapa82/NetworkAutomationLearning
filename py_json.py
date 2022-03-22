# JSON is commonly used with data APIS. Here how we can parse  JSON into a Python Dictionary 

import json

#sample json
userJson = '{"first_name": "John", "last_name": "Doe", "Age":30}'

#parse to dict 
user = json.loads(userJson)

print(user)
print(user['first_name'])

#change dict to JSON format 
car = {'make' :'Toyota', 'model': 'Sienna', 'year': 2017}

carJSON = json.dumps(car)
print(carJSON)