import pandas as pd
import sqlite3
from flask import Flask, render_template, request, redirect
import altair as alt
import requests
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from LoggedUser import LoggedUser
from hashlib import md5

conexion = sqlite3.connect('database.db')
controlador = conexion.cursor()


app = Flask(__name__, template_folder='templates', static_folder='templates')
app.config['SECRET_KEY'] = '1'
login_manager = LoginManager(app)
login_manager.login_view = "/login"


def df_usuarios_criticos(x: int):
    dataframe = pd.read_sql_query("SELECT id, emails_clicados, emails_phishing, contrasena FROM usuarios",
                                  conexion)
    for indice, fila in dataframe.iterrows():
        if fila["emails_phising"] == 0:
            dataframe._set_value(indice, "prob_click", 0)
        else:
            dataframe._set_value(indice, "prob_clicks", fila["emails_clicados"] / fila["emails_phising"])

    dataframe = dataframe.sort_values("prob_click", ascending=False)

    with open("pass_debil.txt", "r") as file:
        passwd_debiles = set(file.read().split("\n"))
    dataframe = dataframe[dataframe["contrasena"].isin(passwd_debiles)]
    dataframe = dataframe.head(x)
    return dataframe


def df_webs_vulnerables(x: int):
    dataframe = pd.read_sql_query("SELECT url, cookies, aviso, proteccion_de_datos FROM webs ORDER BY url",
                                  conexion)
    dataframe["Politicas"] = dataframe["cookies"] + dataframe["aviso"] + dataframe["proteccion_de_datos"]
    dataframe = dataframe.sort_values("Politicas").head(x)
    return dataframe


############################### EJERCICIO 4 ###############################

def ultimas_vulnerabilidades():
    respuesta = requests.get("https://cve.circl.lu/api/last")       # guardamos la respuesta del servidor con las vulnerabilidades en tiempo real
    if respuesta.status_code != 200:                                # si la respuesta es distinta de 200 OK, nos salta a Exception para que no explote el código por el error
        raise Exception
    else:                                                           # si la respuesta es 200 OK, empezamos a trabajar
        archivo = respuesta.txt                                     # en un formato JSON (archivo), guardamos la respuesta del servidorr
        dataframe = pd.DataFrame()
        dataframe["id"] = pd.read_json(archivo)["id"]               # leerá el ID de la vulnerabilidad del archivo JSON
        dataframe["summary"] = pd.read_json(archivo)["summary"]     # leerá el resumen o descripcion de la vulnerabildad del archivo JSON

        return dataframe.head(10).to_html()                         # imprimirá en formato HTML las 10 primeras vulnerabilidades de la respuesta

