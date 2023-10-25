from src import arg_parser, report, utils
from src.models import ReportRequest


def main():
    args = arg_parser.parse_args()

    if args.command == 'analyze':
        report.analyze(ReportRequest(args))
    elif args.command == 'token':
        print(utils.get_access_token(args.client_id, args.client_secret))
    else:
        raise ValueError(f'Unknown command: {args.command}')


if __name__ == '__main__':
    main()
