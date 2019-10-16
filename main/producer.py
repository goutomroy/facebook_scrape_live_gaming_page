import faktory
from utils.utils import URL_FACTORY, URL_FACEBOOK_GAMING_HOME
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    with faktory.connection(faktory=URL_FACTORY) as client:
        client.queue('live_see_all', queue='default')
