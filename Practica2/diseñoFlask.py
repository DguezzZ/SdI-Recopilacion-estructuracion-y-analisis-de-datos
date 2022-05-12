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


if __name__ == '__main__':
    app.run(debug=True)


