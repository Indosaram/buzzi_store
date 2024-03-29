"""Common helper functions"""


import hashlib
import socket
import re
from urllib.parse import urlparse

from bs4 import BeautifulSoup as bs
from requests.models import InvalidURL
from selenium_helper.selenium_loader import SeleniumLoader
from selenium.common.exceptions import TimeoutException
import requests

from exception import NotAnUrlError, InvalidMetadataError, UrlUnreachableError


def meta_from_prod_detail_page(link_to_prod):
    """
    return: link, thumbnail, title, id
    """
    try:
        return _meta_from_prod_detail_page(link_to_prod)
    except (
        InvalidMetadataError,
        NotAnUrlError,
        ConnectionError,
        UrlUnreachableError,
        socket.gaierror,
    ):
        return None


def _meta_from_prod_detail_page(link_to_prod):
    url_parsed = urlparse(link_to_prod)

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/88.0.4324.96 Safari/537.36"
    }

    if '.' in url_parsed.netloc:
        try:
            res = requests.get(link_to_prod, headers=headers)
            if res.status_code == 200:
                link = res.url
            else:
                raise ConnectionError(link_to_prod)
        except Exception as exc:
            raise ConnectionError(link_to_prod) from exc

    else:
        raise NotAnUrlError(f'Invalid URL detected : {link_to_prod}')

    driver = SeleniumLoader().driver
    try:
        driver.get(link_to_prod)
    except TimeoutException as exc:
        raise UrlUnreachableError(link_to_prod) from exc

    soup = bs(driver.page_source, features="html.parser")

    thumbnail_meta = soup.find('meta', {"property": "og:image"})
    thumbnail = "https://buzzi.store/no_thumbnail.png"
    if thumbnail_meta is not None and "content" in thumbnail_meta.attrs:
        # Check whether thumbnail link is reachable
        thumbnail_url = thumbnail_meta["content"]
        parsed_url = urlparse(thumbnail_url)
        if parsed_url.scheme:
            url = thumbnail_meta["content"]
        else:
            url = (
                f"{url_parsed.scheme}://{url_parsed.netloc}"
                f"{thumbnail_meta['content']}"
            )

        try:
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                thumbnail = thumbnail_meta["content"]
        except InvalidURL:
            print("Invalid thumbnail URL. Using default image.")

    og_title_meta = soup.find('meta', {"property": "og:title"})
    og_title = ""
    if og_title_meta is not None and "content" in og_title_meta.attrs:
        og_title = og_title_meta["content"]

    title_meta = soup.find('title')
    title = ""
    if title_meta is not None:
        title = title_meta.text

    if title is None and og_title is None:
        raise InvalidMetadataError(
            f"This website does not provide valid meta tags: {link_to_prod}"
        )

    title = max([title, og_title], key=len)
    item_id = hashlib.sha1(title.encode()).hexdigest()

    return link, thumbnail, title, item_id


def category_manager(category):
    """Pre-defined categories"""
    categories = {
        **dict.fromkeys(
            ['인터넷', '이벤트', '생활용품', '기타'],
            '기타',
        ),
        **dict.fromkeys(
            ['컴퓨터', 'PC관련'],
            '컴퓨터',
        ),
        **dict.fromkeys(
            [
                '모바일',
                '게임',
                '휴대폰',
                'A/V',
                '디지털',
                '게임S/W',
                '게임H/W',
            ],
            '게임/디지털',
        ),
        **dict.fromkeys(
            [
                '식품/건강',
                '식품',
                '음식',
            ],
            '식품/건강',
        ),
        **dict.fromkeys(
            ['도서', '서적'],
            '서적',
        ),
        **dict.fromkeys(
            [
                '가전',
                '가전/가구',
                'PC/가전',
            ],
            '가전/가구',
        ),
        **dict.fromkeys(
            [
                '육아',
                '육아용품',
            ],
            '육아',
        ),
        **dict.fromkeys(
            [
                '쿠폰',
                '상품권',
            ],
            '상품권',
        ),
        **dict.fromkeys(
            ['의류', '의류/잡화'],
            '의류/잡화',
        ),
        **dict.fromkeys(
            ['화장품'],
            '화장품',
        ),
        **dict.fromkeys(
            ['인테리어'],
            '인테리어',
        ),
        **dict.fromkeys(
            ['취미용품', '레저용품', '등산/캠핑'],
            '취미/레저',
        ),
    }
    if category in categories.keys():
        return categories[category]

    return None


def price_regex(string):
    """Extract price from a given string"""
    regex = re.compile(r"\d{1,}(,\d+)?원").search(string)
    return regex.group() if regex is not None else None
