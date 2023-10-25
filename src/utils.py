import os

import dotenv
from requests_oauthlib import OAuth2Session


def get_env_var(key: str) -> str:
    """Gets an environment variable, raising an exception if it is not set."""
    dotenv.load_dotenv()
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Missing environment variable: {key}")
    return value


def get_access_token() -> str:
    """Creates an OAuth2 session and retrieves an access token for the Warcraft Logs API.

    Requires the `WCL_CLIENT_ID` and `WCL_CLIENT_SECRET` environment variables to be set.
    See https://classic.warcraftlogs.com/api/docs for more information.
    """

    client_id = get_env_var('WCL_CLIENT_ID')
    client_secret = get_env_var('WCL_CLIENT_SECRET')

    oauth = OAuth2Session(client_id, redirect_uri='https://localhost:5000/callback')
    authorization_url, _ = oauth.authorization_url('https://www.warcraftlogs.com/oauth/authorize')

    print('Please visit this URL to authorize your application:', authorization_url)
    authorization_response = input('Enter the full callback URL: ')

    token_dict = oauth.fetch_token('https://www.warcraftlogs.com/oauth/token',
                                   authorization_response=authorization_response,
                                   client_secret=client_secret)
    return token_dict['access_token']
