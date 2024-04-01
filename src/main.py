import argparse
from link_partidos import get_links
from api_calls import main as get_matches
from lineup_calls import main as get_lineups

GET_LINKS = 'get-links'
GET_STATS = 'get-stats'
GET_LINEUPS = 'get-lineups'


def run_script(action):
    if action == GET_LINKS:
        get_links()
    elif action == GET_STATS:
        get_matches()
    elif action == GET_LINEUPS:
        get_lineups()


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="")
    parser.add_argument('--action', type=str, required=True,
                        help='Action to perform', choices=[GET_LINKS, GET_STATS, GET_LINEUPS])
    return parser.parse_args()


def main():
    args = parse_arguments()
    run_script(args.action)


if __name__ == '__main__':
    main()
