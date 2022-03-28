import sqlite3
import json

conexion = sqlite3.connect('database.db')
controlador = conexion.cursor()


def createDB():
    controlador.execute("DROP TABLE IF EXISTS usuarios")
    controlador.execute("DROP TABLE IF EXISTS fechas")
    controlador.execute("DROP TABLE IF EXISTS ips")
    controlador.execute("DROP TABLE IF EXISTS legal")

    controlador.execute("CREATE TABLE usuarios (id text, telefono text, contrasena text, provincia text, "
                      "permisos bool, emails_total integer, emails_phishing integer, emails_clicados integer, "
                      "constraint PK_usuarios primary key (id))")
    controlador.execute(
        "CREATE TABLE fechas (id text, fecha text, constraint PK_fechas primary key (id,fecha), "
        "constraint FK_fechas_usuarios foreign key (id) references usuarios(id))")
    controlador.execute(
        "CREATE TABLE ips (id text, ip text, constraint PK_ips primary key (id,ip), constraint "
        "FK_ips_usuarios foreign key (id) references usuarios(id))")


    controlador.execute("CREATE TABLE legal (url text, cookies integer, aviso integer, proteccion_de_datos integer,"
                      "creacion integer, constraint PK_webs primary key (url))")

    conexion.commit()


def rellenaTablasJson():
    createDB()

    with open("users.json", "r") as file:
        data = json.load(file)
        for usuario in data["usuarios"]:
            for id in usuario.keys():
                query = "INSERT INTO usuarios (id) VALUES (\'{}\')".format(id)
                controlador.execute(query)

                if usuario[id]["telefono"] != 'None':
                    query = "UPDATE usuarios SET telefono = {} WHERE id = \'{}\'".format(usuario[id]["telefono"], id)
                    controlador.execute(query)

                query = "UPDATE usuarios SET contrasena = \'{}\' WHERE id = \'{}\'".format(usuario[id]["contrasena"], id)
                controlador.execute(query)

                if usuario[id]["provincia"] != 'None':
                    query = "UPDATE usuarios SET provincia = \'{}\' WHERE id = \'{}\'".format(usuario[id]["provincia"], id)
                    controlador.execute(query)

                query = "UPDATE usuarios SET permisos = {} WHERE id = \'{}\'".format(usuario[id]["permisos"], id)
                controlador.execute(query)

                query = "UPDATE usuarios SET emails_total = {} WHERE id = \'{}\'".format(usuario[id]["emails"]["total"], id)
                controlador.execute(query)

                query = "UPDATE usuarios SET emails_phishing = {} WHERE id = \'{}\'".format(usuario[id]["emails"]["phishing"],id)
                controlador.execute(query)

                query = "UPDATE usuarios SET emails_clicados = {} WHERE id = \'{}\'".format(usuario[id]["emails"]["cliclados"],id)
                controlador.execute(query)

                arrayFechas = []
                for fecha in usuario[id]["fechas"]:
                    if fecha not in arrayFechas:
                        query = "INSERT INTO fechas (id,fecha) VALUES (\'{}\',\'{}\')".format(id, fecha)
                        controlador.execute(query)
                        arrayFechas.append(fecha)

                arrayIps = []
                if usuario[id]["ips"]== "None":
                    query = "INSERT INTO ips (id,ip) VALUES (\'{}\',None)".format(id,ip)
                else:
                    for ip in usuario[id]["ips"]:
                        if ip not in arrayIps:
                            query = "INSERT INTO ips (id,ip) VALUES (\'{}\',\'{}\')".format(id, ip)
                            controlador.execute(query)
                            arrayIps.append(ip)
    conexion.commit()

    with open("legal.json", "r") as file:
        data = json.load(file)

        for legal in data["legal"]:
            for url in legal.keys():
                cookies = legal[url]['cookies']
                aviso = legal[url]['aviso']
                proteccion_de_datos = legal[url]['proteccion_de_datos']
                creacion = legal[url]['creacion']
                query = "INSERT INTO legal VALUES (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')".format(url, cookies, aviso,proteccion_de_datos, creacion)
                controlador.execute(query)
    conexion.commit()


rellenaTablasJson()
conexion.close()
