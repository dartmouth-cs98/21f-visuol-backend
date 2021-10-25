# the controllers file handles all of the validation and data manipulation in the API
import os

from utils.hash_password import get_hashed_password, check_password
from mongo.user_auth import add_user, get_user
from mongo.offer import add_offer, get_offer
from jwt import encode
from time import time
from constants import TOKEN_DURATION

def register_user(user_data):
    assert 'email' in user_data, 'Could not find email in user!'
    assert 'password' in user_data, 'Could not find password in user!'

    # assuming this is a dict for now, might be some flask object
    user = {}
    user['email'] = user_data['email']
    
    # hash and salt password
    hashed_password = get_hashed_password(user_data['password'])
    user['password'] = hashed_password

    # new registered users are unverified by default
    user['is_verified'] = False

    # company is None if the user is not affiliated with a company
    user['company'] = user_data['company']

    user['name'] = user_data['name']

    # have a session field but keep this none for now
    # by default when registering we're not handing out a session token
    # should be done in a different call
    user['session'] = None

    resp = add_user(user)

    # we threw an error, return it
    if resp != None:
        return {
            'status': 'failure',
            'error': resp
        }
    
    return {
        'status': 'success'
    }
        
def login(user_data):
    assert user_data != None, 'Could not find user data!'
    assert user_data['email'] != None, 'Could not find user email!'
    assert user_data['password'] != None, 'Could not find user password!'

    email = user_data['email']
    password = user_data['password']
    user = get_user(email)
    if user == None:
        return {
            'status': 'failure',
            'error': 'Could not find user for email {}'.format(email)
        }

    if not check_password(password, user['password']):
        return {
            'status': 'failure',
            'error': 'Incorrect password'
        }

    # expiration is in seconds from epoch, token duration in hours
    expiration = time() + (TOKEN_DURATION * 360)
    session_token = encode({'email': email, 'expiration': expiration}, os.getenv('JWT_SECRET_KEY'), algorithm="HS256")

    return {
        'status': 'success',
        'session_token':  'Bearer {}'.format(session_token),
        'expiration': expiration
    }

def create_offer(offer_data):
    offer = {}

    offer['company'] = offer_data['company']
    offer['date'] = offer_data['date']
    offer['expiration'] = offer_data['expiration']
    offer['base'] = offer_data['base']
    offer['bonus'] = offer_data['bonus']
    offer['401K'] = offer_data['401K']
    offer['PTO'] = offer_data['PTO']

    resp = add_offer(offer)

    # we threw an error, return it
    if resp != None:
        return {
            'status': 'failure',
            'error': resp
        }

    return {
        'status': 'success'
    }

def find_offer(offer_data):
    assert offer_data['id'] != None, "id needed."
    assert offer_data['company'] != None, "company name needed."

    company = offer_data['company']
    offer_id = offer_data['id']

    offer = get_offer(offer_id)

    if offer is None:
        return {
            'status': 'failure',
            'error': 'Could not find offer for id {}'.format(offer_id)
        }

    if offer_id['company'] != company:
        return {
            'status': 'failure',
            'error': 'Offer does not match company'
        }

    return offer
