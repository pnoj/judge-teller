import requests
from flask import Flask, request
import k8s

app = Flask(__name__)

@app.route('/')
def status():
    teller_status = {
        "status": config['status'],
    }
    return teller_status

@app.route('/run', methods=["POST"])
def run():
    pass

@app.before_first_request
def setup():
    global config
    config = dict()
    config["status"] = "ready"
