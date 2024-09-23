import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

token = os.getenv("API_TOKEN")
print(token)
tag = os.getenv("TAG")
print(tag)

# url = f"https://api.clashofclans.com/v1/players/{tag}"
# headers = {
#     'Authorization': f'Bearer {token}',
#     'Content-Type': 'application.json'
# }

# response = requests.get(url, headers=headers)
# # print(type(response))
# response_json = response.json()
# new = (json.dumps(response_json, indent=4))
# print(new)


# with open('player.csv', 'a', newline="") as file:
#     write = csv.writer(file)
#     file.write(new)
