import os
from dotenv import load_dotenv

load_dotenv()

from pymongo import MongoClient
client = MongoClient(os.getenv('MONGODB_URL'))

# MongoDB connection setup from https://www.mongodb.com/blog/post/getting-started-with-python-and-mongodb
db = client.VisuOL
auth_col = db['user_authentication']


# Adds a user to the user_authentication table
# Users are a dictionary with the following fields
# email (required), password (required), session_token (nullable), is_verified (required)
def add_user(user):
    # TODO: add more input validation and check if user already exists

    assert user != None, 'No User Found!'
    assert user['email'] != None, 'No email found!'
    assert user['password'] != None, 'No password found!'
    assert user['name'] != None, 'No name found!'
    
    # verify that the user doesn't already exist
    if auth_col.find_one('') != None:
        return 'Email for user {} already exists!'.format(user['email'])
    auth_col.insert_one(user)
    return None

def get_user(user_email):
    assert user_email != None, 'No user email found!'
    return auth_col.find_one({'email': user_email})

def verify_user(user_email):
    assert user_email != None

# Deletes a user from the user authentication table
def delete_user(user_email):
    assert user_email != None, 'No user email found!'
    auth_col.delete_one({'email': user_email})
    

if __name__ == '__main__':
    add_user({
        'email': 'test@gmail.com',
        'password': 'hashedpassword',
        'session_token': 'token',
        'is_verified': False
    })