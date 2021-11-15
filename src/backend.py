# This file serves to contain all of the routes for our api.
# Within each of these routes, there should not be any computation occuring
# Instead, we handle all data parsing and handling in the controllers file

import controllers

# Credit to https://pythonbasics.org/flask-tutorial-hello-world/ prints hello world
from werkzeug.wrappers import Response
from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv
from json import dumps
import jwt
import os
from time import time

load_dotenv()

# Flask setup
app = Flask(__name__)
CORS(app)

# app.wsgi_app = auth_middleware(app.wsgi_app)

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

@app.route('/api_v1/state_taxes', methods=['POST'])
def state_taxes():
    return controllers.get_state_tax(request.json)

# Returns percent of income going to fed taxes
@app.route('/api_v1/fed_taxes', methods=['POST'])
def fed_taxes():
    return controllers.get_fed_tax(request.json)

# for testing auth middleware
@app.route('/api_v1/authtest', methods=['POST'])
def authtest():
    auth_header = request.headers.get('Authorization')
    auth_result = read_authorization(auth_header)
    if (auth_result != None):
        return auth_result
    return {'status': 'success'}

# Used to place a new offer in the database
# expects all the information that might be present in a job offer
@app.route('/api_v1/create_offer', methods=['POST'])
def create_offer():
    auth_header = request.headers.get('Authorization')
    auth_result = read_authorization(auth_header)
    if (auth_result != None):
        return auth_result
    return controllers.create_offer(request.json)

# Used to search for a job offer
# expects an id and a company name
@app.route('/api_v1/fetch_offer', methods=['POST'])
def fetch_offer():
    auth_header = request.headers.get('Authorization')
    auth_result = read_authorization(auth_header)
    if (auth_result != None):
        return auth_result
    print('json from fetch request', request.json)
    return controllers.find_offer(request.json)

# Retrieves a list of all the offers that a user has
# takes a user's id
# returns a list off all the offer id's and the company names
@app.route('/api_v1/users_offers', methods=['GET'])
def users_offers():
    auth_header = request.headers.get('Authorization')
    auth_result = read_authorization(auth_header)
    if (auth_result != None):
        return auth_result
    
    user = request.environ['user']['email']
    return controllers.users_offers(user)

# Allows users to edit an offer
@app.route('/api_v1/edit_offer', methods=['PUT'])
def edit_offer(offer_data):
    auth_header = request.headers.get('Authorization')
    auth_result = read_authorization(auth_header)
    if (auth_result != None):
        return auth_result
    return controllers.edit_offer(request.json)

def read_authorization(auth_header):
        # don't run middleware for login or register routes.
    if request.path == '/api_v1/login' or request.path == '/api_v1/register_user':
        return # do nothing

    create_error_response = lambda message: Response(response=dumps({
        'status': 'error',
        'message': message
        }),
        status=401,
        mimetype='application/json'
    )
        
    if auth_header == None:
        print('No header token')
        return create_error_response('Could not find header token. Please reauthenticate and reauthorize.')
    
    tokens = auth_header.split()
    if len(tokens) != 2:
        print('Invalid token')
        return create_error_response('Unrecognized authorization header format. Expected 2 tokens, got {}'.format(len(tokens)))
    if tokens[0] != 'Bearer':
        print('Invalid token')
        return create_error_response('Unrecognized authorization header scheme, Expected Bearer, got {}'.format(tokens[0]))
    
    session_token = tokens[1]

    try:
        session_data = jwt.decode(session_token, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])
    except jwt.DecodeError:
        print('Cannot decode token')
        return create_error_response('Could not decode jwt token.')

    # session has expired
    if session_data['expiration'] < time():
        print('Header expired')
        return create_error_response('Header has expired please reauthenticate.')

    print('session data', session_data)
    
    request.environ['user'] = { 'email': session_data['email'] }

app.run(host='0.0.0.0', port=5000) # Flask setup
