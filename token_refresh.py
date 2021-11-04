import requests
import json
import os

response = requests.post(
    url='https://www.strava.com/oauth/token',
    data={
        'client_id': int(os.environ.get('client_id')),
        'client_secret': os.environ.get('client_secret'),
        'code': os.environ.get('strava_code'),
        'grant_type': 'authorization_code'
    }
)

strava_tokens = response.json()

with open('strava_tokens.json', 'w') as outfile:
    json.dump(strava_tokens, outfile)

with open('strava_tokens.json') as check:
    data = json.load(check)

print(data)
