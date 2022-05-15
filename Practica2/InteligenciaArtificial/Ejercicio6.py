import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json

##regresionlinear##
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

##decisiontree##
from sklearn import tree
from sklearn.datasets import load_iris

##randomforest##
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import export_graphviz
from subprocess import call
import graphviz

array_usernames = []
array_recibidos = []
array_clickados = []
array_vulnerables = []

## VAMOS A ENTRENAR EL SISTEMA CON EL ARCHIVO "users_IA_clases.json" QUE TIENE 30 USUARIOS DIVIDIENDOLO POR LA MITAD PARA TRAIN/TEST ##

with open("users_IA_clases.json", "r") as file:
    data = json.load(file)
for usuario in data["usuarios"]:
    array_usernames = array_usernames + [usuario["usuario"]]
    array_recibidos = array_recibidos + [usuario["emails_phishing_recibidos"]]
    array_clickados = array_clickados + [usuario["emails_phishing_clicados"]]
    array_vulnerables = array_vulnerables + [usuario["vulnerable"]]

## METEMOS LOS DATOS EN UN DATA FRAME CALCULANDO LA PROBABILIDAD DE CLICKAR EN UN EMAIL PHISING RECIBIDO ##

df = pd.DataFrame()
df["array_recibidos"] = array_recibidos
df["array_clickados"] = array_clickados
for index, row in df.iterrows():
    if row["array_recibidos"] == 0:
        df._set_value(index, "prob_click", 0)
    else:
        df._set_value(index, "prob_click", row["array_clickados"] / row["array_recibidos"])
df = df.to_numpy()

df_etiqueta = pd.DataFrame()
df_etiqueta["vulnerable"] = array_vulnerables

##linear regression##

# Use only one feature
df = df[:, np.newaxis, 2]
# Split the data into training/testing sets # # half/half = 15/15 #
df_train = df[:-15]
df_test = df[-15:]
# Split the targets into training/testing sets
df_etiqueta_train = df_etiqueta[:-15]
df_etiqueta_test = df_etiqueta[-15:]
## Create linear regression object
regr = linear_model.LinearRegression()
# Train the model using the training sets
regr.fit(df_train, df_train)
print(regr.coef_)
# Make predictions using the testing set
df_pred = regr.predict(df_test)
# The mean squared error
print("Linear Regression mean squared error: %.2f" % mean_squared_error(df_etiqueta_test, df_pred))

## Plot linear regression outputs
plt.scatter(df_test, df_etiqueta_test, color="black")
plt.plot(df_test, df_pred, color="blue", linewidth=3)
plt.xticks(())
plt.yticks(())
plt.show()


##AHORA USAREMOS NUESTRO DATASET DE PREDECIR##

array_usernames = []
array_recibidos = []
array_clickados = []

with open("users_IA_predecir.json", "r") as file:
    data = json.load(file)
for user in data["usuarios"]:
    array_usernames = array_usernames + [user["usuario"]]
    array_recibidos = array_recibidos + [user["emails_phishing_recibidos"]]
    array_clickados = array_clickados + [user["emails_phishing_clicados"]]


##dataframes sobre predecir/testing data##
df = pd.DataFrame()
df["array_recibidos"] = array_recibidos
df["array_clickados"] = array_clickados
for index, row in df.iterrows():
    if row["array_recibidos"] == 0:
        df._set_value(index, "prob_click", 0)
    else:
        df._set_value(index, "prob_click", row["array_clickados"] / row["array_recibidos"])
df = df.to_numpy()

##linear regression##
df=df[:,np.newaxis,2]
df_pred = regr.predict(df)
print(df_pred)

## Decisión tree ##
X, y = df_train, df_etiqueta_train
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, y)

## Random Forest ##
clf2 = RandomForestClassifier(max_depth=2, random_state=0,n_estimators=10)
clf2.fit(X, y.values.ravel())
print(clf.predict(df))

## Plot decision tree ##
dot_data = tree.export_graphviz(clf, out_file=None)
graph = graphviz.Source(dot_data)
graph.render("decisiontree")
dot_data = tree.export_graphviz(clf, out_file=None,filled=True, rounded=True,special_characters=True)
graph = graphviz.Source(dot_data)
graph.render('decisiontree.gv', view=True).replace('\\', '/')
##Random forest##
print(clf2.predict(df))
for i in range(len(clf2.estimators_)):
    estimator = clf2.estimators_[i]
    dot_data= export_graphviz(estimator,out_file=None,rounded=True, proportion=False,precision=2, filled=True)
    #call(['dot', '-Tpng', 'randomforest.dot', '-o', 'tree'+str(i)+'.png', '-Gdpi=600'])
    graph = graphviz.Source(dot_data)
    graph.render('randomforest'+str(i)+'.gv', view=True).replace('\\', '/')
