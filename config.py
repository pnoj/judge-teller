runtimes = {
    'python3': {
        'name': 'Python3',
        'docker_image': 'pnoj/runtime-python3',
        'runtime': 'python3 3.8',
    },
    'java8': {
        'name': 'Java 8',
        'docker_image': 'pnoj/runtime-java8',
        'runtime': 'javac 1.8',
    },
    'java11': {
        'name': 'Java 11',
        'docker_image': 'pnoj/runtime-java11',
        'runtime': 'javac 11',
    },
    'cpp17': {
        'name': 'C++17',
        'docker_image': 'pnoj/runtime-cpp17',
        'runtime': 'gcc 9.3.0',
    },
    'c18': {
        'name': 'C18',
        'docker_image': 'pnoj/runtime-c18',
        'runtime': 'gcc 9.3.0',
    },
    'brainfuck': {
        'name': 'Brainfuck',
        'docker_image': 'pnoj/runtime-brainfuck',
        'runtime': 'BFCC by TheoP',
    },
    'text': {
        'name': 'Text',
        'docker_image': 'pnoj/runtime-text',
        'runtime': 'cat 8.3',
    },
    'haskell': {
        'name': 'Haskell',
        'docker_image': 'pnoj/runtime-haskell',
        'runtime': 'ghc 8.8.3',
    },
    'scratch': {
        'name': 'Scratch',
        'docker_image': 'pnoj/runtime-scratch',
        'runtime': 'scrape 20.06.5',
    },
}

token = '<your_auth_token_here>'

config = {
    "runtimes": runtimes,
    "token": token,
}
