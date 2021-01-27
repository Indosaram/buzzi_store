from bs4 import BeautifulSoup as bs

from selenium_loader import SeleniumLoader


class CoolnjoyHelper:
    def __init__(self, param_common, param_coolnjoy):
        self.driver = SeleniumLoader(param_common['webdriver_path']).driver
        self.json_path = param_common['json_path']
        self.baseURL = param_coolnjoy['baseURL']
        self.boardURL = param_coolnjoy['boardURL']
