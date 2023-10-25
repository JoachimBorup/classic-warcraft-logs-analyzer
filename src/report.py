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
