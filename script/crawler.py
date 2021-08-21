"""Main crawler class"""

import os
import json
import platform
from urllib.parse import quote
from urllib.request import urlretrieve

import requests

from cloudinary_helper import CloudinaryHelper
from ppomppu_helper import PpomppuHelper
from clien_helper import ClienHelper
from ruliweb_helper import RuliwebHelper
from coolenjoy_helper import CoolenjoyHelper


class MainCrawler:
    """Main crawler class"""

    def __init__(self, parameter) -> None:
        self.param_common = parameter['common']
        self.param_ppompu = parameter['ppompu']
        self.param_clien = parameter['clien']
        self.param_ruliweb = parameter['ruliweb']
        self.param_coolenjoy = parameter['coolenjoy']

        cloudinary_param = {
            'cloud_name': parameter['common']['cloudinary_name'],
            'api_key': parameter['common']['cloudinary_api_key'],
            'api_secret': parameter['common']['cloudinary_api_secret'],
        }
        self.cloudinary_helper = CloudinaryHelper(
            cloudinary_param["cloud_name"]
        )
        self._download_json()

    def _run_ppompu(self):
        ppomppu_helper = PpomppuHelper(self.param_common, self.param_ppompu)
        prod_details = ppomppu_helper.run()

        return prod_details

    def _run_clien(self):
        clien_helper = ClienHelper(self.param_common, self.param_clien)
        prod_details = clien_helper.run()

        return prod_details

    def _run_coolenjoy(self):
        coolenjoy_helper = CoolenjoyHelper(
            self.param_common, self.param_coolenjoy
        )
        prod_details = coolenjoy_helper.run()

        return prod_details

    def _run_ruliweb(self):
        ruliweb_helper = RuliwebHelper(self.param_common, self.param_ruliweb)
        prod_details = ruliweb_helper.run()

        return prod_details

    def _save_json(self, data):
        print('📋 Converting links to deep & short links')

        with open(
            self.param_common['json_path'],
            'r',
            encoding='utf-8',
        ) as file:
            data_old = json.load(file)['products']

        data_ids = [entry['id'] for entry in data_old]

        data_final = []
        for idx, entry in enumerate(data):
            deeplink = self._to_deeplink(entry['link'])
            entry['link'] = deeplink if deeplink is not None else entry['link']

            if entry['id'] in data_ids:
                data_old[data_ids.index(entry['id'])] = entry
            else:
                data_final.append(entry)
            print(f"-> Converting {idx+1}/{len(data)} links", end="\r")
        print("")

        data_final.extend(data_old)

        data_sorted = sorted(data_final, key=lambda x: x['date'], reverse=True)
        jsondata = {"products": data_sorted[:1000]}
        with open(
            self.param_common['json_path'],
            'w',
            encoding='utf-8',
        ) as file:
            json.dump(jsondata, file, ensure_ascii=False, indent=4)
        self._upload_json()
        print('Finish saving .json')

    def _to_deeplink(self, link):
        deeplink = link

        try:
            res = requests.get(
                "https://api.linkprice.com/ci/service/custom_link_xml"
                f"?a_id={self.param_common['linkprice_af_id']}"
                f"&url={quote(link, safe='')}&mode=json",
            )
            res_json = res.json()
            if res_json['result'] == 'S' and res_json['url'] is not None:
                deeplink = res_json['url']
            else:
                res = requests.get(
                    "http://cutt.ly/api/api.php?"
                    f"key={self.param_common['cuttly_api_key']}"
                    f"&short={quote(deeplink, safe='')}"
                )
                if "url" in res.json().keys():
                    res_json = res.json()['url']
                    if res_json['status'] in [1, 7]:
                        deeplink = res_json['shortLink']
        except Exception as exc:
            print("Cannot convert this link by any methods :", exc)

        return deeplink

    def run(self):
        """Run main process"""
        prod_details = []

        prod_details.extend(self._run_ppompu())
        prod_details.extend(self._run_ruliweb())

        self._save_json(prod_details)

    def _download_json(self):
        url = self.cloudinary_helper.get_url('productsData.json')
        urlretrieve(url, self.param_common['json_path'])

    def _upload_json(self):
        self.cloudinary_helper.upload_file(self.param_common['json_path'])
        print("-> json upload succeed")


if __name__ == "__main__":
    if platform.system() == 'Windows':
        WEBDRIVER_PATH = 'C:\\chromedriver\\chromedriver.exe'
        from dotenv import load_dotenv

        load_dotenv(verbose=True)

    elif platform.system() == 'Darwin':
        WEBDRIVER_PATH = './script/chromedriver_mac'
        from dotenv import load_dotenv

        load_dotenv(verbose=True)
    else:
        WEBDRIVER_PATH = './script/chromedriver'

    parameter = {
        'common': {
            'webdriver_path': WEBDRIVER_PATH,
            'json_path': os.path.join(os.getcwd(), 'src', 'productsData.json'),
            'linkprice_af_id': os.getenv('LINKPRICE_AF_ID'),
            'cuttly_api_key': os.getenv('CUTTLY_API_KEY'),
            'cloudinary_name': os.getenv('CLOUDINARY_NAME'),
            'cloudinary_api_key': os.getenv('CLOUDINARY_API_KEY'),
            'cloudinary_api_secret': os.getenv('CLOUDINARY_API_SECRET'),
        },
        'ppompu': {
            'base_url': 'http://www.ppomppu.co.kr/zboard/',
            'board_url': 'http://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu&hotlist_flag=999',
        },
        'ruliweb': {
            'base_url': 'https://bbs.ruliweb.com/news/board/1020',
            'board_url': 'https://bbs.ruliweb.com/news/board/1020?view_best=1',
        },
        'clien': {},
        'coolenjoy': {},
    }

    mc = MainCrawler(parameter)
    mc.run()
