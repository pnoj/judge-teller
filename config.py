import os

executors = {
    'python3': {
        'name': 'Python3',
        'image': 'pnoj/executor-python3:sha-3b90c3f',
        'runtime': 'python3 3.8',
    },
    'java8': {
        'name': 'Java 8',
        'image': 'pnoj/executor-java8:sha-3b90c3f',
        'runtime': 'javac 1.8',
    },
    'java11': {
        'name': 'Java 11',
        'image': 'pnoj/executor-java11:sha-3b90c3f',
        'runtime': 'javac 11',
    },
    'cpp17': {
        'name': 'C++17',
        'image': 'pnoj/executor-cpp17:sha-3b90c3f',
        'runtime': 'gcc 9.3.0',
    },
    'c18': {
        'name': 'C18',
        'image': 'pnoj/executor-c18:sha-3b90c3f',
        'runtime': 'gcc 9.3.0',
    },
    'brainfuck': {
        'name': 'Brainfuck',
        'image': 'pnoj/executor-brainfuck:sha-3b90c3f',
        'runtime': 'BFCC by TheoP',
    },
    'text': {
        'name': 'Text',
        'image': 'pnoj/executor-text:sha-3b90c3f',
        'runtime': 'cat 8.3',
    },
    'haskell': {
        'name': 'Haskell',
        'image': 'pnoj/executor-haskell:sha-3b90c3f',
        'runtime': 'ghc 8.8.3',
    },
    'scratch': {
        'name': 'Scratch',
        'image': 'pnoj/executor-scratch:sha-3b90c3f',
        'runtime': 'scrape 20.06.5',
    },
}

token = '<your_auth_token_here>'

redis_url = "redis://localhost"

cpu = "700m"

tasker_image = "pnoj/tasker:sha-cee666e"

pod_ip = os.environ['POD_IP']

isolate_init_interval = 1

executor_contact_max_retry = 1000

executor_contact_retry_delay = 0.25

config = {
    "executors": executors,
    "token": token,
    "cpu": cpu,
    "redis_url": redis_url,
    "tasker_image": tasker_image,
    "pod_ip": pod_ip,
    "isolate_init_interval": isolate_init_interval,
    "executor_contact_max_retry": executor_contact_max_retry,
    "executor_contact_retry_delay": executor_contact_retry_delay,
}
