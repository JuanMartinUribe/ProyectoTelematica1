from flask import Flask, request
import requests
import csv   

app = Flask(__name__)

@app.route("/put",methods = ['POST'])
def put():
    updated = False
    data = dict(request.get_json())
    key = data["key"]
    value = data["value"]
    matrix = []

    with open("node3.csv",'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            if row and row[0]!=key: matrix.append(row)
            elif row[0]==key: updated = True

    with open('node3.csv', 'w',newline='') as f:
        writer = csv.writer(f)
        for row in matrix:
                writer.writerow(row)
        writer.writerow([key,value])

    #metodo para actualizar los followers, es totalmente sincronico porque se debe esperar a que el proceso termine
    follower()

    if not updated:
        return "Your key has been saved"
    else:
        return "Your key has been updated"

#ruta del get del nodo, se retorna el valor de la llave, o un mensaje en caso de que no exista
@app.route("/get",methods = ['POST'])
def get():
    data = dict(request.get_json())
    key = data["key"]
    matrix = []
    
    with open("node3.csv",'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            if row: matrix.append(row)

    for row in matrix:
        if row[0] == key:
            return row[1]

    return "key not found" , 202

#ruta del delete del nodo, se borra la llave en caso de que exista
@app.route("/delete",methods = ['POST'])
def delete():
    data = dict(request.get_json())
    key = data["key"]

    matrix = []
    with open("node3.csv",'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            if row: matrix.append(row)

    deleted = False
    with open('node3.csv', 'w',newline='') as f:
        writer = csv.writer(f)
        for row in matrix:
            if row[0]!=key:
                writer.writerow(row)
            else: deleted = True
    if deleted :
        #se llama a los followers de los otros nodos para actualizar la informacion 
        follower()
        return "key deleted" , 202
    else: return "key doesnt exist, nothing deleted",202

#ruta en caso de que el nodo se llame para actualizar los followers que residen en este nodo
@app.route("/followernode1",methods = ['POST'])
def replicaNode1():
    file = request.files['file']
    file.save('node1follower.csv')
    return '',202
@app.route("/followernode2",methods = ['POST'])
def replicaNode2():
    file = request.files['file']
    file.save('node2follower.csv')
    return '',202

#metodo que llama los followers ubicados en otros nodos para ser actualizados
def follower():
    file = {'file':open('node3.csv','rb')}
    requests.post('http://127.0.0.1:5001/followernode3',files=file)
    file = {'file':open('node3.csv','rb')}
    requests.post('http://127.0.0.1:5002/followernode3',files=file)



@app.route("/followernode1/get",methods = ['POST'])
def getNode1Follower():
    data = dict(request.get_json())
    key = data["key"]
    matrix = []

    with open("node1follower.csv",'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            if row: matrix.append(row)

    for row in matrix:
        if row[0] == key:
            return row[1]

    return "key not found" , 202

@app.route("/followernode2/get",methods = ['POST'])
def getNode2Follower():
    data = dict(request.get_json())
    key = data["key"]
    matrix = []

    with open("node2follower.csv",'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            if row: matrix.append(row)

    for row in matrix:
        if row[0] == key:
            return row[1]

    return "key not found" , 202