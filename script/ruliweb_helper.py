import hashlib
import re
from datetime import datetime

from urllib.parse import urlparse

import requests

from bs4 import BeautifulSoup as bs

from selenium_loader import SeleniumLoader
from exception import *


class RuliwebHelper:
    def __init__(self, param_common, param_clien):
        selenium_loader = SeleniumLoader(param_common['webdriver_path'])
        self.driver = selenium_loader.driver
        self.driver_exceptions = selenium_loader.exceptions
        self.json_path = param_common['json_path']
        self.baseURL = param_clien['baseURL']
        self.boardURL = param_clien['boardURL']

    def run(self):
        self.driver.get(self.boardURL)

        print('🎁 루리웹')
        pre_prod_details = []
        for idx in range(7, 35):
            entry = self.driver.find_element_by_xpath(
                f'//*[@id="board_list"]/div/div[2]/table/tbody/tr[{idx}]'
            )
            try:
                shop = self.driver.find_element_by_xpath(
                    f'//*[@id="board_list"]/div/div[2]/table/tbody/tr[{idx}]/td[3]/div/a[1]/a'
                ).text[1:-1]
                if shop == '품절':
                    continue
            except self.driver_exceptions.NoSuchElementException:
                shop = ''

            # Get product details
            prod_detail = {}
            prod_detail['origin'] = "루리웹"
            prod_detail['shop'] = shop

            soup = bs(entry.get_attribute('innerHTML'), features="html.parser")
            prod_detail['origin_url'] = soup.select_one("a[class = 'deco']")[
                'href'
            ]
            prod_detail['hit'] = soup.select_one(
                "td[class='hit']"
            ).text.replace('\n', '')
            prod_detail['up'] = soup.select_one(
                "td[class='recomd']"
            ).text.replace('\n', '')

            pre_prod_details.append(prod_detail)

        prod_details = []
        for idx, prod_detail in enumerate(pre_prod_details):
            print(f'-> Processing {idx+1}/{len(pre_prod_details)}')
            try:
                prod_details.append(self._get_product_data(prod_detail))
            except Exception as e:
                print(e)
                continue

        print(
            f'✅ Processed {len(prod_details)}/{len(pre_prod_details)} entries'
        )
        self.driver.close()

        return prod_details

    def _get_product_data(self, prod_detail):
        self.driver.get(prod_detail['origin_url'])
        raw_title = (
            self.driver.find_element_by_xpath(
                "/html/head/meta[@property='og:title']"
            )
            .get_attribute('content')
            .split('|')[0]
        )

        prod_detail['description'] = self.driver.find_element_by_xpath(
            "/html/head/meta[@property='og:description']"
        ).get_attribute('content')

        date_string = self.driver.find_element_by_class_name('regdate').text
        date_obj = datetime.strptime(date_string, "%Y.%m.%d (%H:%M:%S)")
        prod_detail['date'] = datetime.strftime(date_obj, '%Y-%m-%d %H:%M')

        price = re.compile(r"\d{3,}(,\d{1,3})?원").search(raw_title)
        prod_detail['price'] = price.group() if price is not None else price

        freeshipping = ['무료', '무배', '무료배송']
        if any(ele in raw_title for ele in freeshipping):
            prod_detail['shipping'] = '무료배송'
        else:
            prod_detail['shipping'] = ''

        # Parse prod page's metadata
        try:
            webelement = self.driver.find_element_by_class_name('source_url')
        except:
            raise NoUrlExistError('No product URL exsits')
        link_to_prod = webelement.text.split(' ')[-1]
        url_parsed = urlparse(link_to_prod)

        if '.' in url_parsed.netloc:
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
            }
            try:
                res = requests.get(link_to_prod, headers=headers)
            except Exception as e:
                raise e
            if res.reason == 'OK':
                prod_detail['link'] = res.url
            else:
                raise ConnectionError
        else:
            raise NotAnUrlError(f'Invalid URL detected : {link_to_prod}')

        soup = bs(res.text, features="html.parser")
        try:
            prod_detail['thumbnail'] = soup.select_one(
                "meta[property='og:image']"
            )['content']
            prod_detail['title'] = soup.find('title').text
            prod_detail['id'] = hashlib.sha1(
                prod_detail['title'].encode()
            ).hexdigest()
        except:
            raise InvalidMetadataError(
                'This website does not provide valid meta tags.'
            )

        return prod_detail
