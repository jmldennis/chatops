import messenger
import yaml
import json
import requests

#Get Webex API KEY from YAML File
try:
    with open("./config.yml", 'r') as yamlfile:
        config = yaml.load(yamlfile, Loader=yaml.FullLoader)
    print("Success: Loaded YAML config file")
except Exception:
    print("Yaml file incomplete or invalid format")
    raise


message = messenger.Messenger(config["webex_api_key"])

message.post_message_email("jodennis@cisco.com","hi")