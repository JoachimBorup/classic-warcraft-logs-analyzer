import os
import requests
from dotenv import load_dotenv
from requests_oauthlib import OAuth2Session

from models import Report, ReportRequest

load_dotenv()

PRIVATE_CLIENT_ID = os.getenv('WCL_PRIVATE_CLIENT_ID')
PRIVATE_CLIENT_SECRET = os.getenv('WCL_PRIVATE_CLIENT_SECRET')
base_url = 'https://www.warcraftlogs.com/api/v2/user'


def get_access_token() -> str:
    oauth = OAuth2Session(PRIVATE_CLIENT_ID, redirect_uri='https://localhost:5000/callback')
    authorization_url, _ = oauth.authorization_url('https://www.warcraftlogs.com/oauth/authorize')

    print('Please visit this URL to authorize your application:', authorization_url)
    authorization_response = input('Enter the full callback URL: ')

    _token = oauth.fetch_token('https://www.warcraftlogs.com/oauth/token',
                              authorization_response=authorization_response,
                              client_secret=PRIVATE_CLIENT_SECRET)
    return _token['access_token']


def get_report(request: ReportRequest) -> Report:
    access_token = get_access_token()

    query = """
    query ($code: String!) {
      reportData {
        report(code: $code) {
          code
          endTime
        }
      }
    }
    """

    data = {
        'query': query,
        'variables': {
            'code': request.code
        }
    }

    with requests.session() as session:
        session.headers = {'Authorization': f'Bearer {access_token}'}
        response = session.get(base_url, json=data)
        

        print(f"Status is {response.status_code}")
        print(response.url)
        print(response.json())

    return None