from flask import Flask, request
from pymongo import MongoClient
import json
from app import app
import os

# grab mongo db key from the secret text file
db_url = os.environ.get("MONGODB_URI")
if db_url == None:
    secret_reader = open("./app/secret_key.txt", 'r');
    db_url = secret_reader.read()
    print db_url
client = MongoClient(db_url)
db = client.heroku_jvk8p0cg

# static url
@app.route('/')
def index():
    return "Hi dudes (and dudettes), check out my insta!"
