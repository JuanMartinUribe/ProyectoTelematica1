from flask import Flask, request
import requests



app = Flask(__name__)
@app.route("/")
def database():

    json_data = request.json
    if not json_data: 
        return "make sure to send arguments",202

    commands = ("put","get","delete")
    if "command" not in json_data or json_data["command"] not in commands:
        return "make sure to send a valid command",202
    
    command = json_data["command"]

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


def put(data):
    key = data["key"]
    node = myHash(key)
    if node == 0:
        return requests.post('http://127.0.0.1:5001/put',json=data).content
    elif node==1:
        return requests.post('http://127.0.0.1:5002/put',json=data).content
        

def get(data):
    key = data["key"]
    node = myHash(key)
    if node == 0:
        return requests.post('http://127.0.0.1:5001/get',json=data).content
    elif node==1:
        return requests.post('http://127.0.0.1:5002/get',json=data).content

def delete(data):
    key = data["key"]
    node = myHash(key)
    if node == 0:
        return requests.post('http://127.0.0.1:5001/delete',json=data).content
    elif node==1:
        return requests.post('http://127.0.0.1:5002/delete',json=data).content
        

def myHash(s):
    return (sum(ord(ch) for ch in s))%2


if __name__ == "main":
    app.run(host='127.0.0.1',port=5000)  # run our Flask app