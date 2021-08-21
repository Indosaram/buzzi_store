"""Coolenjoy helper class"""

from selenium_helper.selenium_loader import SeleniumLoader


class CoolenjoyHelper:
    """Coolenjoy helper class"""

    def __init__(self, param_common, param_coolenjoy):
        self.driver = SeleniumLoader().driver
        self.json_path = param_common['json_path']
        self.base_url = param_coolenjoy['base_url']
        self.board_url = param_coolenjoy['board_url']

    def run(self):
        """Run crawling"""
        return
