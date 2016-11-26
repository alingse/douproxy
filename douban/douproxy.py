# coding=utf-8
# author@alingse
# 2016.08.10

import functools
import json

from weppy import App
from weppy import Cache
from weppy.cache import DiskCache
from weppy import response
from weppy import sdict

from apiv2_frodo import id_url
from apiv2_frodo import isbn_url
from apiv2_frodo import get_info as get_info_byurl

from apiv2 import get_info as get_info_byid
from search import search_pc

from const import const


app = App(__name__)

cache = Cache(disk=DiskCache())

app.config.logging.logfile = sdict(
    level="debug",
    max_size=10*1024*1024,
    on_app_debug=True,
)


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
    # log
    app.log.warning(u'gen info code:{},msg:{}'.format(code, const.MSG[code]))

    info = {
        'code': code,
        'msg': const.MSG[code],
        'data': data,
    }
    return info

gen_err = gen_code_info


def bookinfo_v1(bookid):
    def cache_get_v1():
        return get_info_byid(bookid)

    status, info = cache(bookid, cache_get_v1, 3*24*60*60)
    app.log.info('v1:bookid:{},info-status:{}'.format(bookid, status))

    if status is True:
        return gen_code_info(const.SUCCESS, data=info)
    if status is False:
        cache.clear(key=bookid)
        return gen_err(const.TIMEOUT)
    if status == 404:
        return gen_err(const.NOT_FOUND)
    if status == 403:
        cache.clear(key=bookid)
        return gen_err(const.FORBIDDEN)
    # unknow
    app.log.debug('v1:{},http:{},content:{}'.format(bookid, status, info))
    cache.clear(key=bookid)
    return gen_err(const.UNKNOW_ERR)


def bookinfo_v2(url):
    def cache_get_v2():
        return get_info_byurl(url)

    info = cache(url, cache_get_v2, 3*24*60*60)
    app.log.info('v2:bookurl:{},info'.format(url))

    if info is None:
        return gen_err(const.TIMEOUT)
    if 'code' not in info:
        return gen_code_info(const.SUCCESS, data=info)

    code = info['code']
    if code == 404:
        return gen_err(const.NOT_FOUND)
    if code == 403:
        cache.clear(key=url)
        return gen_err(const.FORBIDDEN)

    # unknow
    app.log.debug('v2:bookurl:{},info:http:{},content:{}'.format(url, code, info))
    cache.clear(key=url)
    return gen_err(const.UNKNOW_ERR)


@app.route('/api/v1.0/book/isbn/<int:isbn>')
@app.route('/api/v1.0/book/name/<str:name>')
@app.route('/api/v1.0/book/<int:bookid>')
@vjson(version='1.0')
def book_pc_v1(isbn=None, bookid=None, name=None):
    text = None
    if isbn is not None:
        text = isbn
    if name is not None:
        text = name.strip()

    def cache_search():
        return search_pc(text.decode('utf-8'))

    if bookid is None and text is not None:
        # req search
        booklist = cache(text, cache_search, 15)
        # search err

        if len(booklist) == 0:
            return gen_err(const.NOT_FOUND)

        if type(booklist) != list:
            app.log.info('search:text:{},booklist:{}'.format(text, booklist))
            if booklist is None:
                cache.clear(key=text)
                return gen_err(const.TIMEOUT)
            elif booklist is False:
                cache.clear(key=text)
                return gen_err(const.FORBIDDEN)
            else:
                cache.clear(key=text)
                return gen_err(const.UNKNOW_ERR)

        # search true/ choose first
        bookid = booklist[0]['id']
        app.log.info('search:text:{},bookid:{}'.format(text, bookid))

    return bookinfo_v1(bookid)


@app.route('/api/v1.1/book/isbn/<int:isbn>')
@app.route('/api/v1.1/book/<int:bookid>')
@vjson(version='1.1')
def book_v2_v1(isbn=None, bookid=None):
    if isbn is not None:
        url = isbn_url(isbn)
    if bookid is not None:
        url = id_url(bookid)

    res = bookinfo_v2(url)
    if res['code'] != const.SUCCESS:
        return res

    bookid = res['data']['id']
    return bookinfo_v1(bookid)


@app.route('/api/v2.0/book/isbn/<int:isbn>')
@app.route('/api/v2.0/book/<int:bookid>')
@vjson(version=2.0)
def book_v2(isbn=None, bookid=None):
    if isbn is not None:
        url = isbn_url(isbn)
    if bookid is not None:
        url = id_url(bookid)

    return bookinfo_v2(url)


if __name__ == '__main__':
    app.run(host=const.ALLOW_HOST, port=const.PORT, debug=False)
