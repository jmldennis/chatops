#help manage a ngrok connection
import requests


class Ngrok():
    #Input default NGROK information
    def __init__(self,ipaddr="127.0.0.1"):
        self.ipaddr = ipaddr
        self.ngrok_console = f'http://{self.ipaddr}:4040/api/tunnels'
        self.url = {}

    #Get NGROK urls from localhost api
    #url is a dictionary with the urls assigned by type ex. http or https
    #urls is a list of urls
    def get_ngrok_urls(self):
        self.url["https"] = None
        self.url["http"] = None

        self.urls = []
        tunnels = requests.get(self.ngrok_console).json()['tunnels']
        for tunnel in tunnels:
            self.urls.append(tunnel['public_url'])

        for item in self.urls:
            if "https" in item:
                self.url["https"] = item
            elif "http" in item:
                self.url["http"] = item