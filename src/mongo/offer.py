import os
from dotenv import load_dotenv
from bson import ObjectId

load_dotenv()

import pymongo

client = pymongo.MongoClient(os.getenv('MONGODB_URL'))

# MongoDB connection setup from https://www.mongodb.com/blog/post/getting-started-with-python-and-mongodb
db = client.VisuOL
col = db['offers']


# Adds an offer to the offer table
# Offers are a dictionary with all the standard things found in typical offer letters
def add_offer(offer):
    col.insert_one(offer)
    return None


# Retrieves a specific offer from the table
def get_offer(offer_id):
    assert offer_id is not None, "no id given!"

    return col.find_one({'_id': ObjectId(offer_id)})


# Retrieves all the offers that a user has
# Takes in the id of a user
def get_offers(user_id):
    assert user_id is not None, "no id given!"

    return col.find({'user_id': user_id})

# Updates a specific offer
def update_offer(offer_id, body):
    return col.update_one({'_id': ObjectId(offer_id)}, body)


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
