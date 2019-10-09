import logging
from faktory import Worker

from main.tasks import get_five_ips, get_an_ip
from main.utils import URL_FACTORY
import multiprocessing


# logging.basicConfig(level=logging.DEBUG)


w = Worker(faktory=URL_FACTORY, queues=['default'], concurrency=multiprocessing.cpu_count())
# fb_scrapper = FacebookScrapper()
# w.register('gaming_home', fb_scrapper.gaming_home)
# w.register('get_five_ips', get_five_ips)
w.register('get_an_ip', get_an_ip)

w.run()

