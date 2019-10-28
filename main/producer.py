import argparse
import faktory
from utils import URL_FACTORY
import logging

logging.basicConfig(level=logging.INFO)


def main():
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('-nup', '--num_user_to_parse', type=int)
    my_parser.add_argument('-nps', '--num_post_scroll', type=int)
    c_args = my_parser.parse_args()
    with faktory.connection(faktory=URL_FACTORY) as client:
        client.queue('live_see_all', args=[c_args.num_user_to_parse, c_args.num_post_scroll], queue='default')


if __name__ == '__main__':
    main()
