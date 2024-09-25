import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime
import logging

# def main():

log_file_path = '/home/lukethan/projects/clash_project/data_to_file.log'

logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv('/home/lukethan/projects/clash_project/.env')

token = os.getenv("API_TOKEN")
if token is None:
    logging.error('API_TOKEN not found')

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}
response = requests.get('https://api.clashofclans.com/v1/clans/%232GLLPQYLL/currentwar', headers=headers)
logging.info(f"API response status code: {response.status_code}")

response = response.json()

dt = datetime.now()

progress_directory = '/home/lukethan/projects/clash_project/in_progress'
finished_directory = '/home/lukethan/projects/clash_project/finished'

# Create the absolute file path
file_path_p = os.path.join(progress_directory, f'war{dt.month}.{dt.day}.{dt.year}time{dt.hour}.{dt.minute}.json')

if response["state"] == 'inWar':
    with open(file_path_p, "a") as json_file:
        json.dump(response, json_file, indent=4)
        logging.info(f'Response recorded for inWar at {dt}')
elif response["state"] == 'warEnded':
    end_time = response['endTime'][0:8]
    file_name = f'war{end_time}.json'
    file_path = os.path.join(finished_directory, file_name)
    if os.path.exists(file_path):
        logging.info(f'{file_path} already exists')
    else:
        with open(file_path, "a") as json_file:
            json.dump(response, json_file, indent=4)
        logging.info(f"{file_path} created and response recorded at {dt}")
