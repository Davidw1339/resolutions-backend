from flask import Flask, request
from pymongo import MongoClient
from app import app
import os

db_url = os.environ.get("MONGODB_URI")
if db_url == None:
    secret_reader = open("./app/secret_key.txt", 'r');
    db_url = secret_reader.read()
client = MongoClient(db_url.strip())
db = client.heroku_jvk8p0cg

def establish_connection():
    return db
