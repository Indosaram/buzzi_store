import os
import json
import platform

from ppomppu_helper import PpomppuHelper


class MainCrawler:
    def __init__(self, param) -> None:
        self.param_common = param['common']
        self.param_ppompu = param['ppompu']

    def _run_ppompu(self):
        ph = PpomppuHelper(self.param_common, self.param_ppompu)
        prod_details = ph.run()

        return prod_details

    def _save_json(self, data):
        jsondata = {"products": data}
        with open(
            self.param_common['json_path'],
            'w',
            encoding='utf-8',
        ) as f:
            json.dump(jsondata, f, ensure_ascii=False, indent=4)
        print('Finish saving .json')

    def run(self):
        prod_details = []

        prod_details.extend(self._run_ppompu())

        self._save_json(prod_details)


if __name__ == "__main__":
    if platform.system() == 'Windows':
        webdriver_path = 'C:\\chromedriver\\chromedriver.exe'
    else:
        webdriver_path = './script/chromedriver'

    param = {
        'common': {
            'webdriver_path': webdriver_path,
            'json_path': os.path.join(os.getcwd(), 'src', 'productsData.json'),
        },
        'ppompu': {
            'baseURL': 'http://www.ppomppu.co.kr/zboard/',
            'boardURL': 'http://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu&hotlist_flag=999',
        },
        'ruliweb': {
            'baseURL': 'https://bbs.ruliweb.com/news/board/1020'
            'boardURL': 'https://bbs.ruliweb.com/news/board/1020?view_best=1'
        },
    }

    mc = MainCrawler(param)
    mc.run()