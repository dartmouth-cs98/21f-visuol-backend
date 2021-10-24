# This file serves to contain all of the routes for our api.
# Within each of these routes, there should not be any computation occuring
# Instead, we handle all data parsing and handling in the controllers file

import os
import controllers

#Credit to https://pythonbasics.org/flask-tutorial-hello-world/ prints hello world
from flask import Flask
from flask import request
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# MongoDB connection setup from https://www.mongodb.com/blog/post/getting-started-with-python-and-mongodb
client = MongoClient(os.getenv('MONGODB_URL'))
db=client.admin
# Issue the serverStatus command and print the results
print(db.command("serverStatus"))

# Flask setup
app = Flask(__name__)
app.config('SECRET_KEY') = os.getenv('JWT_SECRET_KEY')

@app.route('/')
def index():
    return 'Hello World!'

# Expects a json file with user information
# Fields currently include email and password
@app.route('/api_v1/register_user', methods=['POST'])
def register_user():
    return controllers.register_user(request.json)

@app.route('/api_v1/login', methods=['POST'])
def login():
    return controllers.login(request.json)

@app.route('/api_v1/authtest', methods=['POST'])
def authtest():
    return {'status': 'success'}


app.run(host='0.0.0.0', port=81)# Flask setup
app = Flask(__name__)