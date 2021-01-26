import re
import hashlib

import requests

from bs4 import BeautifulSoup as bs

from selenium_loader import SeleniumLoader


class PpomppuHelper:
    def __init__(self, param_common, param_ppompu):
        self.driver = SeleniumLoader(param_common['webdriver_path']).driver
        self.json_path = param_common['json_path']
        self.baseURL = param_ppompu['baseURL']
        self.boardURL = param_ppompu['boardURL']

    def run(self):
        self.driver.get(self.boardURL)
        entries = self.driver.find_elements_by_class_name(
            'list0'
        ) + self.driver.find_elements_by_class_name('list1')
        routes = [
            bs(entry.get_attribute('innerHTML'), features="html.parser").select(
                'a'
            )[1]['href']
            for entry in entries
        ]
        prod_details = []

        print('🎁 뽐뿌')
        for idx, route in enumerate(routes):
            print(f'-> Processing {idx+1}/{len(routes)}', end='\r')
            try:
                prod_details.append(self._get_product_data(idx, route))
            except:
                continue
        print('')
        self.driver.close()

        return prod_details

    def _get_product_data(self, idx, route):
        self.driver.get(self.baseURL + route)

        # Get product details
        prod_detail = {}
        prod_detail['origin'] = "뽐뿌"

        # this part is little treaky, better find another approach later
        raw_title = self.driver.find_element_by_class_name('view_title2').text
        fragments = re.compile("\[(.+?)\]|\((.+?)\)").findall(raw_title)
        prod_detail['shop'] = fragments[0][0]
        prod_detail['price'], prod_detail['shipping'] = fragments[-1][1].split(
            '/'
        )

        innerHTML = self.driver.find_element_by_class_name(
            'sub-top-text-box'
        ).get_attribute('innerHTML')
        soup = bs(innerHTML, features="html.parser")

        prod_detail['date'] = (
            re.compile(r'\d\d\d\d-\d\d-\d\d').search(soup.text).group()
        )
        prod_detail['hit'] = (
            re.compile(r'조회수: \d+').search(soup.text).group().split(' ')[1]
        )
        prod_detail['up'] = (
            re.compile(r'추천수: \d+').search(soup.text).group().split(' ')[1]
        )

        prod_detail['origin_url'] = self.driver.find_element_by_xpath(
            "/html/head/meta[@property='og:url']"
        ).get_attribute('content')

        # Parse prod page's metadata
        link_to_prod = self.driver.find_element_by_class_name(
            'wordfix'
        ).text.split(' ')[1]
        res = requests.get(link_to_prod)
        if res.reason == 'OK':
            prod_detail['link'] = res.url
        else:
            raise KeyError

        soup = bs(res.text, features="html.parser")
        prod_detail['thumbnail'] = soup.find('meta', {"property": "og:image"})[
            'content'
        ]
        prod_detail['title'] = soup.find('title').text
        prod_detail['id'] = hashlib.sha1(
            prod_detail['title'].encode()
        ).hexdigest()

        return prod_detail
