# ProyectoTelematica1
Juan Martin Uribe
Daniel Jose Giraldo
Hector Banilat

DISTRIBUTED DATABASE KEY:VALUE with FLASK

Requirements
Python, ideally in a venv:
-pip install flask
-pip install requests

Run Main Server app on default port
Run nodes App on 5001, 5002, 5003 ... every node has a csv named with its respective node.
Flask run --host: "host" --port: "port" On every Node 

The central server and every node is a different app, they are independent from each other.
Run each app, you can use multiple terminals.
The main app must know the ip and port of its nodes, and the hash function must % n depending on how many nodes there are.
