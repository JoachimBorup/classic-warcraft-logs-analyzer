from collections import Counter

from src import graphql
from src.models import ReportRequest


def analyze(request: ReportRequest):
    print(f"Retrieving report {request.code} from Warcraft Logs...")
    report = graphql.get_report(request)
    print(f"Retrieved report {request.code}!")
    print()

    fights = report.fights
    if len(fights) == 0:
        print("No fights found matching the given criteria.")
        return

    print(f"Report consists of {len(fights)} fights:")
    for fight in fights:
        mode = "Heroic" if fight.difficulty == 4 else "Normal"
        if fight.kill:
            print(f"- Killed {fight.name} ({mode})")
        else:
            print(f"- Wiped on {fight.name} ({mode}) at {fight.boss_percentage}%")

    death_events = report.death_events
    count: int = 0
    last_death_ability: list[str] = []
    for death_event in death_events:
        ability_names = [death.ability_name for death in death_events]
        most_common_cause, count_ability = Counter(ability_names).most_common(1)[0]
        print(f"- Player: {death_event.name} died to {death_event.ability_name}")
        count = len(death_events)
        last_death_ability.append(death_event.ability_name)
    print(f"- The amount: {count} of people dying on this pull")
    print(f"- The amount: {count_ability} of people dying to {most_common_cause}")
