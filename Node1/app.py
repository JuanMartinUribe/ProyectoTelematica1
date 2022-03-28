from flask import Flask, request
import requests
import csv   

app = Flask(__name__)

@app.route("/put",methods = ['POST'])
def put():
    updated = False
    data = dict(request.get_json())
    fields=[data["key"],data["value"]]
    key = data["key"]
    value = data["value"]
    matrix = []
    with open("node1.csv",'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            if row and row[0]!=key: matrix.append(row)
            elif row[0]==key: updated = True

    with open('node1.csv', 'w',newline='') as f:
        writer = csv.writer(f)
        for row in matrix:
                writer.writerow(row)
        writer.writerow([key,value])
    if not updated:
        return "Your key has been saved"
    else:
        return "Your key has been updated"

@app.route("/get",methods = ['POST'])
def get():

    data = dict(request.get_json())
    key = data["key"]

    matrix = []
    with open("node1.csv",'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            if row: matrix.append(row)

    for row in matrix:
        if row[0] == key:
            return row[1]

    return "key not found" , 202

@app.route("/delete",methods = ['POST'])
def delete():

    data = dict(request.get_json())
    key = data["key"]

    matrix = []
    with open("node1.csv",'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            if row: matrix.append(row)

    deleted = False
    with open('node1.csv', 'w',newline='') as f:
        writer = csv.writer(f)
        for row in matrix:
            if row[0]!=key:
                writer.writerow(row)
            else: deleted = True
    if deleted : return "key deleted" , 202
    else: return "key doesnt exist, nothing deleted",202