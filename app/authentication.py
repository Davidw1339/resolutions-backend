from flask import Flask, request
from pymongo import MongoClient
from app import app

# grab mongo db key from the secret text file
secret_reader = open("./app/secret_key.txt", 'r');
db_url = secret_reader.read()
print db_url
client = MongoClient(db_url.strip())
# client = MongoClient("mongodb://heroku_jvk8p0cg:bmfkj28v7ulnn2c9ptiga42n0n@ds145355.mlab.com:45355/heroku_jvk8p0cg")
db = client.heroku_jvk8p0cg

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
        "password": password
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
