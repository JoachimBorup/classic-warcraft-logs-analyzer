import graphql
from models import ReportRequest


def analyze(request: ReportRequest):
    print(f"Retrieving report {request.code} from Warcraft Logs...")
    report = graphql.get_report(request)
    print(f"Retrieved report {request.code}!")
    print()

    fights = report.fights
    average_item_levels = [fight.average_item_level for fight in fights]
    min_avg_ilvl, max_avg_ilvl = min(average_item_levels), max(average_item_levels)

    print(f"Report consists of {len(fights)} fights, with the avg. ilvl "
          f"ranging between {min_avg_ilvl:.2f} and {max_avg_ilvl:.2f}:")
    for fight in fights:
        mode = "Heroic" if fight.difficulty == 4 else "Normal"
        if fight.kill:
            print(f"- Killed {fight.name} ({mode})")
        else:
            print(f"- Wiped on {fight.name} ({mode}) at {fight.boss_percentage}%")

