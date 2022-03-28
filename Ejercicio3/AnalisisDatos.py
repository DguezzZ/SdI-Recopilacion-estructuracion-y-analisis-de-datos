import pandas as pd
import sqlite3
import numpy as np
import math

conexion = sqlite3.connect('database.db')
controlador = conexion.cursor()


def numCorreos(rango: int):
    if rango < 0:
        rango = -rango
        dataframe = pd.read_sql_query("SELECT * FROM usuarios WHERE emails_total >= \'{}\' group by id".format(rango),
                                      conexion)

        dataframe["IPs"] = pd.read_sql_query(
            "SELECT COUNT(ip) FROM ips INNER JOIN usuarios USING(id) WHERE emails_total ""< \'{}\' group by id".format(
                rango), conexion)

        dataframe["Fechas"] = pd.read_sql_query(
            "SELECT COUNT(fecha) FROM fechas INNER JOIN usuarios USING(id) WHERE ""emails_total < \'{}\' group by id".format(
                rango), conexion)

        return dataframe
    elif rango > 0:

        dataframe = pd.read_sql_query("SELECT * FROM usuarios WHERE emails_total >= \'{}\' group by id".format(rango),
                                      conexion)

        dataframe["IPs"] = pd.read_sql_query(
            "SELECT COUNT(ip) FROM ips INNER JOIN usuarios USING(id) WHERE emails_total "">= \'{}\' group by id".format(
                rango), conexion)

        dataframe["Fechas"] = pd.read_sql_query(
            "SELECT COUNT(fecha) FROM fechas INNER JOIN usuarios USING(id) WHERE ""emails_total >= \'{}\' group by id".format(
                rango), conexion)

        return dataframe
    else:
        return "hay algun errror"


def permisos(tipop: int):
    if tipop == 1 or tipop == 0:
        dataframe = pd.read_sql_query("SELECT * FROM usuarios WHERE permisos = \'{}\' group by id".format(tipop),
                                      conexion)

        dataframe["IPs"] = pd.read_sql_query(
            "SELECT COUNT(ip) FROM ips INNER JOIN usuarios USING(id) WHERE permisos ""= \'{}\' group by id".format(
                tipop), conexion)

        dataframe["Fechas"] = pd.read_sql_query(
            "SELECT COUNT(fecha) FROM fechas INNER JOIN usuarios USING(id) WHERE ""permisos = \'{}\' group by id".format(
                tipop), conexion)

        return dataframe
    else:
        return "hay algun error"


def observaciones(dataframe):
    return dataframe["emails_phising"].sum()


def missing(dataframe):
    cont = 0
    for index, row in dataframe.iterrows():
        if row["email_phising"] is None or math.isnan(row["emails_phising"]):
            cont = cont + 1
    return cont


def mediana(dataframe):
    return np.median(dataframe["emails_phising"].to_numpy())


def media(dataframe) -> float:
    return dataframe["emails_phising"].sum / len(dataframe)


def varianza(dataframe):
    return np.var(dataframe["emails_phishing"].to_numpy())


def max(dataframe) -> int:
    return dataframe["emails_phishing"].max()


def min(dataframe) -> int:
    return dataframe["emails_phishing"].min()


dataframe_admins = permisos(1)
dataframe_users = permisos(0)

dataframe_masCorreo = numCorreos(200)
dataframe_menosCorreo = numCorreos(-200)

print()
print("----------------------------------------------------------------")
print()

print("Agrupacíon POR PERMISOS: ")
print("#################### Para ADMINS ####################")
print("Observaciones Admins", observaciones(dataframe_admins))
print("Valores ausentes Admins: ", missing(dataframe_admins))
print("Media Admins: ", media(dataframe_admins))
print("Mediana Admins: ", mediana(dataframe_admins))
print("Varianza Admins: ", varianza(dataframe_admins))
print("Máximo Admins: ", max(dataframe_admins))
print("Minimo Admins: ", max(dataframe_admins))

print("#################### Para USERS ####################")
print("Observaciones Users", observaciones(dataframe_users))
print("Valores ausentes en Users: ", missing(dataframe_users))
print("Media Users: ", media(dataframe_users))
print("Mediana Users: ", mediana(dataframe_users))
print("Varianza Users: ", varianza(dataframe_users))
print("Máximo Users: ", max(dataframe_users))
print("Minimo Users: ", max(dataframe_users))

print()
print("----------------------------------------------------------------")
print()

print("Agrupacíon POR NUMERO DE EMAILS: ")
print("#################### +200 correos ####################")
print("Observaciones Admins", observaciones(dataframe_masCorreo))
print("Valores ausentes Admins: ", missing(dataframe_masCorreo))
print("Media Admins: ", media(dataframe_masCorreo))
print("Mediana Admins: ", mediana(dataframe_masCorreo))
print("Varianza Admins: ", varianza(dataframe_masCorreo))
print("Máximo Admins: ", max(dataframe_masCorreo))
print("Minimo Admins: ", max(dataframe_masCorreo))

print("#################### -200 correos ####################")
print("Observaciones Users", observaciones(dataframe_menosCorreo))
print("Valores ausentes en Users: ", missing(dataframe_menosCorreo))
print("Media Users: ", media(dataframe_menosCorreo))
print("Mediana Users: ", mediana(dataframe_menosCorreo))
print("Varianza Users: ", varianza(dataframe_menosCorreo))
print("Máximo Users: ", max(dataframe_menosCorreo))
print("Minimo Users: ", max(dataframe_menosCorreo))
