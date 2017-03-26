# coding=utf-8
# 2016.08.07


class _const:
    class ConstError(TypeError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const{0}".format(name))

        if not name.isupper():
            raise TypeError("Need to bind uppercase")

        self.__dict__[name] = value

const = _const()

const.SUCCESS = 100000
const.NOT_FOUND = 200404
const.TIMEOUT = 200504
const.FORBIDDEN = 200403
const.UNKNOW_ERR = 200999

const.MSG = {
    const.SUCCESS: u'sucess',
    const.NOT_FOUND: u'notfound',
    const.TIMEOUT: u'timeout',
    const.FORBIDDEN: u'forbidden',
    const.UNKNOW_ERR: u'unknow'
}

const.CACHE_TIME = 3 * 24 * 60 * 60
const.PORT = 8001
const.ALLOW_HOST = '127.0.0.1'
