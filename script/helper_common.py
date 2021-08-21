"""Common helper functions"""


import hashlib
import re
from urllib.parse import urlparse

from bs4 import BeautifulSoup as bs
import requests

from exception import NotAnUrlError, InvalidMetadataError


def meta_from_prod_detail_page(link_to_prod):
    """
    return: link, thumbnail, title, id
    """
    try:
        return _meta_from_prod_detail_page(link_to_prod)
    except (InvalidMetadataError, NotAnUrlError, ConnectionError):
        return None


def _meta_from_prod_detail_page(link_to_prod):
    url_parsed = urlparse(link_to_prod)

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/88.0.4324.96 Safari/537.36"
    }

    if '.' in url_parsed.netloc:
        res = requests.get(link_to_prod, headers=headers)
        if res.status_code == 200:
            link = res.url
        else:
            raise ConnectionError(link_to_prod)
    else:
        raise NotAnUrlError(f'Invalid URL detected : {link_to_prod}')

    soup = bs(res.text, features="html.parser")
    thumbnail_meta = soup.find('meta', {"property": "og:image"})
    thumbnail = "https://buzzi.store/buzzi-store-logo.png"
    if thumbnail_meta is not None and "content" in thumbnail_meta:
        # Check whether thumbnail link is reachable
        res = requests.get(thumbnail_meta["content"], headers=headers)
        if res.status_code == 200:
            thumbnail = thumbnail_meta["content"]

    og_title_meta = soup.find('meta', {"property": "og:title"})
    og_title = ""
    if og_title_meta is not None and "content" in og_title_meta:
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
