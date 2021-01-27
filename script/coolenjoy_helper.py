from bs4 import BeautifulSoup as bs

from selenium_loader import SeleniumLoader


class CoolenjoyHelper:
    def __init__(self, param_common, param_coolenjoy):
        selenium_loader = SeleniumLoader(param_common['webdriver_path'])
        self.driver = selenium_loader.driver
        self.driver_exceptions = selenium_loader.exceptions
        self.json_path = param_common['json_path']
        self.baseURL = param_coolenjoy['baseURL']
        self.boardURL = param_coolenjoy['boardURL']
