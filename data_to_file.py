import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime

load_dotenv

token = os.getenv("API_TOKEN")

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application.json'
}
response = requests.get('https://api.clashofclans.com/v1/clans/%232GLLPQYLL/currentwar', headers=headers)

response = response.json()

dt = datetime.now()
if response['state'] == 'inWar':
    with open(f'war{dt.month}.{dt.day}.{dt.year}time{dt.hour}.{dt.minute}.json', "a") as json_file:
        json.dump(response, json_file, indent=4)
elif response['state'] == 'warEnded':
    with open(f'war{dt.month}.{dt.day}.{dt.year}ended.json', "a") as json_file:
        json.dump(response, json_file, indent=4)