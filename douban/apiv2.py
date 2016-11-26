# coding=utf-8
# author@alingse
# 2016.08.07

# from random import choice
import requests
import uuid
import json


user_agents = [
    'Mozilla/4.8 [en] (Windows NT 6.0; U)',
    '(Windows Vista) Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
    'Mozilla/5.0 (X11; U; Linux; i686; en-US; rv:1.6) Gecko Debian/1.6-7',
    'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/125.2 (KHTML, like Gecko) Safari/125.8',
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.4) Gecko Netscape/7.1 (ax)',
    'Mozilla/5.0 (Windows; U; Windows XP) Gecko MultiZilla/1.6.1.0a',
    'Opera/9.20 (Windows NT 6.0; U; en)',
    'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0 )',
    'Mozilla/5.0 (X11; U; Linux; i686; en-US; rv:1.6) Gecko Debian/1.6-7',
    'Links/0.9.1 (Linux 2.4.24; i386;)',
    'python-requests/2.7.0 CPython/2.7.10 Linux/4.2.0-16-generic',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/45.0.2454.101 Chrome/45.0.2454.101 Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
]

accepts = [
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    '*/*',
]


def get_info(id, category='book'):
    try:
        headers = {
            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Host": "api.douban.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Upgrade-Insecure-Requests": "1",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"
        }

        cookies = {
            "ps": "y",
            "__utmz": "30149280.1476369702.7.6.utmcsr=baidu|utmccn=(organic)|utmcmd=organic",
            "regpop": "1",
            "bid": "5-PQxwnaP2E",
            "__utmt_douban": "1",
            "__utmt": "1",
            "ap": "1",
            "gr_user_id": str(uuid.uuid4()),
            "__utma": "30149280.1766249388.1473671047.1475685017.1476369702.7",
            "__utmb": "30149280.8.10.1476369702",
            "__utmc": "30149280",
            "ll": "\\\"108288\\\"",
            "viewed": "\\\"{}\\\"".format(id),
            "ct": "y"
        }

        url = 'https://api.douban.com/v2/{}/{}'.format(category, id)
        r = requests.get(
            url,
            headers=headers,
            cookies=cookies,
            timeout=3,
            allow_redirects=False)

        code = r.status_code
        if code == 200:
            return True, r.json()
        return code, r.content
    except Exception:
        pass

    return False, None


if __name__ == '__main__':
    import sys

    id = '2708965'
    category = 'book'
    if len(sys.argv) >= 2:
        id = sys.argv[1]
        category = sys.argv[2]

    status, result = get_info(id, category)
    print(status)
    print(json.dumps(result, ensure_ascii=False).encode('utf-8'))
