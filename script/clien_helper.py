import hashlib
import re

import requests

from bs4 import BeautifulSoup as bs

from selenium_loader import SeleniumLoader


class ClienHelper:
    def __init__(self, param_common, param_clien):
        self.driver = SeleniumLoader(param_common['webdriver_path']).driver
        self.json_path = param_common['json_path']
        self.baseURL = param_clien['baseURL']
        self.boardURL = param_clien['boardURL']

    def run(self):
        self.driver.get(self.boardURL)

        entries = [
            self.driver.find_element_by_xpath(
                f'//*[@id="board_list"]/div/div[2]/table/tbody/tr[{idx}]'
            )
            for idx in range(7, 35)
        ]

        print('🎁 루리웹')
        prod_details = []
        for idx, entry in enumerate(entries):
            print(f'-> Processing {idx+1}/29', end='\r')
            try:
                prod_details.append(self._get_product_data(entry))
            except:
                continue

        print('')
        self.driver.close()

        return prod_details

    def _get_product_data(self, entry):
        soup = bs(entry.get_attribute('innerHTML'), features="html.parser")
        deco = soup.select_one('a', {'class': 'deco'})
        shop = deco.text
        if shop == '품절':
            raise KeyError

        # Get product details
        prod_detail = {}
        prod_detail['origin'] = "루리웹"
        prod_detail['shop'] = shop
        prod_detail['origin_url'] = deco['href']
        prod_detail['hit'] = soup.select_one('td', {'class': 'hit'}).text
        prod_detail['up'] = soup.select_one('td', {'class': 'recomd'}).text

        self.driver.get(prod_detail['link'])
        raw_title = self.driver.find_element_by_xpath(
            "/html/head/meta[@property='og:title']"
        ).text.split('|')[0]

        prod_detail['description'] = self.driver.find_element_by_xpath(
            "/html/head/meta[@property='og:description']"
        ).text

        # this part is little treaky, better find another approach later
        raw_title = self.driver.find_element_by_class_name('view_title2').text
        fragments = re.compile("\[(.+?)\]|\((.+?)\)").findall(raw_title)
        prod_detail['shop'] = fragments[0][0]
        prod_detail['price'], prod_detail['shipping'] = fragments[-1][1].split(
            '/'
        )

        # Parse prod page's metadata
        link_to_prod = soup.select_one('div', {'class': 'source_url'}).text
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
