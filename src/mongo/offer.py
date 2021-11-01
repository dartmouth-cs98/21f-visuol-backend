import os
from dotenv import load_dotenv
from bson import ObjectId

load_dotenv()

import pymongo

client = pymongo.MongoClient(os.getenv('MONGODB_URL'))

# MongoDB connection setup from https://www.mongodb.com/blog/post/getting-started-with-python-and-mongodb
db = client.VisuOL
col = db['offers']


# Adds a user to the user_authentication table
# Users are a dictionary with the following fields
# email (required), password (required), session_token (nullable), is_verified (required)
def add_offer(offer):
    col.insert_one(offer)
    return None


def get_offer(offer_id):
    assert offer_id is not None, "no id given!"

    return col.find_one({'_id': ObjectId(offer_id)})


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
