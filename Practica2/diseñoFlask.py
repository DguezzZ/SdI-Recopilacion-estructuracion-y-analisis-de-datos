import pandas as pd
import sqlite3
from flask import Flask, render_template, request, redirect
import altair as alt
import requests

from hashlib import md5
from flask import Flask, render_template,request, redirect

con = sqlite3.connect('database.db')
controlador = con.cursor()



app = Flask(__name__)

@app.route('/')
def mainPage():
    return render_template('mainPage.html')


@app.route('/ultimasVulnerabilidades', methods = ['GET'])
def ultimas_vulnerabilidades():
    array = [1,2,3]
##revisar oscar##
#    respuesta = requests.get("https://cve.circl.lu/api/last")       # guardamos la respuesta del servidor con las vulnerabilidades en tiempo real
#    if respuesta.status_code != 200:                                # si la respuesta es distinta de 200 OK, nos salta a Exception para que no explote el código por el error
#        raise Exception
 #   else:                                                           # si la respuesta es 200 OK, empezamos a trabajar
  #      archivo = respuesta.txt                                     # en un formato JSON (archivo), guardamos la respuesta del servidorr
   #     dataframe = pd.DataFrame()
    #    dataframe["id"] = pd.read_json(archivo)["id"]               # leerá el ID de la vulnerabilidad del archivo JSON
     #   dataframe["summary"] = pd.read_json(archivo)["summary"]     # leerá el resumen o descripcion de la vulnerabildad del archivo JSON

    return render_template('ultimasVulnerabilidades.html',pene=array)                      # imprimirá en formato HTML las 10 primeras vulnerabilidades de la respuesta

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

def usuarios_spam(mayor: bool):
    if mayor:
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



if __name__ == '__main__':
    app.run(debug=True)


