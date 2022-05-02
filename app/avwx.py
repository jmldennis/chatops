import requests

class Avwx():
    def __init__(self,token):
        self.headers = {
                        "Authorization":f"Bearer {token}",
                        "Content-Type":"application/json"
                    }

    def get_weather(self,airport_code):
        self.airport_code = airport_code
        self.url = "https://avwx.rest/api/taf/" + self.airport_code

        try:
            self.response = requests.get(self.url, headers = self.headers)
            if self.response.status_code == 200:
                self.response_json = self.response.json()
                self.METAR = self.response_json["raw"]
                self.flight_rules = self.response_json["forecast"][0]["flight_rules"]
            
        except:
            print("Error getting weather for " + self.airport_code)