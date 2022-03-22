from requests.models import HTTPError
from flask import Flask, request, abort
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import requests
import os


app = Flask(__name__)
@app.route("/")
def database():

    json_data = request.json
    if not json_data: 
        return "make sure to send arguments"

    commands = ("store","get","update","delete")
    if "command" not in json_data or json_data["command"] not in commands:
        return "make sure to send a valid command"
    
    command = json_data["command"]

    if command == "store":
        if "key" not in json_data or "value" not in json_data:
            return "Must send a key and a value"
        
        ret_value = put(json_data)
        return ret_value

    elif command == "get":
        if "key" not in json_data:
            return "Must send a key"
        
        ret_value = get(json_data)
        return ret_value
    return "nada"


def put(data):
    key = data["key"]
    node = myHash(key)
    if node == 0:
        return requests.post('http://127.0.0.1:5010/put',json=data)
    elif node==1:
        requests.post('http://127.0.0.1:5000/put',json=data)
        return "Your key has been saved"

def get(data):
    key = data["key"]
    node = myHash(key)
    if node == 0:
        return requests.post('http://127.0.0.1:5010/get',json=data)
    elif node==1:
        return requests.post('http://127.0.0.1:5000/get',json=data).content
        

def myHash(s):
    return (sum(ord(ch) for ch in s))%2


if __name__ == "main":
    app.run(host='127.0.0.1',port=5001)  # run our Flask app