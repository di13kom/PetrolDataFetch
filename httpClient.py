#!/usr/bin/python3

from http import client
import urllib.parse
import zlib
from http import cookies
from http import HTTPStatus
import time
import json
import sys
from SqlAdapter import SqlAdapter
from SqlDeclarative import Petrol_Transactions
from datetime import datetime
from CookieManager import CookieManager


class DataFetcher(object):
    def __init__(self, fileN):
        with open(fileN) as fl:
            obj = json.load(fl)
            self.Site = obj['SiteUrl']
            self.UserName = obj['UserName']
            self.UserPassword = obj['Password']
        self.CookieManager = CookieManager()
        self.SqlAdapter = SqlAdapter()
        self.MainConnection = client.HTTPSConnection(self.Site)

    def GetUrl(self, url):
        self.MainConnection.request("GET", url)
        response = self.MainConnection.getresponse()
        print('GetUrl status:', response.status, response.reason)
        self.CookieManager.LoadFromString(response.getheader('Set-Cookie'))
        print('---inCookie GetUrl:\n' + self.CookieManager.GetOutput() + '\n----')
        response.read()
        #print(response.getheaders())

    def GetUrlJson(self, url):
        headers =   {
                        "Accept": "application/json, text/plain, */*",
                        "Accept-Encoding": "gzip, deflate, br",
                        #"Accept-Language": "ru-RU,en;q=0.9",
                        #"Connection": "keep-alive",
                        "Cookie": self.CookieManager.GetCurrentCookiesString(),
                        "Host": self.Site,
                        "Referer": "https://online.petrolplus.ru/transactions",
                        #"User-Agent": "Mozilla",
                        "DNT":"1",
                    }

        self.MainConnection.request("GET", url, headers=headers)
        response = self.MainConnection.getresponse()
        print('---GetUrlJson status: %s, reason: %s, prtotcol version: %s---'%( response.status, response.reason, response.version))

        print('---inCookie GetUrlJson:\n' + self.CookieManager.GetOutput() + '\n----')

        contentType = response.getheader('Content-Encoding')
        content = response.read()

        if contentType == 'gzip':
            content = zlib.decompress(content, zlib.MAX_WBITS|16)
        elif contentType == 'deflate':
            content = zlib.decompress(content, -zlib.MAX_WBITS)

        content = content.decode('utf-8')
        jsonContent = json.loads(content, encoding='utf-8')
        #print(jsonContent)
        transactions = []
        for val in jsonContent.get('transactions'):
            transactions.append(
                Petrol_Transactions(
                    Transaction_Id = val['idTrans']
                    , CardNum = val['cardNum']
                    , Date = datetime.strptime(val['date'][:-3],"%Y-%m-%dT%H:%M:%S")
                    , ServicePointDescription = val['idPos']
                    , CardHolder = val['holder']
                    , ServicePointAddress = val['posAddress']
                    , OperationDescription = val['typeName']
                    , ServiceDescription = val['serviceName']
                    , Amount = val['amount']
                    , Price = val['price']
                    , OverAllPrice = val['summa']
                    , Discount = val['discount']
                )
            )

        self.SqlAdapter.Append(transactions)
            

    def TryLogin(self, url):
        
        params = urllib.parse.urlencode({'username':self.UserName, 'password':self.UserPassword})
        headers =   {
                        "Accept": "application/json, text/plain, */*",
                        "Accept-Encoding": "gzip, deflate, br",
                        #"Accept-Language": "ru-RU,en;q=0.9",
                        #"Connection": "keep-alive",
                        "Cookie": self.CookieManager.GetCurrentCookiesString(),
                        "Content-Type": "application/x-www-form-urlencoded",
                        "Host": self.Site,
                        "Referer": "https://online.petrolplus.ru/",
                        #"User-Agent": "Mozilla",
                        "DNT":"1",
                        "X-Compress": "null"
                    }

        self.MainConnection.request("POST", url, params, headers)
        response = self.MainConnection.getresponse()
        print('TryLogin status: %s, reason: %s, prtotcol version: %s'%( response.status, response.reason, response.version))
        #if(response.status == HTTPStatus.OK):
        #print(response.getheaders())

        cookStr = response.getheader('Set-Cookie')
        print('---inCookie TryLogin:\n' + cookStr + '\n----')
        self.CookieManager.CookiesSessionWorkAround(cookStr)
        #print('Cookies: %s'%(self.Cookies))

        contentType = response.getheader('Content-Encoding')
        content = response.read()

        if contentType == 'gzip':
            content = zlib.decompress(content, zlib.MAX_WBITS|16)
        elif contentType == 'deflate':
            content = zlib.decompress(content, -zlib.MAX_WBITS)

        content = content.decode('utf-8')
        jsonContent = json.loads(content, encoding='utf-8')
        print(jsonContent)

    def Close(self):
        self.MainConnection.close()


def main():
    obj = DataFetcher('settings.json')
    obj.GetUrl('/')
    #time.sleep(1)
    obj.TryLogin('/api/v1/login')
    obj.GetUrlJson('/api/v1/transactions/main/dateFrom/01.05.2018/dateTo/31.08.2018/?isOnlySusp=false&format=JSON&limit=1000&offset=0&refresh=0&sortBy=DATE&sortOrder=DESC')
    obj.Close()



if __name__ == "__main__":
    main()
