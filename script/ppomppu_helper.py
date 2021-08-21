"""Ppomppu helper class"""

import re

from bs4 import BeautifulSoup as bs
from selenium_helper.selenium_loader import SeleniumLoader

from helper_common import category_manager, meta_from_prod_detail_page


class PpomppuHelper:
    """Ppomppu Helper class"""

    def __init__(self, param_common, param_ppompu):
        self.driver = SeleniumLoader().driver
        self.json_path = param_common['json_path']
        self.base_url = param_ppompu['base_url']
        self.board_url = param_ppompu['board_url']

    def run(self):
        """Run crawling"""
        self.driver.get(self.board_url)
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
            product_data = self._get_product_data(route)
            if product_data is not None:
                prod_details.append(product_data)
        print(f'✅ Processed {len(prod_details)}/{len(routes)} entries')
        self.driver.close()

        return prod_details

    def _get_product_data(self, route):
        self.driver.get(self.base_url + route)

        if '품절 / 종결 / 취소된 게시물입니다.' in self.driver.page_source:
            print("This deal is already closed.")
            return None

        # Get product details
        prod_detail = {}
        prod_detail['origin'] = "뽐뿌"

        # this part is little tricky, better find another approach later
        try:
            raw_title = self.driver.find_element_by_class_name(
                'view_title2'
            ).text
            fragments = re.compile(r"\[(.+?)\]|\((.+?)\)").findall(raw_title)
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

        inner_html = self.driver.find_element_by_class_name(
            'sub-top-text-box'
        ).get_attribute('innerHTML')
        soup = bs(inner_html, features="html.parser")

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
        pre_category = (re.compile(r'분류: \w+').search(soup.text).group()).split(
            ' '
        )[1]
        prod_detail['category'] = category_manager(pre_category)

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

        result = meta_from_prod_detail_page(link_to_prod)
        if result is not None:
            (
                prod_detail['link'],
                prod_detail['thumbnail'],
                prod_detail['title'],
                prod_detail['id'],
            ) = result
        else:
            return None

        return prod_detail
