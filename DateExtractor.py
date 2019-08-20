#!/usr/bin/python3

from datetime import datetime,timedelta

class DateExtractor(object):
    Interval = timedelta(days=45)
    def __init__(self):
        self.EndDt = datetime.today()
        self.StartDt = self.EndDt - DateExtractor.Interval

    def GetStartDtFormat(self):
        return self.StartDt.strftime('%d.%m.%Y')
    def GetEndDtFormat(self):
        return self.EndDt.strftime('%d.%m.%Y')
    def GetEndDtSqlFormat(self):
        return (self.EndDt + timedelta(days=1)).strftime('%Y-%m-%d')
    def GetStartSqlFormat(self):
        return self.StartDt.strftime('%Y-%m-%d')
