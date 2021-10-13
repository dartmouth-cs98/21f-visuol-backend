#Credit to https://pythonbasics.org/flask-tutorial-hello-world/ prints hello world
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

app.run(host='0.0.0.0', port=81)