import json

with open('verified.json') as json_data:
    d = json.load(json_data)
    for item in d:
        my_id = item[0]
        my_desc = item[1]
        print(my_id, my_desc)
