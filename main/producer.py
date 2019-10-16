import faktory
from utils.utils import URL_FACTORY, URL_FACEBOOK_GAMING_HOME
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    with faktory.connection(faktory=URL_FACTORY) as client:
        # client.queue('gaming_home', args=(URL_FACEBOOK_GAMING_HOME, ), queue='default')
        # client.queue('live_see_all', queue='default')
        client.queue('parse_posts', args=('1082685978426145', 'pubgmobiless'), queue='busy')
