import requests

from src.models import DeathEvent, Fight, Report, ReportRequest
from src.utils import get_env_var

API_URL = 'https://www.warcraftlogs.com/api/v2/user'


def query_graphql(query: str, variables: dict) -> dict:
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
    queryFights = """
        query ($code: String!, $encounterID: Int, $fightIDs: [Int]) {
            reportData {
                report(code: $code) {
                    fights(encounterID: $encounterID, fightIDs: $fightIDs) {
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
    queryTable = """
        query ($code: String!, $encounterID: Int, $fightIDs: [Int]) {
            reportData {
                report(code: $code) {
                    table(encounterID: $encounterID, fightIDs: $fightIDs)
                }
            }
        }
    """
    
    variables = {
        'code': request.code,
        'encounterID': request.encounter,
        'fightIDs': request.fights
    }

    dataRep = query_graphql(queryFights, variables)
    json_fights = dataRep['reportData']['report']['fights']
    datatable = query_graphql(queryTable, variables)
    json_tables = datatable['reportData']['report']['table']['data']['deathEvents']

    print(json_tables)
    
    fights = [Fight(
        name=json_fight['name'],
        encounter_id=json_fight['encounterID'],
        kill=json_fight['kill'],
        difficulty=json_fight['difficulty'],
        boss_percentage=json_fight['bossPercentage'],
        average_item_level=json_fight['averageItemLevel']
    ) for json_fight in json_fights if json_fight['encounterID'] != 0]

    deathEvents = [DeathEvent(
        name=json_table['name'],
        ability_name=json_table['ability']['name']
    )for json_table in json_tables]
    

    return Report(fights=fights, deathEvents=deathEvents)
