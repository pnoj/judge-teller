import requests
import flask
import k8s
import config
import uuid
import redis

app = flask.Flask(__name__)

def authenticate(request):
    token = request.form.get("token")
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
    lang = flask.request.form.get("lang")
    if lang not in state["config"]["executors"]:
        flask.abort(404)
    image = state["config"]["executors"][lang]["image"]
    executor_id = uuid.uuid4().hex
    pod_name = f"executor-{executor_id}"
    api_response = k8s.create_pod(pod_name, image, ports=[8000], resources={"cpu": state["config"]["cpu"]}, privileged=True)
    pod_ip = api_response.status.pod_ip
    rds = state["redis"]
    rds.set(f'executor-{executor_id}-ip', pod_ip)
    return executor_id
    
@app.route('/create/task', methods=["POST"])
def create_task():
    authenticate(flask.request)

@app.route('/delete/executor', methods=["POST"])
def delete_executor():
    authenticate(flask.request)
    executor_id = flask.request.form.get("executor-id")
    pod_name = f"executor-{executor_id}"
    k8s.delete_pod(pod_name)

    return executor_id

@app.route('/send/submission', methods=["POST"])
def send_submission():
    authenticate(flask.request)
    executor_id = flask.request.form.get("executor-id")
    rds = state["redis"]
    pod_ip = rds.get(f'executor-{executor_id}-ip')
    if 'submission' in flask.request.files:
        response = requests.post(f'http://{pod_ip}:8000/compile', files=flask.request.files)
        response.raise_for_status()
    else:
        flask.abort(400)
    return response.text

@app.route('/send/testcase', methods=["POST"])
def send_testcase():
    executor_id = flask.request.form.get("executor-id")
    rds = state["redis"]
    pod_ip = rds.get(f'executor-{executor_id}-ip')
    response = requests.post(f'http://{pod_ip}:8000/run', data=flask.request.form)
    response.raise_for_status()
    return response.text

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

@app.route('/get/executors', methods=["GET"])
def get_runtimes():
    return state["config"]["executors"]

@app.before_first_request
def setup():
    global state
    state = dict()
    state["status"] = "ready"
    state["config"] = config.config
    state["redis"] = redis.Redis.from_url(state["config"]["redis_url"], decode_responses=True)
