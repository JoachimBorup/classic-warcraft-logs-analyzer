import time
from collections import Counter
from typing import List

from src import graphql
from src.models import ReportRequest, Fight, DeathEvent, Report


def analyze(request: ReportRequest):
    report = get_report(request)

    fights = report.fights
    if len(fights) == 0:
        print("No fights found matching the given criteria.")
        return

    print(f"Report consists of {len(fights)} fights:")
    for fight in fights:
        mode = "Heroic" if fight.difficulty == 4 else "Normal"
        if fight.kill:
            print(f"Killed {fight.name} ({mode}):")
        else:
            print(f"Wiped on {fight.name} ({mode}) at {fight.boss_percentage}%:")

        analyze_fight(fight)


def get_report(request: ReportRequest) -> Report:
    print(f"Retrieving report {request.code} from Warcraft Logs...")
    start_time = time.time()
    report = graphql.get_report(request)
    print(f"Retrieved report {request.code} after {time.time() - start_time:.2f} seconds!\n")
    return report


def analyze_fight(fight: Fight):
    analyze_deaths(fight.death_events)


def analyze_deaths(death_events: List[DeathEvent]):
    if len(death_events) == 0:
        print("- No deaths")
        return

    ignored_abilities = {'Divine Intervention'}
    death_events = [death for death in death_events if death.ability_name not in ignored_abilities]
    common_deaths = Counter(death.ability_name for death in death_events).most_common(3)

    print("- All deaths:")
    for death in death_events:
        minutes, seconds = divmod(death.time / 1000, 60)
        print(f'  - {death.name} died to {death.ability_name} at {minutes:.0f}:{seconds:02.0f}')

    print(f'- Most common deaths:')
    for ability_name, count in common_deaths:
        print(f'  - {ability_name}: {count}')
