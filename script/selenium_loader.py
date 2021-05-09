import os

from selenium import webdriver
from selenium.common import exceptions

class SeleniumLoader:
    def __init__(self, webdriverpath):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        )
        options.add_argument('lang=ko_KR')
        options.add_argument('log-level=3')  # To ignore welcome COUPANG message
        prefs = {
            "translate_whitelists": {"en": "ko"},
            "translate": {"enabled": "true"},
        }
        options.add_argument('--no-sandbox')
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.driver = webdriver.Chrome(webdriverpath, options=options)
        self.exceptions = exceptions

if __name__ == '__main__':
    dir_selenium = 'C:\\chromedriver\\'
    sl = SeleniumLoader(dir_selenium)