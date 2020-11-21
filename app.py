from flask import Flask, request, Response
import mariadb
import json
import random
from datetime import datetime
from flask_cors import CORS
import userfunction
import followfunction

app = Flask(__name__)
CORS(app)


@app.route('/login', methods=['POST', 'DELETE'])
def login():
    if request.method == "POST":
        username = request.json.get('username')
        password = request.json.get('password')
        user = userfunction.login(username, password)        
        if user != None:
            return Response(json.dumps(user, default=str), mimetype="application/json", status=200)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    if request.method == "DELETE":
        token = request.json.get('loginToken')
        if userfunction.logout(token):
            return Response("Delete Succsess!", mimetype="text/html", status=201)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
        
@app.route('/users', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def users():
    if request.method == 'GET':
        user_id = request.args.get("user_id")
        data = userfunction.getUsers(user_id)
        if data != None:
            return Response(json.dumps(data, default=str), mimetype="application/json", status=200)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500) 
    elif request.method == "POST":
        email = request.json.get('email')
        username = request.json.get('username')
        password = request.json.get('password')
        birthdate = request.json.get('birthdate')
        bio = request.json.get('bio')
        url = request.json.get('url')
        date = str(datetime.now())[0:10]
        if userfunction.signUp(email, username, password, birthdate, bio, date, url):
            user = userfunction.login(username, password)
            if user != None:
                return Response(json.dumps(user, default=str), mimetype="application/json", status=201)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "PATCH":
        email = request.json.get('email')
        username = request.json.get('username')
        password = request.json.get('password')
        birthdate = request.json.get('birthdate')
        bio = request.json.get('bio')
        url = request.json.get('url')
        user_id = request.json.get('user_id')
        if userfunction.modifyAccount(email, username, password, birthdate, bio, url, user_id):
            return Response("Modify Succsess!", mimetype="text/html", status=201)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "DELETE":
        user_id = request.json.get('user_id')
        if userfunction.deleteAccount(user_id):
            return Response("Delete Succsess!", mimetype="text/html", status=201)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)

@app.route('/follows', methods=['GET', 'POST', 'DELETE'])
def follows():
    if request.method == "GET":
        user_id = request.args.get("userId")
        users = followfunction.getFollows(user_id)
        if users != None:
            return Response(json.dumps(users, default=str), mimetype="application/json", status=200)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500) 
    elif request.method == "POST":
        token = request.json.get('loginToken')
        follow_id = request.json.get('followId')
        if followfunction.follows(token, follow_id):
            return Response("Follows Succsess!", mimetype="text/html", status=204)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "DELETE":
        token = request.json.get('loginToken')
        follow_id = request.json.get('followId')   
        if followfunction.unFollows(token, follow_id):
            return Response("Delete Succsess!", mimetype="text/html", status=204)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
        
@app.route('/followers', methods=['GET'])
def followers():
    if request.method == "GET":
        user_id = request.args.get("userId")
        users = followfunction.getFollowers(user_id)
        if users != None:
            return Response(json.dumps(users, default=str), mimetype="application/json", status=200)
        else:
            return Response("Something went wrong!", mimetype="text/html", status=500)
        
@app.route('/users', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def tweets():
    if request.method == "GET": 
        user_id = request.args.get('userId')
        
    
        
        
        