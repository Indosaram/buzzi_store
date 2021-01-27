import os
import json
import platform
from urllib.parse import quote

import requests

from ppomppu_helper import PpomppuHelper
from clien_helper import ClienHelper
from ruliweb_helper import RuliwebHelper
from coolenjoy_helper import CoolenjoyHelper


class MainCrawler:
    def __init__(self, param) -> None:
        self.param_common = param['common']
        self.param_ppompu = param['ppompu']
        self.param_clien = param['clien']
        self.param_ruliweb = param['ruliweb']
        self.param_coolnjoy = param['coolenjoy']

    def _run_ppompu(self):
        ph = PpomppuHelper(self.param_common, self.param_ppompu)
        prod_details = ph.run()

        return prod_details

    def _run_clien(self):
        ch = ClienHelper(self.param_common, self.param_clien)
        prod_details = ch.run()

        return prod_details

    def _run_coolenjoy(self):
        ch = CoolenjoyHelper(self.param_common, self.param_coolenjoy)
        prod_details = ch.run()

        return prod_details

    def _run_ruliweb(self):
        rh = RuliwebHelper(self.param_common, self.param_ruliweb)
        prod_details = rh.run()

        return prod_details

    def _save_json(self, data):
        data_sorted = sorted(data, key=lambda x: x['date'], reverse=True)

        print('📋 Converting links to deep & short links')
        for dat in data_sorted:
            deeplink = self._to_deeplink(dat['link'])
            dat['link'] = deeplink if deeplink is not None else dat['link']

        jsondata = {"products": data_sorted}
        with open(
            self.param_common['json_path'],
            'w',
            encoding='utf-8',
        ) as f:
            json.dump(jsondata, f, ensure_ascii=False, indent=4)
        print('Finish saving .json')

    def _to_deeplink(self, link):
        res = requests.get(
            f"https://api.linkprice.com/ci/service/custom_link_xml"
            + f"?a_id={self.param_common['linkprice_af_id']}"
            + f"&url={quote(link, safe='')}&mode=json",
        )

        shortlink = None
        res_json = res.json()
        if res_json['result'] == 'S' and res_json['url'] is not None:
            deeplink = res_json['url']

            res = requests.get(
                f"http://cutt.ly/api/api.php?"
                + f"key={self.param_common['cuttly_api_key']}"
                + f"&short={quote(deeplink, safe='')}"
            )
            res_json = res.json()['url']
            if res_json['status'] in [1, 7]:
                shortlink = res_json['shortLink']

        return shortlink

    def run(self):
        prod_details = []

        prod_details.extend(self._run_ppompu())
        prod_details.extend(self._run_ruliweb())

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
            'linkprice_af_id': 'A100671773',
            'cuttly_api_key': '3faf74f71d6a823ce81f910926105cea21b0d',
        },
        'ppompu': {
            'baseURL': 'http://www.ppomppu.co.kr/zboard/',
            'boardURL': 'http://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu&hotlist_flag=999',
        },
        'ruliweb': {
            'baseURL': 'https://bbs.ruliweb.com/news/board/1020',
            'boardURL': 'https://bbs.ruliweb.com/news/board/1020?view_best=1',
        },
        'clien': {},
        'coolenjoy': {},
    }

    mc = MainCrawler(param)
    mc.run()