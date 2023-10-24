import requests

from models import Report, ReportRequest
from utils import get_env_var

base_url = 'https://www.warcraftlogs.com/api/v2/user'

def get_report(request: ReportRequest) -> Report:
    access_token = get_env_var('WCL_ACCESS_TOKEN')

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
