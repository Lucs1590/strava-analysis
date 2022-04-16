import os
import json
import glob
import time
import requests
import pandas as pd


def main():
    url = "https://www.strava.com/api/v3/activities"
    access_token = get_credentials()

    page = 1
    while True:
        response = get_data(url, access_token, 200, page)
        if 'message' in response.columns:
            raise Exception('Authorization Error')
        elif response.empty:
            break
        save_csv(response, 'data/strava_activities_page_{}.csv'.format(page))
        page += 1
    merge_files('data/', 'result/strava_all_activities.csv')


def get_credentials():
    with open('strava_tokens.json') as json_file:
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

    with open('strava_tokens.json', 'w') as outfile:
        json.dump(strava_tokens, outfile)

    with open('strava_tokens.json') as check:
        data = json.load(check)

    return data


def get_data(url, access_token, numb_item_page, page):
    print('Getting data from page {}'.format(page))
    response = requests.get('{0}?access_token={1}&per_page={2}&page={3}'.format(
        url, access_token, numb_item_page, page))
    response = response.json()
    dataframe = pd.json_normalize(response)
    return dataframe


def save_csv(dataframe, filename):
    print('Saving {}'.format(filename))
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
