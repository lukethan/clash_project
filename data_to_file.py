import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime
import logging

load_dotenv

token = os.getenv("API_TOKEN")

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application.json'
}
response = requests.get('https://api.clashofclans.com/v1/clans/%232GLLPQYLL/currentwar', headers=headers)

response = response.json()

logging.basicConfig(filename='data_to_file.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

dt = datetime.now()

if response['state'] == 'inWar':
    with open(f'war{dt.month}.{dt.day}.{dt.year}time{dt.hour}.{dt.minute}.json', "a") as json_file:
        json.dump(response, json_file, indent=4)
elif response['state'] == 'warEnded':
    end_time = response['endTime'][0:8]
    file_name = f'war{end_time}.json'
    if os.path.exists(file_name):
        logging.info(f'{file_name} already exists')
    else:
        with open(file_name, "a") as json_file:
            json.dump(response, json_file, indent=4)
        logging.info(f"{file_name} created and response recorded at {dt}")