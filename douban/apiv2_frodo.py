# coding=utf-8
# author@alingse
# 2016.08.10

import requests
import json


def isbn_url(isbn):
    url = 'https://frodo.douban.com/api/v2/book/isbn/' + isbn
    return url


def id_url(id):
    url = 'https://frodo.douban.com/api/v2/book/' + id
    return url


def get_info(url):
    params = {
        'udid': 'f24597395651dee27bb216ebe5a89b2e7400e6c4',
        'device_id': 'f24597395651dee27bb216ebe5a89b2e7400e6c4',
        'apiKey': '0dad551ec0f84ed02907ff5c42e8ec70',
        'channel': 'Douban',
        'os_rom': 'android'
    }

    headers = {
        'User-Agent': 'api-client/1 com.douban.frodo/4.1.1.1(71) Android/21 ALE-UL00 HUAWEI ALE-UL00  rom:android',
        'Accept-Encoding': 'gzip',
        'host': 'frodo.douban.com',
        # 'Connection': 'Keep-Alive'
    }

    try:
        r = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=3)

        return r.json()
    except Exception:
        pass

if __name__ == '__main__':
    isbn = '9787302275954'
    url = isbn_url(isbn)
    result = get_info(url)
    print(json.dumps(result, ensure_ascii=False))

    id = '10590856'
    url = id_url(id)
    result = get_info(url)
    print(json.dumps(result, ensure_ascii=False))
