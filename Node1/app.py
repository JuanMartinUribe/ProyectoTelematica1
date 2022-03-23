from numpy import e
from flask import Flask, request, abort
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import requests
import os
import csv   

app = Flask(__name__)

@app.route("/put",methods = ['POST'])
def put():

    data = dict(request.get_json())
    fields=[data["key"],data["value"]]
    
    with open(r'node1.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
    return "Your key has been saved"

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