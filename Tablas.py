import json
import numpy as numpy
import panda as panda


with open('users.json') as file:
def parseUsersInfo():

    data = json.load(file)
    list_users = []
    for user in data['usuarios']:
        nombre_user = list(user.keys())[0]
        info_user = user[nombre_user]
        del info_user["fechas"]
        del info_user["ips"]
        info_user['username'] = nombre_user
        list_users.append(info_user)
    return panda.json_normalize(list_users)