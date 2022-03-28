import pandas as pd
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import hashlib
from urllib.request import urlopen

conexion = sqlite3.connect('database.db')
controlador = conexion.cursor()


def contPeligro(AuxDataframe):
    for i, colm in AuxDataframe.iterrows():
        if colm['emails_phishing'] != 0:
            AuxDataframe._set_value(i, "cont_clickados", colm['emails_ciclados'] / colm['emails_phishing'])
        else:
            AuxDataframe._set_value(i, "cont_clickados", 0)
    AuxDataframe.sort_values("cont_clickados", ascending=False)
    return AuxDataframe

def checkSecurity(password):
    if password >= 5:
        esSegura = analyzeString(password)
    else:
        esSegura= False
    return esSegura

def analyzeString(password):
    for i in password:
        if password.isdigit():
            num= True
        elif password.isalpha():
            char= True
    return num and char


def usuariosCriticos():
    dataframe = pd.read_sql_query("SELECT id, emails_clicados, contrasena,emails_phising FROM usuarios ORDER BY emails_clicados DESC",conexion)
    dataframe2 = dataframe[checkSecurity(dataframe["contrasena"])]
    dataframe3 = contPeligro(dataframe)
    finalDataframe= pd.merge(dataframe2,dataframe3)
    finalDataframe.sort_values(['critico', "cont_clickados"], ascending=[False, False])
    imprimeGraficoUsuariosCriticos(finalDataframe)



def imprimeGraficoUsuariosCriticos(Dataframe):
    Dataframe.plot(x='id', y='emails_phishing', kind='bar', figsize=(10, 10))
    plt.show()


def politicasDesactualizadas():
    dataframe = pd.read_sql_query("SELECT url, cookies, aviso, proteccion_de_datos FROM webs ORDER BY url", conexion)
    dataframe["Politicas"] = dataframe["cookies"] + dataframe["aviso"] + dataframe["proteccion_de_datos"]
    dataframe = dataframe[dataframe["Politicas"] == 1]
    dataframe = dataframe.sort_values("url").head(5)
    return dataframe

def imprimeGraficoPaginasDesactualizadas(Dataframe):
    Dataframe.plot(x='url', y='Politicas', kind='bar', figsize=(10, 10))
    plt.ylim()
    plt.show()

# Este codigo no nos funciona correctamente y me estoy volviendo loco intentando resolverlo
# def mediaConexionesVulnerables(condicion: bool):
#     if condicion:
#         dataframe = pd.read_sql_query("SELECT id, contrasena FROM usuarios",conexion)
#         dataframe["IPs"] = pd.read_sql_query("SELECT COUNT(ip) FROM ips group by id", conexion)
#         pd.read_sql_query("SELECT id, emails_clicados, contrasena,emails_phising FROM usuarios ORDER BY emails_clicados DESC",conexion)
#         dataframe2 = dataframe[checkSecurity(dataframe["contrasena"])]
#         dataframe3 = contPeligro(dataframe)
#         finalDataframe = pd.merge(dataframe2, dataframe3)
#         dataframeFinal=pd.merge(finalDataframe,dataframe)
#         return dataframeFinal["IPs"].sum() / len(dataframe)
#     else:
#         dataframe = pd.read_sql_query("SELECT id, contrasena FROM usuarios",conexion)
#         dataframe["IPs"] = pd.read_sql_query("SELECT COUNT(ip) FROM ips group by id", conexion)
#         pd.read_sql_query("SELECT id, emails_clicados, contrasena,emails_phising FROM usuarios ORDER BY emails_clicados DESC",conexion)
#         dataframe2 = dataframe[checkSecurity(dataframe["contrasena"])]
#         dataframe3 = contPeligro(dataframe)
#         finalDataframe = pd.merge(dataframe2, dataframe3)
#         dataframeFinal = pd.merge(finalDataframe, dataframe)
#         return dataframeFinal["IPs"].sum() / len(dataframe)
#
# print("Media de conexiones de usuarios con contraseña vulnerable:", mediaConexionesVulnerables(True))
# print("Media de conexiones de usuarios con contraseña no vulnerable:", mediaConexionesVulnerables(False))

def webs_creacion():
    dataframe = pd.read_sql_query("SELECT creacion, url, cookies, aviso, proteccion_de_datos FROM webs ORDER BY url", conexion)
    dataframe["Politicas"] = dataframe["cookies"] + dataframe["aviso"] + dataframe["proteccion_de_datos"]
    dataframe_cumplen = dataframe[dataframe["Politicas"] == 3]
    print(dataframe_cumplen)
    dataframe_no_cumplen = dataframe[dataframe["Politicas"] != 3]
    print(dataframe_no_cumplen)


def num_contrasenas_comprometidas():
    dataframe = pd.read_sql_query(
        "SELECT id, contrasena FROM usuarios",conexion)
    dataframe["IPs"] = pd.read_sql_query("SELECT COUNT(ip) FROM ips group by id", conexion)
    with open("weak_pass.txt", "r") as file:
        weak_passwords = set(file.read().split("\n"))
    dataframe_comprometidas = dataframe[dataframe["contrasena"].isin(weak_passwords)]
    dataframe_no_comprometidas = dataframe[~dataframe["contrasena"].isin(weak_passwords)]
    print("Número de contraseñas comprometidas:", len(dataframe_comprometidas))
    print("Número de contraseñas no comprometidas:", len(dataframe_no_comprometidas))



