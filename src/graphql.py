from multiprocessing import Manager
from threading import Thread
from typing import List

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
    fights = get_fights(request)
    return Report(fights=fights)


def get_fights(request: ReportRequest) -> List[Fight]:
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
                }
            }
        }
    """
    variables = {
        'code': request.code,
        'encounterID': request.encounter_id,
        'fightIDs': request.fight_ids,
        'killType': request.kill_type
    }

    report = query_graphql(query, variables)['reportData']['report']
    return get_fights_with_death_events(request, report['fights'])


def get_fights_with_death_events(request: ReportRequest, json_fights: List[dict]) -> List[Fight]:
    def process_death_events(json_fight: dict):
        death_events = get_fight_death_events(request, json_fight['id'])
        fights.append(Fight(json_fight, death_events))

    fights = Manager().list()
    threads = []

    for i, fight in enumerate(json_fights):
        thread = Thread(target=process_death_events, args=[fight])
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

    return list(sorted(fights, key=lambda f: f.start_time))


def get_fight_death_events(request: ReportRequest, fight_id: int) -> List[DeathEvent]:
    query = """
        query ($code: String!, $encounterID: Int, $fightIDs: [Int], $killType: KillType) {
            reportData {
                report(code: $code) {
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
    death_events = []

    for death in report['table']['data']['deathEvents']:
        try:
            death_events.append(DeathEvent(death))
        except KeyError:
            print(f"Warning: Skipping unknown death event: {death}")

    return death_events
