#coding=utf-8
#author@alingse
#2016.08.07

from random import choice

import requests
import json
import sys

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

def get_info(id,category='book'):
    try:
        headers = {
            'User-Agent': choice(user_agents),
            'Accept': choice(accepts),
        }

        cookies = {
            'viewed':'"{}"'.format(id)
        }

        url = 'http://api.douban.com/v2/{}/{}'.format(category, id)
        r = requests.get(url,headers=headers,cookies=cookies,
                            timeout=3,allow_redirects=False)
        if r.status_code == 200:        
            return True,r.json()

        return r.status_code,r.content

    except Exception as e:
        return False,None

if __name__ == '__main__':
    id = '2708965'
    category='book'
    if len(sys.argv) == 2:
        id = sys.argv[1]
    if len(sys.argv) == 3:
        category = sys.argv[2]
    status,result = get_info(id,category)
    print(status)
    print(json.dumps(result,ensure_ascii=False).encode('utf-8'))

