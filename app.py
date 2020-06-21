import requests
import flask
import k8s
import config

app = flask.Flask(__name__)

def authenticate(request):
    token = request.form.get("token")
    print(token, state["config"]["token"])
    if token != state["config"]["token"]:
        flask.abort(400)

@app.route('/')
def status():
    teller_status = {
        "status": state['status'],
    }
    return teller_status


@app.route('/create/executor', methods=["POST"])
def create_executor():
    authenticate(flask.request)
    
@app.route('/create/task', methods=["POST"])
def create_task():
    authenticate(flask.request)

@app.route('/send/testcase', methods=["POST"])
def send_testcase():
    authenticate(flask.request)

@app.route('/send/passthrough', methods=["POST"])
def send_passthrough():
    authenticate(flask.request)

@app.route('/send/callback', methods=["POST"])
def send_callback():
    authenticate(flask.request)

@app.route('/get/task', methods=["GET"])
def get_task():
    authenticate(flask.request)

@app.route('/get/runtimes', methods=["GET"])
def get_runtimes():
    return state["config"]["runtimes"]

@app.before_first_request
def setup():
    global state
    state = dict()
    state["status"] = "ready"
    state["config"] = config.config
