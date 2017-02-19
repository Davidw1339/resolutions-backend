from flask import Flask, request
from pymongo import MongoClient
from bson.objectid import ObjectId
from app import app

from datetime import datetime
import geopy
from geopy.distance import vincenty
from geopy.geocoders import Nominatim
import os
import json
import db_connection


# grab mongo db key from the secret text file
db = db_connection.establish_connection()

@app.route('/create_group', methods=['POST'])
def create_group():
    username = request.form['username']
    group_id = ObjectId()

    user = db.users.update(
        {'username': username},
        {"$set" : {"group": ObjectId(group_id)}},
    )

    user = db.users.find_one({"username": username})
    group = db.groups.insert_one(
        {"_id" : group_id,
        "users": [{username : user["score"]}]
        }
    )
    return str(group_id)


@app.route('/add_user_to_group', methods=['POST'])
def add_user_to_group():
    username = request.form['username']
    group_id = request.form['group_id']

    user = db.users.update(
        {'username': username},
        {"$set" : {"group": ObjectId(group_id), "score": 0}},
    )

    user = db.users.find_one({"username": username})
    if user == None:
        return "user not found"
    group = db.groups.update(
        {"_id" : ObjectId(group_id)},
        {"$push" : {"users": {username: user["score"]}} }
    )
    return "user found"

@app.route('/find_users_group', methods=['GET'])
def find_users_group():
    username = request.args.get('username')
    user = db.users.find_one({"username": username})
    group_id = user['group']
    group = db.groups.find_one({"_id": ObjectId(group_id)})
    if(group):
        return json.dumps({"list":group['users']})
    else:
        return "no group"
