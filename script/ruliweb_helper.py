
from bs4 import BeautifulSoup as bs

from selenium_loader import SeleniumLoader


class RuliwebHelper:
    def __init__(self, param_common, param_ppompu):
        self.driver = SeleniumLoader(param_common['webdriver_path']).driver
        self.json_path = param_common['json_path']
        self.baseURL = param_ppompu['baseURL']
        self.boardURL = param_ppompu['boardURL']
