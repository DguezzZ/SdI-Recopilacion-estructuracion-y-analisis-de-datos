import pandas as pd
import sqlite3
import numpy as np

conexion = sqlite3.connect('database.db')
controlador = conexion.cursor()


def crearDataframe():
    dataframe = pd.read_sql_query("SELECT * FROM usuarios group by id", conexion)
    dataframe["IPs"] = pd.read_sql_query("SELECT COUNT(ip) from ips group by id", conexion)
    dataframe["Fechas"] = pd.read_sql_query("SELECT COUNT(fecha) FROM fechas group by id", conexion)
    return dataframe

dataframe = crearDataframe()

####################################### DATOS ######################################

def cuentaValoresPerdidos(dataframe):
    cont = 0
    for index, row in dataframe.iterrows():
        if row["telefono"] is None:
            cont += 1
        if row["provincia"] is None:
            cont += 1
        if row["IPs"] == 0:
            cont += 1
    return cont

def valoresDisponibles(dataframe):
    return len(dataframe) * len(dataframe.columns) - cuentaValoresPerdidos(dataframe)
print("Numero de muestras:\n", valoresDisponibles(dataframe))

####################################### DATOS 1 ######################################

def mediaFechas(dataframe) -> float:
    return dataframe["Fechas"].sum() / len(dataframe)
print("Media del total de fechas que se ha iniciado sesión:\n", mediaFechas(dataframe))


def desviacionFechas(dataframe) -> float:
    return float(np.std(dataframe["Fechas"].to_numpy()))
print("Desviación estándar del total de fechas que se ha iniciado sesión:\n", desviacionFechas(dataframe))

####################################### DATOS 2######################################

def mediaIps(dataframe) -> float:
    return dataframe["IPs"].sum() / len(dataframe)
print("Media del total de IPs que se han detectado:\n", mediaIps(dataframe))

def desviacionIps(dataframe) -> float:
    return float(np.std(dataframe["IPs"].to_numpy()))
print("Desviación estándar del total de IPs que se han detectado:\n", desviacionIps(dataframe))

####################################### DATOS 3 ######################################

def mediaEmailsTotales(dataframe) -> float:
    return dataframe["emails_total"].sum() / len(dataframe)
print("Media del número de emails recibidos:\n", mediaEmailsTotales(dataframe))

def desviacionEmailsTotales(dataframe) -> float:
    return float(np.std(dataframe["emails_total"].to_numpy()))
print("Desviación estándar del número de emails recibidos:\n", desviacionEmailsTotales(dataframe))

####################################### DATOS 4 ######################################

def minFechas(dataframe) -> int:
    return dataframe["Fechas"].min()
print("Valor mínimo del total de fechas que se ha iniciado sesión:\n", minFechas(dataframe))

def maxFechas(dataframe) -> int:
    return dataframe["Fechas"].max()
print("Valor máximo del total de fechas que se ha iniciado sesión:\n", maxFechas(dataframe))

####################################### DATOS 5 ######################################

def minEmailsTotales(dataframe) -> int:
    return dataframe["emails_total"].min()
print("Valor mínimo del número de emails recibidos:\n", minEmailsTotales(dataframe))


def maxEmailsTotales(dataframe) -> int:
    return dataframe["emails_total"].max()
print("Valor máximo del número de emails recibidos:\n", maxEmailsTotales(dataframe))
