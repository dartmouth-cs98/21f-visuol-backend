# This file serves to contain all of the routes for our api.
# Within each of these routes, there should not be any computation occuring
# Instead, we handle all data parsing and handling in the controllers file

import controllers

# Credit to https://pythonbasics.org/flask-tutorial-hello-world/ prints hello world
from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv

from utils.auth_middleware import auth_middleware

load_dotenv()

# Flask setup
app = Flask(__name__)
CORS(app)
app.wsgi_app = auth_middleware(app.wsgi_app)

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

# for testing auth middleware
@app.route('/api_v1/authtest', methods=['POST'])
def authtest():
    return {'status': 'success'}

@app.route('/api_v1/create_offer', methods=['POST'])
def create_offer():
    return controllers.create_offer(request.json)

@app.route('/api_v1/fetch_offer', methods=['GET'])
def fetch_offer():
    return controllers.find_offer(request.json)


app.run(host='0.0.0.0', port=5000) # Flask setup
app = Flask(__name__)