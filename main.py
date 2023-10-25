import argparse

from src import report, utils
from src.models import ReportRequest


def parse_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(description='Analyze classic Warcraft Logs reports.')
    sub_parsers = arg_parser.add_subparsers(dest='command', required=True)

    analyze_parser = sub_parsers.add_parser(name='analyze', help='Analyze a Warcraft Logs report.')
    analyze_parser.add_argument('report', help='The code of the report to analyze.')
    analyze_parser.add_argument('-f', '--fights', nargs='+', help='The IDs of the fights to analyze.', type=int, default=[])
    encounter_group = analyze_parser.add_mutually_exclusive_group()
    encounter_group.add_argument('-e', '--encounter', help='The ID of the encounter to analyze. Mutually exclusive with --name', type=int)
    encounter_group.add_argument('-n', '--name', help='The name of the encounter to analyze. Mutually exclusive with --encounter')

    sub_parsers.add_parser(name='token', help='Get an access token for the Warcraft Logs API.')

    return arg_parser.parse_args()


def main():
    args = parse_args()

    if args.command == 'analyze':
        report.analyze(ReportRequest(args))
    elif args.command == 'token':
        print(utils.get_access_token())
    else:
        raise ValueError(f'Unknown command: {args.command}')


if __name__ == '__main__':
    main()
