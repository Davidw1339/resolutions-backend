from flask import Flask, request
from pymongo import MongoClient
import json
from app import app
import os
import db_connection


# grab mongo db key from the secret text file
db = db_connection.establish_connection()

# static url
@app.route('/')
def index():
    return "Hi dudes (and dudettes), check out my insta!"
