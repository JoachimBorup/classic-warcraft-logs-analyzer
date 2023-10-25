import requests

from src.models import Fight, Report, ReportRequest
from src.utils import get_env_var

API_URL = 'https://www.warcraftlogs.com/api/v2/user'


def query_graphql(query: str, variables: dict) -> dict:
    """Queries the Warcraft Logs API using GraphQL.

    Requires the `WCL_ACCESS_TOKEN` environment variable to be set.

    :param query: The GraphQL query to execute.
    :param variables: The variables to pass to the query.
    """

    access_token = get_env_var('WCL_ACCESS_TOKEN')
    with requests.session() as session:
        session.headers = {'Authorization': f'Bearer {access_token}'}

        response = session.get(API_URL, json={'query': query, 'variables': variables})
        if response.status_code != 200:
            raise ValueError(f"Error {response.status_code} retrieving report: {response.reason}")

        json = response.json()
        if json.get('errors') is not None:
            raise ValueError(f"Error retrieving report: {json['errors']}")

        return json['data']


def get_report(request: ReportRequest) -> Report:
    query = """
        query ($code: String!, $encounterID: Int, $fightIDs: [Int], $killType: KillType) {
            reportData {
                report(code: $code) {
                    fights(encounterID: $encounterID, fightIDs: $fightIDs, killType: $killType) {
                        encounterID
                        name
                        kill
                        difficulty
                        bossPercentage
                        averageItemLevel
                    }
                }
            }
        }
    """
    variables = {
        'code': request.code,
        'encounterID': request.encounter,
        'fightIDs': request.fights,
        'killType': request.type
    }

    data = query_graphql(query, variables)
    json_fights = data['reportData']['report']['fights']

    fights = [Fight(
        name=json_fight['name'],
        encounter_id=json_fight['encounterID'],
        kill=json_fight['kill'],
        difficulty=json_fight['difficulty'],
        boss_percentage=json_fight['bossPercentage'],
        average_item_level=json_fight['averageItemLevel']
    ) for json_fight in json_fights]

    return Report(fights)
