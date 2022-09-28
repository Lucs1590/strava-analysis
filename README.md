# strava-analysis
Using strava to do personal analyses and to practice data scientist skills.

# Common steps sequence

1. Update the strava code on environment.
2. Run the `create_token.py` script to create a token.
3. Run the `get_activities.py` script to get activities.

# Common problems
The most commom problem is related to the token. If you have a problem with the token, you will need to update this token.
1. Open https://www.strava.com/settings/api and click on `Generate new client secret`.
2. Update the `client_secret` on the `.env` file.
3. You will need a new strava code, so access [this link](http://localhost/exchange_token?state=&code=[CLIENT_ID]&scope=read,activity:read_all,profile:read_all) replacing CLIENT_ID by your client_id.
4. Update the `strava_code` on the `.env` file the code generated on the link.