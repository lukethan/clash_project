import os
from dotenv import load_dotenv
import requests
import pandas as pd
import json

load_dotenv

token = os.getenv("API_TOKEN")

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application.json'
}
response = requests.get('https://api.clashofclans.com/v1/clans/%232GLLPQYLL/currentwar', headers=headers)
response = response.json()
print(json.dumps(response, indent=2))


# df = pd.json_normalize(response, 
#                        record_path=['clan', 'members'], 
#                        meta=[
#                            'state', 
#                            'teamSize', 
#                            'attacksPerMember', 
#                            'battleModifier', 
#                            'preparationStartTime', 
#                            'startTime', 
#                            'endTime', 
#                            ['clan', 'tag'], 
#                            ['clan', 'name'], 
#                            ['clan', 'badgeUrls', 'small'], 
#                            ['clan', 'badgeUrls', 'large'], 
#                            ['clan', 'badgeUrls', 'medium'], 
#                            ['clan', 'clanLevel'], 
#                            ['clan', 'attacks'], 
#                            ['clan', 'stars'], 
#                            ['clan', 'destructionPercentage']
#                        ], 
#                        record_prefix='member_')

# print(df)