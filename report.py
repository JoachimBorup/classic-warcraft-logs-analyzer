import graphql
from models import ReportRequest


def analyze(request: ReportRequest):
    print(f"Retrieving report {request.code} from Warcraft Logs...")
    report = graphql.get_report(request)
    print(f"Got report {request.code}!")
    print()

    print("Analyzing report...")
    print(f"Report consists of {len(report.fights)} fights:")
    for fight in report.fights:
        print(f"- {fight.name}")
