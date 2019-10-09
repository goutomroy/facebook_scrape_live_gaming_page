import faktory
from main.utils import URL_FACTORY, URL_FACEBOOK_GAMING_HOME
import logging


logging.basicConfig(level=logging.DEBUG)


with faktory.connection(faktory=URL_FACTORY) as client:
    # client.queue('gaming_home', args=(URL_FACEBOOK_GAMING_HOME, ), queue='default')
    # client.queue('get_five_ips', queue='default')
    client.queue('get_an_ip', queue='default')
    # client.queue('get_an_ip', queue='default')
    # client.queue('get_an_ip', queue='default')
    # client.queue('get_an_ip', queue='default')
    # client.queue('get_an_ip', queue='default')
