from kubernetes import client, config

config.load_incluster_config()

v1core = client.CoreV1Api()
v1batch = client.BatchV1Api()

def create_job(job_name, image, args=[], env=dict(), ports={}, labels={"app": "teller"}, resources=None, deadline=None):
    env_list = []
    for i in env:
        env_list.append(client.V1EnvVar(name=i, value=env[i]))
    port_list = []
    for i in ports:
        port_list.append(client.V1ContainerPort(container_port=i, host_port=ports[i]))
    if resources != None:
        resource_req = client.V1ResourceRequirements(requests=resource_config, limits=resources)
    else:
        resource_req = None
    container = client.V1Container(
        name=f"{job_name}-container",
        image=image,
        args=args,
        env=env_list,
        ports=port_list,
        resources=resource_req,)
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels=labels),
        spec=client.V1PodSpec(restart_policy="Never", containers=[container]))
    spec = client.V1JobSpec(
        template=template,
	active_deadline_seconds=dealine,
        backoff_limit=4)
    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(name=f"{job_name}"),
        spec=spec)
    api_response = v1batch.create_namespaced_job(
        body=job,
        namespace="pnoj")
    return api_response
