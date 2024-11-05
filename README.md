# spotify-archive

Script to make an archive of my top Spotify tracks each month.

Runs monthly on AWS Lambda to create a new playlist containing my top songs from the previous month. Integrates with Spotify using the Authorization Code flow feature of the Spotipy library. Emails me with a link to the new playlist.

## Useful Links

- https://spotipy.readthedocs.io/en/2.24.0/#
- https://developer.spotify.com/documentation/web-api/tutorials/code-flow
- https://docs.aws.amazon.com/lambda/latest/dg/configuration-function-zip.html
- https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-run-lambda-schedule.html

## Running on Lambda

To run on AWS Lambda, follow these steps:

### 1. Set Up Environment Variables

The Lambda function requires specific environment variables to run, including:

- `ALERT_EMAIL_ADDRESS`: Email address from which alerts will be sent.
- `ALERT_EMAIL_PASSWORD`: Password for alert email account.
- `EMAIL_ADDRESS`: Recipient email address.
- `SPOTIPY_CLIENT_ID`: Client ID for the Spotify application.
- `SPOTIPY_CLIENT_SECRET`: Client secret for the Spotify application.
- `SPOTIPY_REDIRECT_URI`: Redirect URI of the Spotify application for initial authentication.

Set these in the AWS Lambda environment configuration under **Configuration > Environment variables**.

### 2. Package Your Application

To upload the function to AWS Lambda, package your Python code and dependencies:

1. **Install Dependencies**  
   Use `pip` to install dependencies from `requirements.txt` into the root directory of your project:

   ```bash
   pip install -r requirements.txt -t .
   ```

### 3. Zip Entire Directory

Once all necessary files and dependencies are in the root directory, you can zip everything:

```bash
zip -r lambda_function.zip ./*
```

### 4. Upload Deployment Package to Lambda
