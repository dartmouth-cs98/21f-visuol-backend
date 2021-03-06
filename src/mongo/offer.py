import os
from dotenv import load_dotenv
from bson import ObjectId
from .mongo_client import client

# MongoDB connection setup from https://www.mongodb.com/blog/post/getting-started-with-python-and-mongodb
db = client.VisuOL
col = db['offers']


# Adds an offer to the offer table
# Offers are a dictionary with all the standard things found in typical offer letters
def add_offer(offer):
    return str(col.insert_one(offer).inserted_id)


# Retrieves a specific offer from the table
def get_offer(offer_id):
    assert offer_id is not None, "no id given!"

    return col.find_one({'_id': ObjectId(offer_id)})


# Retrieves all the offers that a user has
# Takes in the id of a user
def get_offers(user):
    assert user is not None, "no user given!"

    return list(col.find({'user': user}))

# Updates a specific offer
def update_offer(offer_id, body):
    return col.update_one({'_id': ObjectId(offer_id)}, body)

# Deletes an offer from the database
def delete_offer(offer_id):
    assert offer_id is not None, "no id given!"

    col.delete_one({'_id': ObjectId(offer_id)})

# Shares an offer with another user
def share(offer_id, email):
    assert offer_id is not None, "no id given!"
    
    col.find_one_and_update({'_id': ObjectId(offer_id)},{ '$addToSet': {'shared_with': email}})
    
# Gets a list of all the offers that have been shared with the user
def shared_list(user):
    return list(col.find({ 'shared_with': user }))

def update(offer_id, base, bonus):
    assert offer_id is not None, "no id given!"
    
    if(len(base)):
        col.find_one_and_update({'_id': ObjectId(offer_id)},{ '$set': {'base': int(base)}})
    if(len(bonus)):
        col.find_one_and_update({'_id': ObjectId(offer_id)},{ '$set': {'bonus': int(bonus)}})

if __name__ == '__main__':
    add_offer({
        "company": "Google",
        "date": "02/07/21",
        "expiration": "02/21/21",
        "base": 100000,
        "bonus": 15000,
        "401k": 10.0,
        "PTO": 15
    })
