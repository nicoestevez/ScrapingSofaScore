import argparse
from link_partidos import get_links
from api_calls import main as get_matches


def run_script(action):
    if action == 'get-links':
        get_links()
    elif action == 'get-data':
        get_matches()


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="")
    parser.add_argument('--action', type=str, required=True,
                        help='Action to perform', choices=['get-links', 'get-data'])
    return parser.parse_args()


def main():
    args = parse_arguments()
    run_script(args.action)


if __name__ == '__main__':
    main()
