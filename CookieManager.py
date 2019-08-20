#!/usr/bin/python3

from http import cookies


class CookieManager(object):
    def __init__(self):
        self.Cookies = cookies.SimpleCookie()

    def GetCurrentCookiesString(self):
        cList = []
        cookieString = ''
        for k,v in self.Cookies.items():
            cList.append(k + '=' + v.coded_value)
        cookieString = '; '.join(cList)
        return cookieString

    def CookiesSessionWorkAround(self, cookieString):
        splStr = cookieString.split(',',maxsplit=1)
        for v in splStr:
            self.Cookies.update(cookies.SimpleCookie(v))

    def LoadFromString(self, inStr):
        self.Cookies.load(inStr)

    def GetOutput(self):
        return self.Cookies.output()
