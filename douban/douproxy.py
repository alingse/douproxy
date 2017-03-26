# coding=utf-8
# author@alingse
# 2016.08.10

import functools
import json

from weppy import App
from weppy import Cache
from weppy import request
from weppy import response
from weppy import sdict
from weppy.cache import DiskCache

from apiv2_frodo import id_url
from apiv2_frodo import isbn_url
from apiv2_frodo import get_info as get_info_byurl

from apiv2 import get_info as get_info_byid
from search import search_pc

from const import const


app = App(__name__)

app.config.logging.logfile = sdict(
    level="debug",
    max_size=100*1024*1024
)

cache = Cache(disk=DiskCache())
cache.clear = cache.disk.clear


def vjson(version):
    def jsonresp(func):
        @functools.wraps(func)
        def dumpjson(*args, **kwargs):
            response.headers['Content-Type'] = 'application/json; charset=utf-8'
            obj = func(*args, **kwargs)
            obj['version'] = version
            return json.dumps(obj, ensure_ascii=False).encode('utf-8')
        return dumpjson
    return jsonresp


def gen_code_info(code, data=None):
    info = {
        'code': code,
        'msg': const.MSG[code],
        'data': data,
    }
    app.log.error(u'gen info code:%d, msg:%s', code, const.MSG[code])
    return info


def gen_err(code):
    # request.path
    # app.log.error('')    
    return gen_code_info(code)


def search_bookid(text):
    def cache_search():
        return search_pc(text.decode('utf-8'))

    status, booklist = cache(text, cache_search, 60)

    if status is None:
        cache.clear(key=text)
        return gen_err(const.TIMEOUT)
    elif status is False:
        cache.clear(key=text)
        return gen_err(const.FORBIDDEN)
    elif type(booklist) != list:
        cache.clear(key=text)
        return gen_err(const.UNKNOW_ERR)

    if len(booklist) == 0:
        app.log.error('not found')
        return gen_err(const.NOT_FOUND)
    return booklist[0]['id']


def bookinfo_v1(bookid):
    def cache_get_v1():
        return get_info_byid(bookid)

    status, info = cache(bookid, cache_get_v1, const.CACHE_TIME)

    app.log.info('v1:bookid:%s, info-status:%d', bookid, status)

    if status is True:
        return gen_code_info(const.SUCCESS, data=info)
    elif status is False:
        cache.clear(key=bookid)
        return gen_err(const.TIMEOUT)
    elif status == 404:
        return gen_err(const.NOT_FOUND)
    elif status == 403:
        cache.clear(key=bookid)
        return gen_err(const.FORBIDDEN)
    else:
        app.log.info('v1:bookid:%s, status:%s, content:%s', bookid, status, info)

        cache.clear(key=bookid)        
        return gen_err(const.UNKNOW_ERR)


def bookinfo_v2(url):
    def cache_get_v2():
        return get_info_byurl(url)

    info = cache(url, cache_get_v2, const.CACHE_TIME)

    app.log.info('v1:bookurl:%s, info-status:-', url)

    if info is None:
        return gen_err(const.TIMEOUT)
    elif 'code' not in info:
        return gen_code_info(const.SUCCESS, data=info)

    code = info['code']

    if code == 404:
        return gen_err(const.NOT_FOUND)
    elif code == 403:
        cache.clear(key=url)
        return gen_err(const.FORBIDDEN)
    else:
        app.log.error('v2:bookurl:%s, status: %s,content: %s', url, code, info)

        cache.clear(key=url)
        return gen_err(const.UNKNOW_ERR)


@app.route('/api/v1.0/book/isbn/<int:isbn>')
@app.route('/api/v1.0/book/name/<str:name>')
@app.route('/api/v1.0/book/<int:bookid>')
@vjson(version='1.0')
def book_pc_v1(isbn=None, bookid=None, name=None):
    text = None
    if isbn:
        text = isbn
    elif name:
        text = name.strip()

    if not bookid:
        result = search_bookid(text)
        if isinstance(result, dict):
            return result
        
        bookid = result
        app.log.info('search:text:%s, bookid:%s', text, bookid)
    return bookinfo_v1(bookid)


@app.route('/api/v1.1/book/isbn/<int:isbn>')
@app.route('/api/v1.1/book/<int:bookid>')
@vjson(version='1.1')
def book_v2_v1(isbn=None, bookid=None):
    if isbn:
        url = isbn_url(isbn)
    elif bookid:
        url = id_url(bookid)

    result = bookinfo_v2(url)
    if result['code'] != const.SUCCESS:
        return result

    bookid = result['data']['id']
    return bookinfo_v1(bookid)


@app.route('/api/v2.0/book/isbn/<int:isbn>')
@app.route('/api/v2.0/book/<int:bookid>')
@vjson(version='2.0')
def book_v2(isbn=None, bookid=None):
    if isbn:
        url = isbn_url(isbn)
    elif bookid:
        url = id_url(bookid)

    return bookinfo_v2(url)


if __name__ == '__main__':
    app.run(host=const.ALLOW_HOST, port=const.PORT)
