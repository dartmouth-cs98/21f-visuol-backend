import os

#Credit to https://pythonbasics.org/flask-tutorial-hello-world/ prints hello world
from flask import Flask
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# MongoDB connection setup
client = MongoClient(os.getenv('MONGO_URL'))
db=client.admin
# Issue the serverStatus command and print the results
print(db.command("serverStatus"))

# Flask setup
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

app.run(host='0.0.0.0', port=81)# Flask setup
app = Flask(__name__)
