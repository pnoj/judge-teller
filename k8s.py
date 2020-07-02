from kubernetes import client, config
import time

config.load_incluster_config()

v1core = client.CoreV1Api()
v1batch = client.BatchV1Api()

def create_pod(pod_name, image, args=[], env=dict(), ports=[], labels={"app": "pnoj-teller"}, resources=None, privileged=False, namespace="pnoj", await_creation=True):
    env_list = []
    for i in env:
        env_list.append(client.V1EnvVar(name=i, value=env[i]))
    port_list = []
    for i in ports:
        port_list.append(client.V1ContainerPort(container_port=i))
    if resources != None:
        resource_req = client.V1ResourceRequirements(limits=resources)
    else:
        resource_req = None
    securityContext = client.V1SecurityContext(privileged=privileged)
    container = client.V1Container(
        name=f"{pod_name}-container",
        image=image,
        args=args,
        env=env_list,
        ports=port_list,
        resources=resource_req,
        security_context=securityContext)
    podspec = client.V1PodSpec(restart_policy="Never", containers=[container])
    pod = client.V1Pod(metadata=client.V1ObjectMeta(name=pod_name, labels=labels), spec=podspec)
    api_response = v1core.create_namespaced_pod(namespace=namespace, body=pod)

    if await_creation:
        while True:
            api_response = v1core.read_namespaced_pod(name=pod_name, namespace=namespace)
            if api_response.status.phase != 'Pending':
                break
            time.sleep(0.25)

    return api_response

def read_pod(pod_name, namespace="pnoj"):
    api_response = v1core.read_namespaced_pod(name=pod_name, namespace=namespace)
    return api_response

def delete_pod(pod_name, namespace="pnoj"):
    v1core.delete_namespaced_pod(name=pod_name, namespace=namespace)

config.load_incluster_config()
