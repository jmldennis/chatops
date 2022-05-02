import messenger
import yaml
import json
import requests
from flask import Flask, request, json
import ngrok
from time import sleep
import avwx

#Get Webex API KEY from YAML File
try:
    with open("./config.yml", 'r') as yamlfile:
        config = yaml.load(yamlfile, Loader=yaml.FullLoader)
    print("Success: Loaded YAML config file")
except Exception:
    print("Yaml file incomplete or invalid format")
    raise

#Initialize Flask App
app = Flask(__name__)
port = 5005

#Initialize WebEx Teams
msg = messenger.Messenger(config["webex_api_key"])

#Initialize Ngrok and Get URL's
sleep(10)
tunnel = ngrok.Ngrok("ngrok")
tunnel.get_ngrok_urls()

#Initialize avwx.rest API
airport_weather = avwx.Avwx(config["avwx_token"])

#Delete All Webhooks
msg.delete_all_webhooks()

#Create Webhook
msg.create_webhook(tunnel.url["https"])



@app.route('/', methods=['GET', 'POST'])
def index():
    """Receive a notification from Webex Teams and handle it"""
    if request.method == 'GET':
        return f'Request received on local port {port}'

    elif request.method == 'POST':
        if 'application/json' in request.headers.get('Content-Type'):
            # Notification payload, received from Webex Teams webhook
            data = request.get_json()

            # Loop prevention, ignore messages which were posted by bot itself.
            # The bot_id attribute is collected from the Webex Teams API
            # at object instatiation.
            if msg.bot_id == data.get('data').get('personId'):
                return 'Message from self ignored'
            else:
                # Print the notification payload, received from the webhook
                print(json.dumps(data,indent=4))

                # Collect the roomId from the notification,
                # so you know where to post the response
                # Set the msg object attribute.
                msg.room_id = data.get('data').get('roomId')
                
                # Collect the message id from the notification, 
                # so you can fetch the message content
                message_id = data.get('data').get('id')

                # Get the contents of the received message. 
                msg.get_message(message_id)

                # If message starts with '/server', relay it to the web server.
                # If not, just post a confirmation that a message was received.
                if msg.message_text.startswith('-help'):
	                # Default action is to list send the 'status' command. 
                    msg.reply = "Simply type a 4 char airport code to see the local weather info"
                    msg.post_message_room_id(msg.room_id, msg.reply)
                    
                elif len(msg.message_text) == 4:
                    airport_weather.get_weather(msg.message_text)
                    if airport_weather.response.status_code == 200:
                        msg.reply = airport_weather.METAR
                        msg.post_message_room_id(msg.room_id, msg.reply)
                    elif airport_weather.response.status_code == 204:
                        msg.reply = "Sorry that Airport is not in the API Database"
                        msg.post_message_room_id(msg.room_id, msg.reply)
                    else:
                        msg.reply = "Unknown Error..."
                        msg.post_message_room_id(msg.room_id, msg.reply)
                
                else:
                    msg.reply = "Simply type a 4 char airport code to see the local weather info"
                    msg.post_message_room_id(msg.room_id, msg.reply)

                return data
        else: 
            return ('Wrong data format', 400)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port)