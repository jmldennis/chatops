import messenger
import yaml
import json
import requests
from flask import Flask, request, json

#Get Webex API KEY from YAML File
try:
    with open("./config.yml", 'r') as yamlfile:
        config = yaml.load(yamlfile, Loader=yaml.FullLoader)
    print("Success: Loaded YAML config file")
except Exception:
    print("Yaml file incomplete or invalid format")
    raise

app = Flask(__name__)
port = 5005

@app.route('/', methods=['GET', 'POST'])
def index():
    """Receive a notification from Webex Teams and handle it"""
    if request.method == 'GET':
        return f'Request received on local port {port}'

message = messenger.Messenger(config["webex_api_key"])

message.post_message_email("jodennis@cisco.com","hi")









if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port)