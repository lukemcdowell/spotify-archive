# spotify-archive

Script to make an archive of my top Spotify tracks each month.

Runs monthly on AWS Lambda to create a new playlist containing my top songs from the previous month. Integrates with Spotify using the Authorization Code flow feature of the Spotipy library. Emails me with a link to the new playlist.

![image](https://github.com/user-attachments/assets/f641e409-2745-433c-89a4-ea809441f31a)

## Useful Links

- https://spotipy.readthedocs.io/en/2.24.0/#
- https://developer.spotify.com/documentation/web-api/tutorials/code-flow
- https://docs.aws.amazon.com/lambda/latest/dg/configuration-function-zip.html
- https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-run-lambda-schedule.html
- https://docs.aws.amazon.com/cdk/v2/guide/work-with-cdk-python.html

## Running on Lambda

The Lambda function requires specific environment variables to run, including:

- `ALERT_EMAIL_ADDRESS`: Email address from which alerts will be sent.
- `ALERT_EMAIL_PASSWORD`: Password for alert email account.
- `EMAIL_ADDRESS`: Recipient email address.
- `SPOTIPY_CLIENT_ID`: Client ID for the Spotify application.
- `SPOTIPY_CLIENT_SECRET`: Client secret for the Spotify application.
- `SPOTIPY_REDIRECT_URI`: Redirect URI of the Spotify application for initial authentication.

You need to configure the required Spotify tokens by running `scripts/auth.py`.

The function is then deployed via CDK: `cdk deploy`.

## Running Locally:

- Set up your environment variables and install dependencies (as described above)
- Run `python3 main.py`
  - this will prompt you to log in to Spotify via your web broswer.
  - a playlist called "Test Playlist" will be generated in your Spotify account.
  - your tokens will be stored in a `.cache` file. This file should be packaged and uploaded to lambda.
