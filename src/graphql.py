import requests

from src.models import DeathEvent, Fight, Report, ReportRequest
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
    fights = [get_fight(request, fight_id) for fight_id in request.fight_ids]
    return Report(fights=fights)


def get_fight(request: ReportRequest, fight_id: int) -> Fight:
    query = """
        query ($code: String!, $encounterID: Int, $fightIDs: [Int], $killType: KillType) {
            reportData {
                report(code: $code) {
                    fights(encounterID: $encounterID, fightIDs: $fightIDs, killType: $killType) {
                        id
                        name
                        encounterID
                        startTime
                        endTime
                        kill
                        difficulty
                        bossPercentage
                        averageItemLevel
                    }
                    table(encounterID: $encounterID, fightIDs: $fightIDs, killType: $killType)
                }
            }
        }
    """
    variables = {
        'code': request.code,
        'encounterID': request.encounter_id,
        'fightIDs': [fight_id],
        'killType': request.kill_type
    }

    report = query_graphql(query, variables)['reportData']['report']
    death_events = [DeathEvent(death) for death in report['table']['data']['deathEvents']]
    return Fight(report['fights'][0], death_events)
