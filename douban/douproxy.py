#coding=utf-8
#author@alingse
#2016.08.10


from weppy import App
from weppy import Cache
from weppy.cache import DiskCache
#from weppy import request
from weppy import response
from weppy import sdict

#from weppy.tools import service

app = App(__name__)

cache = Cache(disk=DiskCache())

#for log
app.config.logging.logfile = sdict(
    level="warning",
    max_size=10*1024*1024,
    on_app_debug=True,
)


from apiv2_frodo import id_url
from apiv2_frodo import isbn_url
from apiv2_frodo import get_info as get_info_byurl

from apiv2 import get_info as get_info_byid
from search import search_pc

import const

import json

def vjson(version):
    def jsonresp(func):
        def dumpjson(*args,**kwargs):
            response.headers['Content-Type'] = 'application/json; charset=utf-8'
            obj = func(*args,**kwargs)
            obj['version'] = version
            return json.dumps(obj,ensure_ascii=False).encode('utf-8')
        return dumpjson
    return jsonresp


def gen_code_info(code,data=None):
    #log
    app.log.info(u'gen info code:{},msg:{}'.format(code,const.MSG[code]))

    info = {
        'code':code,
        'msg':const.MSG[code],
        'data':data,
    }
    return info

gen_err = gen_code_info


def bookinfo_v1(bookid):
    def cache_get_v1():
        res = get_info_byid(bookid)
        return res

    status,info = cache(bookid,cache_get_v1,3*24*60*60)
    app.log.info('v1:bookid:{},info-status:{}'.format(bookid,status))

    if status == True:
        return gen_code_info(const.SUCCESS,data=info)
    if status == False:
        return gen_err(const.TIMEOUT)
    if status == 404:
        return gen_err(const.NOT_FOUND)
    if status == 403:
        return gen_err(const.FORBIDDEN)
    #unknow
    app.log.debug('v1:{},http:{},content:{}'.format(bookid,status,info))
    return gen_err(const.UNKNOW_ERR)


def bookinfo_v2(url):
    def cache_get_v2():
        res = get_info_byurl(url)
        return res

    info = cache(url,cache_get_v2,3*24*60*60)
    app.log.info('v2:bookurl:{},info'.format(url))

    if info == None:
        return gen_err(const.TIMEOUT)
    if 'code' not in info:
        return gen_code_info(const.SUCCESS,data=info)

    code = info['code']
    if code == 404:
        return gen_err(const.NOT_FOUND)
    if code == 403:
        return gen_err(const.FORBIDDEN)
    #unknow
    app.log.debug('v2:bookurl:{},info:http:{},content:{}'.format(url,code,info))
    return gen_err(const.UNKNOW_ERR)


@app.route('/api/v1.0/book/isbn/<int:isbn>')
@app.route('/api/v1.0/book/name/<str:name>')
@app.route('/api/v1.0/book/<int:bookid>')
@vjson(version=1.0)
def book_pc_v1(isbn=None,bookid=None,name=None):
    search_text = None
    if isbn != None:
        text_key = isbn
        search_text = isbn
    if name != None:
        text_key = name.strip()
        search_text = name.strip().decode('utf-8')
    
    def cache_search():
        res = search_pc(search_text)
        return res

    if bookid == None and search_text != None:
        #req search
        booklist = cache(text_key,cache_search,15)
        #search err
        if type(booklist) != type([]) or len(booklist) == 0:
            app.log.info('search:text:{},booklist:{}'.format(text_key,booklist))
            if booklist == None:
                return gen_err(const.TIMEOUT)
            elif booklist == []:
                return gen_err(const.NOT_FOUND)
            elif booklist == False:
                return gen_err(const.FORBIDDEN)
            else:
                return gen_err(const.UNKNOW_ERR)
        #search true
        bookid = booklist[0]['id']
        app.log.info('search:text:{},bookid:{}'.format(text_key,bookid))
    return bookinfo_v1(bookid)


@app.route('/api/v1.1/book/isbn/<int:isbn>')
@vjson(version=1.1)
def book_v2_v1(isbn=None,bookid=None):
    if isbn != None:
        url = isbn_url(isbn)
    if bookid != None:
        url = id_url(bookid)
    
    res = bookinfo_v2(url)
    if res['code'] != const.SUCCESS:
        return res

    bookid = res['data']['id']    
    return bookinfo_v1(bookid)


@app.route('/api/v2.0/book/isbn/<int:isbn>')
@app.route('/api/v2.0/book/<int:bookid>')
@vjson(version=2.0)
def book_v2(isbn=None,bookid=None):
    if isbn != None:
        url = isbn_url(isbn)
    if bookid != None:
        url = id_url(bookid)

    return bookinfo_v2(url)


if __name__ == '__main__':
    app.run(host=const.ALLOW_HOST, port=const.PORT,debug=True)
