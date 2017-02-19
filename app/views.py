from flask import Flask, request
from pymongo import MongoClient
import json
from app import app

# grab mongo db key from the secret text file
secret_reader = open("./app/secret_key.txt", 'r');
db_url = secret_reader.read()
client = MongoClient(db_url)

# static url
@app.route('/')
def index():
    return "Hello, World!"

# url parameters
@app.route('/endpoint/<input>')
def endpoint(input):
    return input

# api with endpoint
@app.route('/nameEndpoint', methods=['GET'])
def nameEndpoint():
    if 'name' in request.args:
    	return 'My name is ' + request.args['name']
