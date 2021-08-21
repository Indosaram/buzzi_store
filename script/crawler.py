"""Main crawler class"""

from json.decoder import JSONDecodeError
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

    def __init__(self, parameters) -> None:
        self.param_common = parameters['common']
        self.param_ppompu = parameters['ppompu']
        self.param_clien = parameters['clien']
        self.param_ruliweb = parameters['ruliweb']
        self.param_coolenjoy = parameters['coolenjoy']

        self.cloudinary_helper = CloudinaryHelper("buzzistore")
        self._download_json()
        self._disable_ssl_warning()

    @staticmethod
    def _disable_ssl_warning():
        requests.packages.urllib3.disable_warnings()  # pylint: disable=no-member
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += (  # pylint: disable=no-member
            ':HIGH:!DH:!aNULL'
        )

        try:
            requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += (
                ':HIGH:!DH:!aNULL'
            )
        except AttributeError:
            # no pyopenssl support used / needed / available
            pass

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
        def to_cuttly(deeplink):
            try:
                res = requests.get(
                    "https://cutt.ly/api/api.php?"
                    f"key={self.param_common['cuttly_api_key']}"
                    f"&short={quote(deeplink, safe='')}",
                    verify=False,
                )
                res_json = res.json()['url']
                if res_json['status'] in [1, 7]:
                    deeplink = res_json['shortLink']
                else:
                    print("Invalid request has been sent to cutt.ly api")
            except JSONDecodeError as exc:
                print(exc, res.text)

            return deeplink

        deeplink = link

        res = requests.get(
            "https://api.linkprice.com/ci/service/custom_link_xml"
            f"?a_id={self.param_common['linkprice_af_id']}"
            f"&url={quote(link, safe='')}&mode=json",
            verify=False,
        )
        res_json = res.json()
        if res_json['result'] == 'S' and res_json['url'] is not None:
            deeplink = to_cuttly(res_json['url'])
        else:
            print("No merchant info in linkprice:", link)

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

    main_crawler = MainCrawler(parameter)
    main_crawler.run()
