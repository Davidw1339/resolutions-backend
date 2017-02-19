from flask import Flask, request
from pymongo import MongoClient
from app import app

from datetime import datetime
import geopy
from geopy.geocoders import Nominatim
import os
import json

# grab mongo db key from the secret text file
db_url = os.environ.get("MONGODB_URI")
if db_url == None:
    secret_reader = open("./app/secret_key.txt", 'r');
    db_url = secret_reader.read()
    print db_url
client = MongoClient(db_url.strip())
db = client.heroku_jvk8p0cg

@app.route('/create_resolution', methods=['POST'])
def create_resolution():
    username = request.form['username']
    resolution = request.form['resolution']
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    days = request.form['days'] # array of ints 0-6
    time_start = request.form['time_start'] # format -- 1:30PM
    time_end = request.form['time_end'] # format -- 2:30PM

    geolocator = Nominatim()
    point = geopy.Point(latitude=latitude, longitude=longitude)
    location, (longit, latit) = geolocator.reverse(point)

    datetime_time_start = datetime.strptime(time_start, '%I:%M%p')
    datetime_time_end = datetime.strptime(time_end, '%I:%M%p')

    new_res = {"resolution": resolution,
                "location": location,
                #"longitude": longitude,
                #"latitude": latitude,
                "days": days.split(),
                "start_time": datetime_time_start,
                "end_time": datetime_time_end,
                }

    user = db.users.update(
        {'username': username},
        {"$set" : {"resolutions": new_res}},
    )

    return "success"

@app.route('/get_resolution', methods=['GET'])
def get_resolution():
    username = request.args.get('username')
    user = db.users.find_one({"username": username})
    resolution = user["resolutions"]
    formatted_json = format_resolution_json(resolution)

    if formatted_json:
        return json.dumps(formatted_json)
    return "poop"


def format_resolution_json(resolution):
    formatted_json = {"resolution": resolution["resolution"],
                    "location": resolution["location"],
                    "days": [int(x) for x in resolution["days"]],
                    "start_time": '{:%I:%M%p}'.format(resolution["start_time"]),
                    "end_time": '{:%I:%M%p}'.format(resolution["end_time"])
                    }
    return formatted_json


@app.route('/valid_check_in', methods=['GET'])
def valid_check_in():
    username = request.args.get('username')
    user = db.users.find_one({"username": username})
    resolution = user["resolutions"]
    formatted_resolution = format_resolution_json(resolution)

    current_latitude = request.args.get('latitude')
    current_longitude = request.args.get('longitude')
    now = datetime.now()
    day_of_week = now.weekday()

    geolocator = Nominatim()
    point = geopy.Point(latitude=current_latitude, longitude=current_longitude)
    location, (longit, latit) = geolocator.reverse(point)

    if(day_of_week in formatted_resolution["days"]):
        if(location == formatted_resolution["location"]):
            if resolution["start_time"] < now < resolution["start_end"]:
                return "valid"
    return "invalid"
