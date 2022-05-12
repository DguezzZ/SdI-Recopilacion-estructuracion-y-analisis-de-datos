from urllib import request

import pandas as pd
import sqlite3
import numpy as np
import matplotlib.pyplot as plt

from flask import Flask, render_template,request, redirect




con = sqlite3.connect('database.db')
controlador = con.cursor()



app = Flask(__name__)

@app.route('/')




