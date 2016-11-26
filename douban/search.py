# coding=utf-8
# author@alingse
# 2016.08.04

import requests
from pyquery import PyQuery as pq

from random import choice

user_agents = [
    'Mozilla/4.8 [en] (Windows NT 6.0; U)',
    '(Windows Vista) Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
    'Mozilla/5.0 (X11; U; Linux; i686; en-US; rv:1.6) Gecko Debian/1.6-7',
    'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/125.2 (KHTML, like Gecko) Safari/125.8',
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36",
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


def search_pc(text):
    url = 'https://book.douban.com/subject_search'
    params = {
        'search_text': text,
        'cat': 1001
        }
    headers = {
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Host": "book.douban.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Upgrade-Insecure-Requests": "1",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Referer": "https://book.douban.com/",
        "User-Agent": choice(user_agents)
        }
    cookies = {
        "_pk_ref.100001.3ac3": "%5B%22%22%2C%22%22%2C1471834877%2C%22https%3A%2F%2Fwww.douban.com%2Fsearch%3Fq%3D9787302275954%22%5D",
        "__utmz": "81379588.1471675184.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic|utmctr=%E8%B1%86%E7%93%A3",
        "gr_cs1_941838d9-f372-4092-90be-f60196e8cf53": "user_id%3A0",
        "gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03": "941838d9-f372-4092-90be-f60196e8cf53",
        "bid": "\"H9+6qvsgiqk\"",
        "_vwo_uuid_v2": "8A3D4A933CECBF41BD1587AD9EAABFD5|f3ce0227957076158f7ccf32f73dc507",
        "ap": "1",
        "_pk_id.100001.3ac3": "784b73e1bf8c96ac.1471675185.3.1471834877.1471679343.",
        "_pk_ses.100001.3ac3": "*",
        "gr_user_id": "398c9c6a-039b-4389-8900-fb2f336c0d43",
        "__utma": "81379588.1761734391.1471675184.1471675184.1471679343.2",
        "ll": "\"118318\"",
        }

    try:
        r = requests.get(
            url,
            headers=headers,
            params=params,
            cookies=cookies,
            timeout=3)

        html = r.content.decode('utf-8')
        if r.status_code != 200:
            return False
    except Exception:
        return None

    htmld = pq(html)
    booklist = []
    items = htmld('.subject-list')('.subject-item')
    for i in range(len(items)):
        item = items.eq(i)
        book = {}
        book['img'] = item('.pic')('img').attr('src')
        bookurl = item('.info')('a').attr('href')
        ek = bookurl.rfind('/')
        sk = bookurl.rfind('/', 0, ek)
        book['id'] = bookurl[sk+1:ek]
        book['url'] = bookurl
        book['title'] = item('.info')('a').attr('title')
        book['rating_nums'] = item('.star')('.rating_nums').text()
        book['p'] = item('.star')('.pl').text()[1:-4]

        booklist.append(book)

    return booklist

if __name__ == '__main__':
    name = '9780262182539'
    # name = u'机器学习'
    booklist = search_pc(name)
    print(booklist)
