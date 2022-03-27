from requests.models import HTTPError
from flask import Flask, request
import requests
'''
Front server o request manager, recibe peticiones del cliente e identifica que sea
una entrada valida. Luego llama al nodo correspondiente para realizar la operacion
'''

app = Flask(__name__)
@app.route("/")
def database():

    #revisar que sea mediante json
    json_data = request.json
    if not json_data: 
        return "make sure to send arguments",202
    
    #revisar que ingrese un comando valido
    commands = ("put","get","delete")
    if "command" not in json_data or json_data["command"] not in commands:
        return "make sure to send a valid command",202
    
    command = json_data["command"]

    #realizar el llamado a los nodos con el respectivo comando
    if command == "put":
        if "key" not in json_data or "value" not in json_data:
            return "Must send a key and a value",202
        
        ret_value = put(json_data)
        return ret_value

    elif command == "get":
        if "key" not in json_data:
            return "Must send a key",202
        
        ret_value = get(json_data)
        return ret_value
    
    elif command == "delete":
        if "key" not in json_data:
            return "send a key to delete",202
        ret_value = delete(json_data)
        return ret_value
    return 

#operacion put, se hashea la llave y se le asigna el nodo, llamandolo a la ruta de dicha operacion 
def put(data):
    key = data["key"]
    node = myHash(key)
    if node == 0:
        return requests.post('http://127.0.0.1:5001/put',json=data).content
    elif node==1:
        return requests.post('http://127.0.0.1:5002/put',json=data).content
    elif node ==2:
        return requests.post('http://127.0.0.1:5003/put',json=data).content

        
#operacion get, se hashea la llave y se le asigna el nodo, llamandolo a la ruta de dicha operacion
def get(data):
    key = data["key"]
    node = myHash(key)
    if node == 0:
        try:
            return requests.post('http://127.0.0.1:5001/get',json=data).content
        except Exception:
            try:
                return requests.post('http://127.0.0.1:5002/followernode1/get',json=data).content
            except Exception:
                try:
                    return requests.post('http://127.0.0.1:5003/followernode1/get',json=data).content
                except Exception:
                    return "server is down", 202
    elif node==1:
        try:
            return requests.post('http://127.0.0.1:5002/get',json=data).content
        except Exception:
            try:
                return requests.post('http://127.0.0.1:5001/followernode2/get',json=data).content
            except Exception:
                try:
                    return requests.post('http://127.0.0.1:5003/followernode2/get',json=data).content
                except Exception:
                    return "server is down", 202
    elif node ==2:
        try:
            return requests.post('http://127.0.0.1:5003/get',json=data).content
        except Exception:
            try:
                return requests.post('http://127.0.0.1:5002/followernode3/get',json=data).content
            except Exception:
                try:
                    return requests.post('http://127.0.0.1:5001/followernode3/get',json=data).content
                except Exception:
                    return "server is down", 202

#operacion delete, se hashea la llave y se le asigna el nodo, llamandolo a la ruta de dicha operacion
def delete(data):
    key = data["key"]
    node = myHash(key)
    if node == 0:
        return requests.post('http://127.0.0.1:5001/delete',json=data).content
    elif node==1:
        return requests.post('http://127.0.0.1:5002/delete',json=data).content
    elif node ==2:
        return requests.post('http://127.0.0.1:5003/delete',json=data).content

#funcion hash personalizada %n para saber en que nodo realizar la operacion de la llave
def myHash(s):
    return (sum(ord(ch) for ch in s))%3


if __name__ == "main":
    app.run(host='127.0.0.1',port=5000)  # run our Flask app