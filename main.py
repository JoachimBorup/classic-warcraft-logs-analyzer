import argparse

import report
from models import ReportRequest


def parse_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(description='Analyze classic Warcraft Logs reports.')
    arg_parser.add_argument('report', help='The code of the report to analyze.')
    arg_parser.add_argument('--encounter', help='The encounter to analyze.')
    arg_parser.add_argument('--fights', nargs='+', help='The fights to analyze.')
    return arg_parser.parse_args()


def main():
    args = parse_args()
    request = ReportRequest(args)
    report.analyze(request)


if __name__ == '__main__':
    main()
