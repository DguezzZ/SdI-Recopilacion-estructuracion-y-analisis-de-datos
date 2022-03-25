import json
import pandas as panda
import sqlite3


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


    def creacionBD():
        conexion = sqlite3.connect("basededatos.db")
        print("Base de datos abierta con exito")
        conexion.execute('''CREATE TABLE usuarios
                    (ID INT PRIMARY KEY NOT NULL,
                    NOMBRE      TEXT    NOT NULL,
                    TLFN        TEXT    NOT NULL,
                    CONTRA      TEXT    NOT NULL,
                    PROV        TEXT    NOT NULL,
                    PERMISOS    TEXT    NOT NULL,
                    FECHA       TEXT    NOT NULL,
                    IPS         TEXT    NOT NULL);''')

        for info in data['usuarios']:
            sql = "INSERT INTO usuarios(ID,NOMBRE,TLFN,CONTRA,PROV,PERMISOS,FECHA,IPS) VALUES('%s',%d,%d,%d,%d,%d,%d,%d)" % (
            info['ID'], info['NOMBRE'], info['TLFN'], info['CONTRA'], info['PROV'], info['PERMISOS'],
            info['FECHA'], info['IPS'])

            conexion.execute(sql)
            conexion.commit()

        cursor = conexion.execute("select id,nombre,tlfn,contra,prov,permisos,fecha,ips from usuarios")
        for row in cursor:
            print('ID= ', row[0], 'Name= ', row[1], 'Telefono= ', row[2], 'Contraseña= ', row[3], 'Provincia= ', row[4], 'Permisos= ', row[5], 'Fecha= ', row[6], 'IPS= ', row[7])

        print("operacion terminada")
        conexion.close()