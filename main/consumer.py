import logging
from faktory import Worker
import multiprocessing
from tasks import live_see_all, parse_profile, parse_posts
from utils import URL_FACTORY

logging.basicConfig(level=logging.INFO)


def main():
    concurrency = multiprocessing.cpu_count()
    w = Worker(faktory=URL_FACTORY, queues=['default', 'busy'], concurrency=1)
    w.register('live_see_all', live_see_all)
    w.register('parse_profile', parse_profile)
    w.register('parse_posts', parse_posts)
    w.run()


if __name__ == '__main__':
    main()

