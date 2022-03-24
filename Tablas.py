import json

with open('users.json') as file:
    data = json.load(file)

    for user in data['usuarios']:
        print('cliente1' + user['sergio.garcia'])