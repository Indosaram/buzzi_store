import re

from bs4 import BeautifulSoup as bs

from selenium_loader import SeleniumLoader
from exception import *
from helper_common import meta_from_prod_detail_page


class PpomppuHelper:
    def __init__(self, param_common, param_ppompu):
        selenium_loader = SeleniumLoader(param_common['webdriver_path'])
        self.driver = selenium_loader.driver
        self.driver_exceptions = selenium_loader.exceptions
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
            print(f'-> Processing {idx+1}/{len(routes)}')
            try:
                prod_details.append(self._get_product_data(idx, route))
            except Exception as e:
                print(e)
                continue
        print(f'✅ Processed {len(prod_details)}/{len(routes)} entries')
        self.driver.close()

        return prod_details

    def _get_product_data(self, idx, route):
        self.driver.get(self.baseURL + route)

        if '품절 / 종결 / 취소된 게시물입니다.' in self.driver.page_source:
            raise KeyError

        # Get product details
        prod_detail = {}
        prod_detail['origin'] = "뽐뿌"

        # this part is little tricky, better find another approach later
        try:
            raw_title = self.driver.find_element_by_class_name(
                'view_title2'
            ).text
            fragments = re.compile("\[(.+?)\]|\((.+?)\)").findall(raw_title)
            prod_detail['shop'] = fragments[0][0]
            prod_detail['price'], shipping = fragments[-1][1].split('/')
            freeshipping = ['무료', '무배', '무료배송', '0']
            if any(ele in shipping for ele in freeshipping):
                prod_detail['shipping'] = '무료배송'
            else:
                prod_detail['shipping'] = ''
        except ValueError:
            print('No valid price / shipping info')
            prod_detail['shop'] = ''
            prod_detail['price'] = ''
            prod_detail['shipping'] = ''

        innerHTML = self.driver.find_element_by_class_name(
            'sub-top-text-box'
        ).get_attribute('innerHTML')
        soup = bs(innerHTML, features="html.parser")

        prod_detail['date'] = (
            re.compile(r'\d\d\d\d-\d\d-\d\d \d\d:\d\d')
            .search(soup.text)
            .group()
        )
        prod_detail['hit'] = (
            re.compile(r'조회수: \d+').search(soup.text).group().split(' ')[1]
        )
        prod_detail['up'] = (
            re.compile(r'추천수: \d+').search(soup.text).group().split(' ')[1]
        )
        prod_detail['category'] = (
            re.compile(r'분류: \w+').search(soup.text).group()
        )

        prod_detail['origin_url'] = self.driver.find_element_by_xpath(
            "/html/head/meta[@property='og:url']"
        ).get_attribute('content')
        prod_detail['description'] = self.driver.find_element_by_xpath(
            "/html/head/meta[@property='og:description']"
        ).get_attribute('content')

        # Parse prod page's metadata
        link_to_prod = self.driver.find_element_by_class_name(
            'wordfix'
        ).text.split(' ')[1]

        (
            prod_detail['link'],
            prod_detail['thumbnail'],
            prod_detail['title'],
            prod_detail['id'],
        ) = meta_from_prod_detail_page(link_to_prod)

        return prod_detail
