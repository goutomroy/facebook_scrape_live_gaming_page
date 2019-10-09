import time

import faktory
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from stem import Signal
from stem.control import Controller
from main.utils import CHROME_DRIVER_PATH, PROXY, URL_FACTORY, MOZILLA_DRIVER_PATH
# from selenium.webdriver.chrome.chrome_profile import ChromeProfile


# signal TOR for a new connection
def switch_IP():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)


def get_an_ip():
    # switch_IP()
    browser = get_browser()
    browser.get('https://whatsmyip.com/')
    browser.implicitly_wait(30)
    html = browser.page_source
    # soup = BeautifulSoup(html, 'lxml')
    # print(html)
    soup = BeautifulSoup(html, 'lxml')

    print('------------------------------------------')
    # print(soup.prettify())
    print(soup.find("p",  attrs={"id": "shownIpv4"}))
    # browser.quit()


def get_five_ips():
    with faktory.connection(faktory=URL_FACTORY) as client:
        for i in range(5):
            client.queue('get_an_ip', queue='default')
            # time.sleep(1)


# get a new selenium webdriver with tor as the proxy
def get_browser():
    # options = Options()
    # options.headless = True
    # options.add_argument(f'--proxy-server={PROXY}')
    # browser = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=options)
    # return browser

    fp = webdriver.FirefoxProfile()
    # Direct = 0, Manual = 1, PAC = 2, AUTODETECT = 4, SYSTEM = 5
    fp.set_preference("network.proxy.type", 1)
    fp.set_preference("network.proxy.socks_version", 5)
    fp.set_preference("network.proxy.socks", "127.0.0.1")
    fp.set_preference("network.proxy.socks_port", 9050)
    # fp.set_preference("network.proxy.socks_remote_dns", False)
    fp.update_preferences()
    from selenium.webdriver.firefox.options import Options
    options = Options()
    options.headless = True
    # options.add_argument('--headless')
    binary = FirefoxBinary(MOZILLA_DRIVER_PATH)
    capabilities_argument = DesiredCapabilities().FIREFOX
    # capabilities_argument["marionette"] = False

    # return webdriver.Firefox(options=options, firefox_profile=fp, executable_path=MOZILLA_DRIVER_PATH)
    return webdriver.Firefox(options=options, firefox_profile=fp, firefox_binary=binary, capabilities=capabilities_argument)


def gaming_home(url):
    # self.switch_IP()
    browser = get_browser()
    browser.get(url)

    browser.implicitly_wait(30)
    html = browser.page_source

    soup = BeautifulSoup(html, 'lxml')
    see_all_url = soup.find("a", attrs={'class': "_4jy0 _4jy4 _517h _51sy _42ft"})
    print('================')
    # print(html)
    # print()
    print(f'{type(see_all_url)}  {see_all_url}')
    browser.quit()