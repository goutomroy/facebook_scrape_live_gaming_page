from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils.utils import CHROME_DRIVER_PATH


class WebBrowser(object):
    __instance = None
    __browser = None

    def __init__(self):
        if WebBrowser.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            options = Options()
            # options.add_argument("--disable-impl-side-painting")
            options.headless = True
            browser = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=options)
            browser.implicitly_wait(30)
            browser.set_page_load_timeout(30)
            browser.set_script_timeout(15)
            browser.maximize_window()

            WebBrowser.__browser = browser
            WebBrowser.__instance = self

    def get_browser(self):
        return self.__browser

    @staticmethod
    def get_instance():
        if WebBrowser.__instance is None:
            WebBrowser()
        return WebBrowser.__instance

    def __str__(self):
        return 'WebBrowser object'
