import sys
from multiprocessing import Manager
from threading import Thread

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
    """Gets a report from the Warcraft Logs API.

    :param request: The report request.
    :return: The report.
    """

    query = """
        query (
            $code: String!
            $encounterID: Int
            $fightIDs: [Int]
            $killType: KillType
        ) {
            reportData {
                report(code: $code) {
                    masterData {
                        actors {
                            id
                            name
                        }
                    }
                    fights(
                        encounterID: $encounterID
                        fightIDs: $fightIDs
                        killType: $killType
                    ) {
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
    fights = get_fights_with_death_events(request, report['fights'])
    actors = {actor['id']: actor['name'] for actor in report['masterData']['actors']}

    return Report(fights, actors)


def get_fights_with_death_events(request: ReportRequest, json_fights: list[dict]) -> list[Fight]:
    """Gets a list of fights with death events for each fight.
    This method is parallelized to speed up the process of retrieving death events.

    :param request: The report request.
    :param json_fights: The fights to retrieve death events for.
    :return: The fights with death events.
    """

    def process_death_events(json_fight: dict):
        death_events = get_fight_death_events(request, json_fight['id'])
        fights.append(Fight(json_fight, death_events))

    fights = Manager().list()
    threads = [Thread(target=process_death_events, args=[fight]) for fight in json_fights]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    return list(sorted(fights, key=lambda f: f.start_time))


def get_fight_death_events(request: ReportRequest, fight_id: int) -> list[DeathEvent]:
    """Gets the death events for a given fight.

    :param request: The report request.
    :param fight_id: The ID of the fight to retrieve death events for.
    :return: The death events for the given fight.
    """

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


def get_actor_events(request: ReportRequest, actor_id: int, fight: Fight):
    query = """
    query (
        $code: String!
        $encounterID: Int
        $fightIDs: [Int]
        $killType: KillType
        $sourceID: Int
        $startTime: Float
        $endTime: Float
    ) {
        reportData {
            report(code: $code) {
                events(
                    encounterID: $encounterID
                    fightIDs: $fightIDs
                    killType: $killType
                    sourceID: $sourceID
                    startTime: $startTime
                    endTime: $endTime
                ) {
                    nextPageTimestamp
                    data
                }
            }
        }
    }
    """
    variables = {
        'code': request.code,
        'encounterID': request.encounter_id,
        'fightIDs': [fight.id],
        'killType': request.kill_type,
        'sourceID': actor_id,
        'startTime': fight.start_time,
        'endTime': fight.end_time
    }

    events = query_graphql(query, variables)['reportData']['report']['events']
    next_page_timestamp = events['nextPageTimestamp']
    if next_page_timestamp is not None:
        print(f"Warning: More events exist at timestamp {next_page_timestamp}", file=sys.stderr)

    return events['data']
