import os

from selenium import webdriver


class SeleniumLoader:
    def __init__(self, dir_selenium):
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
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        webdriverpath = os.path.join(dir_selenium, 'chromedriver.exe')

        self.driver = webdriver.Chrome(webdriverpath, options=options)


if __name__ == '__main__':
    dir_selenium = 'C:\\chromedriver\\'
    sl = SeleniumLoader(dir_selenium)