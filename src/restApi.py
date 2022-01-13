# PoHelper (PoHelper Telegram bot powered by Python)
# Copyright (C) 2022  drlorente97.eth <drlorente97@gmail.com>

# General Declarations
from flask import Flask, jsonify, request

app = Flask(__name__)
@app.route('/', methods = ['GET', 'POST'] )
def get_data():
    if request.method == 'GET':
        return 'RESTful API'
    elif request.method == 'POST':
        global inp_params

        inputs = {"fileName": request.json["fileName"], "fileId": request.json["fileId"], "ModuleId": request.json["ModuleId"], "WorkflowId": request.json["WorkflowId"],"Language": request.json["Language"], "callbackuri": request.json["callbackuri"]}

        inp_params.append(inputs)
        return '200'
def run_API ():
    app.run(port='7777')
