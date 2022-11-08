import os
import json
import glob
import time
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def main():
    url = "https://www.strava.com/api/v3/activities"
    access_token = get_credentials()

    page = 1
    print('Getting data from Strava')
    while True:
        response = get_data(url, access_token, 200, page)
        if 'message' in response.columns:
            raise Exception('Authorization Error')
        if response.empty:
            break
        save_csv(response, f'data/strava_activities_page_{page}.csv')
        page += 1
    merge_files('data/', 'result/strava_all_activities.csv')
    print('Done Successfully')

def get_credentials():
    with open('strava_tokens.json', encoding='utf-8') as json_file:
        strava_tokens = json.load(json_file)

    if 'expires_at' not in strava_tokens.keys() or strava_tokens['expires_at'] < time.time():
        strava_tokens = refresh_credentials(strava_tokens)

    return strava_tokens['access_token']


def refresh_credentials(strava_tokens):
    response = requests.post(
        url='https://www.strava.com/oauth/token',
        data={
            'client_id': int(os.environ.get('client_id')),
            'client_secret': os.environ.get('client_secret'),
            'grant_type': 'refresh_token',
            'refresh_token': strava_tokens['refresh_token']
        }
    )

    strava_tokens = response.json()

    with open('strava_tokens.json', 'w', encoding='utf-8') as outfile:
        json.dump(strava_tokens, outfile)

    with open('strava_tokens.json', encoding='utf-8') as check:
        data = json.load(check)

    return data


def get_data(url, access_token, numb_item_page, page):
    print(f'Getting data from page {page}')
    response = requests.get(
        f'{url}?access_token={access_token}&per_page={numb_item_page}&page={page}'
    )
    response = response.json()
    dataframe = pd.json_normalize(response)
    return dataframe


def save_csv(dataframe, filename):
    print(f'Saving {filename}')
    dataframe.to_csv(filename)


def merge_files(path, filename):
    print('Merging files')
    csv_files = [pd.read_csv(_file)
                 for _file in glob.glob(os.path.join(path, "*.csv"))]
    final_df = csv_files.pop(len(csv_files)-1)
    final_df = final_df.append(csv_files)
    save_csv(final_df, filename)


if __name__ == '__main__':
    main()
