import json
import re
import requests
import platform

from bs4 import BeautifulSoup as bs

from selenium_loader import SeleniumLoader


class PpomppuHelper:
    def __init__(self):
        if platform.system() == 'Windows':
            webdriver_path = 'C:\\chromedriver\\chromedriver.exe'
        else:
            webdriver_path = './chromedriver'
        self.driver = SeleniumLoader(webdriver_path).driver
        self.baseURL = 'http://www.ppomppu.co.kr/zboard/'
        self.boardURL = self.baseURL + 'zboard.php?id=ppomppu&hotlist_flag=999'

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

        for idx, route in enumerate(routes):
            print(f'-> Processing {idx+1}/{len(routes)}', end='\r')
            try:
                prod_details.append(self._get_product_data(route))
            except:
                continue
            print('')
        self.driver.close()

        return prod_details

    def _get_product_data(self, route):
        self.driver.get(self.baseURL + route)

        # Get product details
        prod_detail = {}

        # this part is little treaky, better find another approach later
        raw_title = self.driver.find_element_by_class_name('view_title2').text
        fragments = re.compile("\[(.+?)\]|\((.+?)\)").findall(raw_title)
        prod_detail['shop'] = fragments[0][0]
        prod_detail['price'], prod_detail['shipping'] = fragments[-1][1].split(
            '/'
        )
        prod_detail['title'] = ' '.join(raw_title.split(' ')[1:])

        innerHTML = self.driver.find_element_by_class_name(
            'sub-top-text-box'
        ).get_attribute('innerHTML')
        soup = bs(innerHTML, features="html.parser")

        prod_detail['date'] = (
            re.compile(r'\d\d\d\d-\d\d-\d\d').search(soup.text).group()
        )
        prod_detail['hit'] = re.compile(r'조회수: \d+').search(soup.text).group()
        link_original = self.driver.find_element_by_class_name(
            'wordfix'
        ).text.split(' ')[1]
        res = requests.get(link_original)
        if res.reason == 'OK':
            prod_detail['link'] = res.url
        else:
            raise KeyError

        innerHTML = self.driver.find_element_by_class_name(
            'board-contents'
        ).get_attribute('innerHTML')
        soup = bs(innerHTML, features="html.parser")
        img_selector = soup.select_one('img')
        prod_detail['img'] = (
            f"https:{str(img_selector['src'])}"
            if img_selector is not None
            else None
        )

        return prod_detail

    def save_json(self, data):
        jsondata = {"data": data}
        with open("productsData.json", "w", encoding='utf-8') as f:
            json.dump(jsondata, f, ensure_ascii=False, indent=4)
        print('Finish saving .json')


if __name__ == '__main__':
    ph = PpomppuHelper()
    prod_details = ph.run()
    ph.save_json(prod_details)
