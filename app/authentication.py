from flask import Flask, request
from pymongo import MongoClient
from app import app
import os
import db_connection


# grab mongo db key from the secret text file
db = db_connection.establish_connection()

@app.route('/test')
def test():
    return 'hello'

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    cursor = db.users.find({'username': username})
    if cursor:
        for user in cursor:
            return 'already-registered'

    password = request.form['password']

    user = db.users.insert_one(
    {
        "username": username,
        "password": password,
        "score": 0
    })
    if user:
        return "success"
    else:
        return "no-success"

@app.route('/login', methods=['GET'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    user = db.users.find_one({"username": username, "password": password})
    if user:
        return "success"
    return "no-auth"
