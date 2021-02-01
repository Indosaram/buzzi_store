import requests
import hashlib
import re

from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse

from exception import *


def meta_from_prod_detail_page(link_to_prod):
    """
    return: link, thumbnail, title, id
    """
    url_parsed = urlparse(link_to_prod)

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
    }

    if '.' in url_parsed.netloc:
        try:
            res = requests.get(link_to_prod, headers=headers)
        except Exception as e:
            raise e
        if res.reason == 'OK':
            link = res.url
        else:
            raise ConnectionError
    else:
        raise NotAnUrlError(f'Invalid URL detected : {link_to_prod}')

    soup = bs(res.text, features="html.parser")
    try:
        thumbnail = soup.find('meta', {"property": "og:image"})['content']
        try:
            res = requests.get(thumbnail, headers=headers)
        except Exception as e:
            raise e
        if res.reason != 'OK':
            thumbnail = "https://buzzi.store/buzzi-store-logo.png"

        title = soup.find('meta', {"property": "og:title"})['content']
        id = hashlib.sha1(title.encode()).hexdigest()
    except:
        raise InvalidMetadataError(
            'This website does not provide valid meta tags.'
        )

    return link, thumbnail, title, id


def category_manager(category):
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

    return categories[category]


def price_regex(string):
    regex = re.compile(r"\d{1,}(,\d+)?원").search(string)
    return regex.group() if regex is not None else None