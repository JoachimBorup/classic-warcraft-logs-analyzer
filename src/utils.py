import os
from typing import Optional

import dotenv
from requests_oauthlib import OAuth2Session


def get_env_var(key: str) -> str:
    """Gets an environment variable, raising an exception if it is not set."""
    dotenv.load_dotenv()
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Missing environment variable: {key}")
    return value


def get_access_token(client_id: Optional[str] = None, client_secret: Optional[str] = None) -> str:
    """Creates an OAuth2 session and retrieves an access token for the Warcraft Logs API.
    Will prompt the user to visit a URL and enter the callback URL.
    See https://classic.warcraftlogs.com/api/docs for more information.

    :param client_id: The client ID for the Warcraft Logs API. If None,
           the `WCL_CLIENT_ID` environment variable will be used instead.
    :param client_secret: The client secret for the Warcraft Logs API. If None,
           the `WCL_CLIENT_SECRET` environment variable will be used instead.
    :return: The access token.
    """

    if client_id is None:
        client_id = get_env_var('WCL_CLIENT_ID')
    if client_secret is None:
        client_secret = get_env_var('WCL_CLIENT_SECRET')

    oauth = OAuth2Session(client_id, redirect_uri='https://localhost:5000/callback')
    authorization_url, _ = oauth.authorization_url('https://www.warcraftlogs.com/oauth/authorize')

    print('Please visit this URL to authorize your application:', authorization_url)
    authorization_response = input('Enter the full callback URL: ')

    token_dict = oauth.fetch_token('https://www.warcraftlogs.com/oauth/token',
                                   authorization_response=authorization_response,
                                   client_secret=client_secret)
    return token_dict['access_token']
