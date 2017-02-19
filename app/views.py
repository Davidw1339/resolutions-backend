from flask import Flask, request
from pymongo import MongoClient
import json
from app import app

# grab mongo db key from the secret text file
secret_reader = open("./app/secret_key.txt", 'r');
db_url = secret_reader.read()
client = MongoClient(db_url)
db = client.heroku_jvk8p0cg

# static url
@app.route('/')
def index():
    return "Hi dudes (and dudettes), check out my insta!"
