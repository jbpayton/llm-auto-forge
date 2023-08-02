import os
import json

def load_secrets(filename='secrets.json'):
    if not os.path.exists(filename):
        return
    with open(filename) as f:
        secrets = json.load(f)
        for key, value in secrets.items():
            os.environ[key] = str(value)