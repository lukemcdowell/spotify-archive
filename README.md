# spotify-archive

Script to make an archive of my top Spotify tracks each month.

Runs monthly on AWS Lambda to create a new playlist containing my top songs from the previous month. Integrates with Spotify using the Authorization Code flow feature of the Spotipy library. Emails me with a link to the new playlist.

![image](https://github.com/user-attachments/assets/f641e409-2745-433c-89a4-ea809441f31a)

## Useful Links

- https://spotipy.readthedocs.io/en/2.24.0/#
- https://developer.spotify.com/documentation/web-api/tutorials/code-flow
- https://docs.aws.amazon.com/lambda/latest/dg/configuration-function-zip.html
- https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-run-lambda-schedule.html

## Running on Lambda

To deploy and run on AWS Lambda, you first need to run the app locally to authenticate via Spotify, and generate a `.cache` file containing your authentication and refresh tokens.

### 1. Run the App Locally
This is required in order to authenticate via Spotify and generate your authentication and refresh tokens. 

- Set up your environment variables locally and install dependencies
- Run `python3 main.py`
   this will prompt you to log in to Spotify via your web broswer.
   - a playlist called "Test Playlist" will be generated in your Spotify account.
   - your tokens will be stored in a `.cache` file. This file should be packaged and uploaded to lambda.

### 2. Set Up Environment Variables

The Lambda function requires specific environment variables to run, including:

- `ALERT_EMAIL_ADDRESS`: Email address from which alerts will be sent.
- `ALERT_EMAIL_PASSWORD`: Password for alert email account.
- `EMAIL_ADDRESS`: Recipient email address.
- `SPOTIPY_CLIENT_ID`: Client ID for the Spotify application.
- `SPOTIPY_CLIENT_SECRET`: Client secret for the Spotify application.
- `SPOTIPY_REDIRECT_URI`: Redirect URI of the Spotify application for initial authentication.

Set these in the AWS Lambda environment configuration under **Configuration > Environment variables**.

### 3. Package Your Application

To upload the function to AWS Lambda, package your Python code and dependencies:

**Install Dependencies**  
   It is recommended to create a copy of your project directory first, to keep all of the installed dependencies separate from your git project. Use `pip` to install dependencies from `requirements.txt` into the root directory of your project:

   ```bash
   pip3 install -r requirements.txt -t .
   ```


### 4. Zip Entire Directory

Once all necessary files and dependencies are in the root directory, you can zip everything:

```bash
zip -r lambda_function.zip ./*
```

### 5. Upload Deployment Package to Lambda

## Running Locally:
- Set up your environment variables and install dependencies (as described above)
- Run `python3 main.py` 
   - this will prompt you to log in to Spotify via your web broswer. 
   - a playlist called "Test Playlist" will be generated in your Spotify account.
   - your tokens will be stored in a `.cache` file. This file should be packaged and uploaded to lambda.
