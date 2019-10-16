import logging
import re

URL_FACTORY = 'tcp://:aggero@localhost:7419'
CHROME_DRIVER_PATH = '/usr/lib/chromium-browser/chromedriver'
MOZILLA_DRIVER_PATH = r"/usr/local/bin/geckodriver"

URL_FACEBOOK_ROOT = 'https://www.facebook.com'
URL_FACEBOOK_GAMING_HOME = 'https://www.facebook.com/gaming/?view=home'

PROXY = "socks5://localhost:9050"

PROXIES = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}


def is_valid_email(text):
    regex = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if re.search(regex, text):
        return True
    return False


def is_url(text):
    regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    if re.search(regex, text):
        return True
    return False


