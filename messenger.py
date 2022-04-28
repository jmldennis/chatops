import json
import requests


class Messenger():
    def __init__(self, api_key):
        self.base_url = 'https://api.ciscospark.com/v1/'
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept":"application/json",
            "Content-Type": "application/json"
        }
        self.bot_id = requests.get(f'{self.base_url}/people/me', headers=self.headers).json().get('id')
        
    def get_message(self, message_id):
        """ Retrieve a specific message, specified by message_id """
        print(f'MESSAGE ID: {message_id}')
        received_message_url = f'{self.base_url}/messages/{message_id}'
        self.message_text = requests.get(received_message_url, headers=self.headers).json().get('text')


    def post_message_room_id(self, room_id, message):
        """ Post message to a Webex Teams space, specified by room_id """
        data = {
            "roomId": room_id,
            "text": message,
            }
        post_message_url = f'{self.base_url}/messages'
        self.post_message = requests.post(post_message_url,headers=self.headers,data=json.dumps(data))
        #print(json.dumps(post_message.json(),indent=4))

    def post_message_email(self, email, message):
        """ Post message to a Webex Teams space, specified by email """
        data = {
            "toPersonEmail": email,
            "text": message,
            }
        post_message_url = f'{self.base_url}/messages'
        self.post_message = requests.post(post_message_url,headers=self.headers,data=json.dumps(data))
        #print(json.dumps(post_message.json(),indent=4))

    def create_webhook(self, url):
        webhooks_api = 'https://webexapis.com/v1/webhooks'

        data = { 
            "name": "Webhook to ChatBot",
            "resource": "all",
            "event": "all",
            "targetUrl": url
        }
        self.create_webhook_response = requests.post(webhooks_api, headers=self.headers, data=json.dumps(data))


    def delete_webhook(self, webhookId):
        webhooks_api = f'https://webexapis.com/v1/webhooks/{webhookId}'
       
        self.delete_webhook_response = requests.delete(webhooks_api,headers=self.headers, data=json.dumps(data))