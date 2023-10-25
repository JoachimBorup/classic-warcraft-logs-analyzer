import argparse


def parse_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(description='Analyze classic Warcraft Logs reports.')
    sub_parsers = arg_parser.add_subparsers(dest='command', required=True)

    _add_analyze_sub_parser(sub_parsers)
    _add_token_sub_parser(sub_parsers)

    return arg_parser.parse_args()


def _add_analyze_sub_parser(sub_parsers):
    analyze_parser = sub_parsers.add_parser(name='analyze', help='Analyze a Warcraft Logs report.')
    analyze_parser.add_argument('report', help='The code of the report to analyze.')
    analyze_parser.add_argument('-f', '--fights', nargs='+', type=int, default=[],
                                help='The IDs of the fights to analyze.')

    encounter_group = analyze_parser.add_mutually_exclusive_group()
    encounter_group.add_argument('-e', '--encounter', type=int,
                                 help='The ID of the encounter to analyze. Mutually exclusive with --name')
    encounter_group.add_argument('-n', '--name',
                                 help='The name of the encounter to analyze. Mutually exclusive with --encounter')


def _add_token_sub_parser(sub_parsers):
    sub_parsers.add_parser(name='token', help='Get an access token for the Warcraft Logs API.')
