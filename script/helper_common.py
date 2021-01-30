import requests
import hashlib

from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse

from exception import *


def meta_from_prod_detail_page(link_to_prod):
    """
    return: link, thumbnail, title, id
    """
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
            link = res.url
        else:
            raise ConnectionError
    else:
        raise NotAnUrlError(f'Invalid URL detected : {link_to_prod}')

    soup = bs(res.text, features="html.parser")
    try:
        thumbnail = soup.find('meta', {"property": "og:image"})['content']
        title = soup.find('meta', {"property": "og:title"})['content']
        id = hashlib.sha1(title.encode()).hexdigest()
    except:
        raise InvalidMetadataError(
            'This website does not provide valid meta tags.'
        )

    return link, thumbnail, title, id