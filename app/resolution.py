from flask import Flask, request
from pymongo import MongoClient
from app import app

from datetime import datetime, timedelta
import geopy
from geopy.distance import vincenty
from geopy.geocoders import Nominatim
import os
import json
import db_connection


# grab mongo db key from the secret text file
db = db_connection.establish_connection()

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
                "longitude": longitude,
                "latitude": latitude,
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
    if(len(resolution) == 0 ):
        return "poop"
    formatted_json = format_resolution_json(resolution)

    if formatted_json:
        return json.dumps(formatted_json)
    return "poop"


def format_resolution_json(resolution):
    formatted_json = {"resolution": resolution["resolution"],
                    "location": resolution["location"],
                    "longitude": float(resolution["longitude"]),
                    "latitude": float(resolution["latitude"]),
                    "days": [int(x) for x in resolution["days"]],
                    "start_time": '{:%I:%M%p}'.format(resolution["start_time"]),
                    "end_time": '{:%I:%M%p}'.format(resolution["end_time"])
                    }
    return formatted_json


@app.route('/valid_check_in', methods=['POST'])
def valid_check_in():
    username = request.form['username']
    user = db.users.find_one({"username": username})
    resolution = user["resolutions"]
    formatted_resolution = format_resolution_json(resolution)

    current_latitude = request.form['latitude']
    current_longitude = request.form['longitude']
    current_checkin = datetime.now()
    day_of_week = current_checkin.weekday()

    if user["last_checkin"] is None:
        min_checkin = current_checkin - timedelta(1)
    else:
        min_checkin = user["last_checkin"] +  timedelta(days=1)

    if current_checkin >= min_checkin:
        if day_of_week in formatted_resolution["days"]:
            if vincenty((current_latitude, current_longitude), (resolution['latitude'], resolution['longitude'])).miles < 0.25:
                user = db.users.update(
                    {'username': username},
                    {"$inc" : {"score": 1},
                    "$set" : {"last_checkin" : current_checkin}}
                )
                return "valid"
    return "invalid"
