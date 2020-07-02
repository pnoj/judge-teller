import requests
import flask
import k8s
import config
import uuid
import redis
import time

app = flask.Flask(__name__)

def authenticate(request):
    token = request.form.get("token")
    if token != state["config"]["token"]:
        flask.abort(401)

def get_box_id():
    return int(time.time()*(1/state["config"]["isolate_init_interval"])%1000)

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
    api_response = k8s.create_pod(pod_name, image, env={"ISOLATE_BOX_ID": str(get_box_id())}, ports=[8000], resources={"cpu": state["config"]["cpu"]}, privileged=True)
    pod_ip = api_response.status.pod_ip
    rds = state["redis"]
    rds.set(f'executor-{executor_id}-ip', pod_ip)

    for i in range(0, state["config"]["executor_contact_max_retry"]):
        try:
            resp = requests.get(f"http://{pod_ip}:8000")
            resp_json = resp.json()
            assert resp_json["status"] == "ready"
            break
        except requests.exceptions.ConnectionError:
            time.sleep(state["config"]["executor_contact_retry_delay"])
    
    return executor_id
    
@app.route('/create/task', methods=["POST"])
def create_task():
    authenticate(flask.request)

    callback_url = flask.request.form.get("callback_url")
    passthrough_url = flask.request.form.get("passthrough_url")
    submission_file_url = flask.request.form.get("submission_file_url")
    problem_file_url = flask.request.form.get("problem_file_url")
    language = flask.request.form.get("language")

    image = state["config"]["tasker_image"]
    tasker_id = uuid.uuid4().hex
    pod_name = f"tasker-{tasker_id}"
    task_fetch_url = f'http://{state["config"]["pod_ip"]}:8000/get/task/{tasker_id}'

    rds = state["redis"]
    rds.set(f'tasker-{tasker_id}-callback', callback_url)
    rds.set(f'tasker-{tasker_id}-passthrough', passthrough_url)
    rds.set(f'tasker-{tasker_id}-submission', submission_file_url)
    rds.set(f'tasker-{tasker_id}-problem', problem_file_url)
    rds.set(f'tasker-{tasker_id}-lang', language)

    api_response = k8s.create_pod(pod_name, image, env={"ISOLATE_BOX_ID": str(get_box_id())}, args=["--task_fetch_url", task_fetch_url], privileged=True)

    return tasker_id

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
    authenticate(flask.request)
    executor_id = flask.request.form.get("executor-id")
    rds = state["redis"]
    pod_ip = rds.get(f'executor-{executor_id}-ip')
    response = requests.post(f'http://{pod_ip}:8000/run', data=flask.request.form)
    response.raise_for_status()
    return response.text

@app.route('/send/passthrough/<tasker_id>', methods=["POST"])
def send_passthrough(tasker_id):
    rds = state["redis"]
    passthrough_url = rds.get(f'tasker-{tasker_id}-passthrough')
    response = requests.post(passthrough_url, json=flask.request.json)
    response.raise_for_status()
    return response.text

@app.route('/send/callback/<tasker_id>', methods=["POST"])
def send_callback(tasker_id):
    rds = state["redis"]
    callback_url = rds.get(f'tasker-{tasker_id}-callback')
    response = requests.post(callback_url, json=flask.request.json)
    
    pod_name = f"tasker-{tasker_id}"
    k8s.delete_pod(pod_name)

    return response.text

@app.route('/get/task/<tasker_id>', methods=["GET"])
def get_task(tasker_id):
    rds = state["redis"]
    submission_file_url = rds.get(f'tasker-{tasker_id}-submission')
    problem_file_url = rds.get(f'tasker-{tasker_id}-problem')
    language = rds.get(f'tasker-{tasker_id}-lang')

    data = {
        'callback_url': f'http://{state["config"]["pod_ip"]}:8000/send/callback/{tasker_id}',
        'passthrough_url': f'http://{state["config"]["pod_ip"]}:8000/send/passthrough/{tasker_id}',
        'submission_file_url': submission_file_url,
        'problem_file_url': problem_file_url,
        'language': language,
        'teller_endpoint': f'http://{state["config"]["pod_ip"]}:8000',
        'token': state["config"]["token"],
    }

    return data

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
