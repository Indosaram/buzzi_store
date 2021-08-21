"""Clien helper class"""

from selenium_helper.selenium_loader import SeleniumLoader


class ClienHelper:
    """Clien helper class"""

    def __init__(self, param_common, param_coolnjoy):
        self.driver = SeleniumLoader().driver
        self.json_path = param_common['json_path']
        self.base_url = param_coolnjoy['base_url']
        self.board_url = param_coolnjoy['board_url']

    def run(self):
        """Run crawling"""
        return
