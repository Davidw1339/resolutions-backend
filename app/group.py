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

    group = db.groups.insert_one(
        {"_id" : group_id,
        "users": [username]}
    )
    return str(group_id)


@app.route('/add_user_to_group', methods=['POST'])
def add_user_to_group():
    username = request.form['username']
    group_id = request.form['group_id']

    user = db.users.update(
        {'username': username},
        {"$set" : {"group": ObjectId(group_id)}},
    )

    group = db.groups.update(
        {"_id" : ObjectId(group_id)},
        {"$push" : {"users": username} }
    )
    return "success"