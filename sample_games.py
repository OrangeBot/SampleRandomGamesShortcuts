import argparse
import resources

parser = argparse.ArgumentParser()
parser.add_argument('--verbose', '-v', action='store_true', default=resources.verbose)

args = parser.parse_args()
resources.verbose = args.verbose


def main(verbose):
    if verbose:
        print("Starting random game sample generation")

    from lib import update_games_shortcuts
    today_games = update_games_shortcuts(hardcode_mode=True)

    if verbose:
        print("Games shortcuts generation finished")


if __name__ == "__main__":
    main(resources.verbose)

