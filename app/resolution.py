from flask import Flask, request
from pymongo import MongoClient
from app import app

from datetime import datetime
from geopy.geocoders import Nominatim

# grab mongo db key from the secret text file
secret_reader = open("./app/secret_key.txt", 'r');
db_url = secret_reader.read()
print db_url
client = MongoClient(db_url.strip())

@app.route('/create', methods=['POST'])
def create():
    username = request.form['username']
    resoltion = request.form['resoltion']
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    days = request.form['days'] # array of ints 0-6
    time_start = request.form['time_start'] # format -- 1:30PM
    time_end = request.form['time_end'] # format -- 2:30PM

    datetime_time_start = datetime.strptime(time_start, '%I:%M%p')
    datetime_time_end = datetime.strptime(time_end, '%I:%M%p')

    new_res = {"resoltion": resoltion,
                "latitude": latitude,
                "longitude": longitude,
                "days": days,
                "time": time,
                }

    user = mongo.db.users.update(
        {'username': username},
        { "$push": { resolutions: new_res} }
    )


'''
@app.route('/checkin', methods=['POST'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    user = db.users.find_one({"username": username, "password": password})
    if user:
        return "success"
    return "no-auth"
'''
