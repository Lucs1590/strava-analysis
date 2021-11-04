import requests
from pandas.io.json import json_normalize
import json


def get_data(url, access_token, numb_item_page, page):
    response = requests.get('{0}?access_token={1}&per_page={2}&page={3}'.format(
        url, access_token, numb_item_page, page))
    response = response.json()
    return response


def get_credentials():
    with open('strava_tokens.json') as json_file:
        strava_tokens = json.load(json_file)
    return strava_tokens['access_token']


def save_csv(response):
    df = json_normalize(response)
    df.to_csv('data/strava_activities_all_fields_pag{}.csv'.format(page))


url = "https://www.strava.com/api/v3/activities"
access_token = get_credentials()

page = 1
while True:
    response = get_data(url, access_token, 200, page)
    if not response:
        break
    save_csv(response)
    page += 1
