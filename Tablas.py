import json
import numpy as numpy
import pandas as pd
import sqlite3
import dataclasses

with open('users.json') as file:
    data = json.load(file)

    def parseUsersInfo():
        list_users = []
        for user in data['usuarios']:
            nombre_user = list(user.keys())[0]
            info_user = user[nombre_user]
            del info_user["fechas"]
            del info_user["ips"]
            info_user['username'] = nombre_user
            list_users.append(info_user)
        return pd.json_normalize(list_users)


    def creacionBD():
        conexion = sqlite3.connect("basededatos.db")
        print("Base de datos abierta con exito")
        try:
            conexion.execute('''CREATE TABLE usuarios
                        (telefono       TEXT    NOT NULL,
                        contrasena      TEXT    NOT NULL,
                        provincia       TEXT    NOT NULL,
                        permisos        TEXT    NOT NULL,
                        fechas          TEXT    NOT NULL,
                        ips             TEXT    NOT NULL);''')
            print("Tabla creada")
        except sqlite3.OperationalError:
            print("Tabla ya existente")
        conexion.close()
        for info in data['usuarios']:
            sql = "INSERT INTO usuarios(telefono,contrasena,provincia,permisos,fechas,ips) VALUES('%s','%s','%s','%s','%s','%s')" % (
                info['telefono'], info['contrasena'], info['provincia'], info['permisos'],
                info['fechas'], info['IPS'])

            conexion.execute(sql)
            conexion.commit()

        cursor = conexion.execute("select nombre,telefono,contrasena,provincia,permisos,fecha,ips from usuarios")
        for row in cursor:
            print(row)

        print("operacion terminada")
        conexion.close()

if __name__ == '__main__':
    parseUsersInfo()
    creacionBD()
