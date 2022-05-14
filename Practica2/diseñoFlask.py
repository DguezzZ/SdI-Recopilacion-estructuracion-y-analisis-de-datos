import pandas as pd
import sqlite3
import altair as alt
import requests
from hashlib import md5
from flask import Flask, render_template, request, redirect, url_for, flash
import urllib.parse

con = sqlite3.connect('database.db', check_same_thread=False)
controlador = con.cursor()

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/vulnerables')
def vulnerables():
    df=usuarios_criticos(int(request.args.get('value',default=20)))
    grafico=alt.Chart(df).mark_bar().encode(x="id",y="probabilidad_click")
    dfspam=usuarios_spam(int(request.args.get('mayor',default=0)))
    return render_template('vulnerables.html',grafico=grafico.to_json(),value=int(request.args.get('value',default=20)),tablaUser=dfspam.to_html(),mayor=int(request.args.get('mayor',default=0)))

@app.route('/webvulnerables')
def pagvulnerables():
    df=webs_vulnerables(int(request.args.get('value',default=20)))
    grafico=alt.Chart(df).mark_bar().encode(x="url",y="Seguridad")
    return render_template('webvulnerables.html',grafico=grafico.to_json(),value=int(request.args.get('value',default=20)))



@app.route('/ultimasVulnerabilidades', methods = ['GET'])
def ultimas_vulnerabilidades():

    respuesta = requests.get("https://cve.circl.lu/api/last")       # guardamos la respuesta del servidor con las vulnerabilidades en tiempo real
    if respuesta.status_code != 200:                                # si la respuesta es distinta de 200 OK, nos salta a Exception para que no explote el código por el error
       raise Exception
    else:                                                           # si la respuesta es 200 OK, empezamos a trabajar
        archivo = respuesta.text                                     # en un formato JSON (archivo), guardamos la respuesta del servidorr
        df = pd.DataFrame()
        df["id"] = pd.read_json(archivo)["id"]               # leerá el ID de la vulnerabilidad del archivo JSON
        df["summary"] = pd.read_json(archivo)["summary"]     # leerá el resumen o descripcion de la vulnerabildad del archivo JSON

    return render_template('ultimasVulnerabilidades.html',lista=df.head(10).to_html())    # imprimirá en formato HTML las 10 primeras vulnerabilidades de la respuesta

@app.route('/obtenerservicios', methods = ['GET'])
def obtenerservicio():
    #return render_template('ultimasVulnerabilidades.html',lista=buscador_servicios(request.args.get('servicio')))
    return render_template('obtenerServiciosv2.html',lista=buscador_servicios2(request.args.get('servicio', default="Microsoft")),servicio=request.args.get('servicio', default="Microsoft"))


def usuarios_criticos(top: int):
    usr = pd.read_sql_query("SELECT id, emails_phishing, emails_clicados FROM usuarios", con)
    for index, fila in usr.iterrows():
        if fila["emails_phishing"] > 0:
            usr._set_value(index, "probabilidad_click", fila["emails_clicados"]/ fila["emails_phishing"])
        else:
            usr._set_value(index, "probabilidad_click", 0)
    usr = usr.sort_values("probabilidad_click", ascending=False).head(top)
    return usr


def webs_vulnerables(top: int):
    web = pd.read_sql_query("SELECT url, cookies, aviso, proteccion_de_datos FROM legal", con)
    web["Seguridad"] = web["cookies"] + web["aviso"] + web["proteccion_de_datos"]
    web = web.sort_values("Seguridad", ascending=False).head(top)
    return web

def usuarios_spam(mayor: int):
    if bool(mayor):
        usr = pd.read_sql_query("SELECT id, telefono, provincia, emails_total, emails_phishing, emails_clicados FROM usuarios where emails_clicados>=usuarios.emails_phishing/2", con)
    else:
        usr = pd.read_sql_query("SELECT id, telefono, provincia, emails_total, emails_phishing, emails_clicados FROM usuarios where emails_clicados<usuarios.emails_phishing/2", con)
    return usr

def ultimas_vul():
    respuesta = requests.get("https://www.cve-search.org/api/")
    if respuesta.status_code != 200:
        raise Exception
    else:
        json = respuesta.text
        data = pd.DataFrame()
        data["summary"] = pd.read_json(json)["summary"]
        data["id"] = pd.read_json(json)["id"]
        return data.head(10).to_html()

def buscador_servicios(servicio: str):
    print('UwU')
    respuesta = requests.get("http://cve.circl.lu/api/browse/"+urllib.parse.quote(servicio))
    if respuesta.status_code != 200:
        raise Exception
    else:
        json = respuesta.text
        data = pd.DataFrame()
        if "product" in pd.read_json(json):
            data["product"] = pd.read_json(json)["product"]
        return data.to_html()

def buscador_servicios2(servicio: str):
    print('UwU')
    respuesta = requests.get("http://cve.circl.lu/api/browse/"+urllib.parse.quote(servicio))
    if respuesta.status_code != 200:
        raise Exception
    else:
        json = respuesta.text
        data = pd.DataFrame()
        if "product" in pd.read_json(json):
            data["product"] = pd.read_json(json)["product"]
        return data["product"]

if __name__ == '__main__':
    app.run()


