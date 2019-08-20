#!/usr/bin/python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from SqlDeclarative import Petrol_Transactions
from SqlDeclarative import DbEngine

class SqlAdapter(object):
    def __init__(self):
        self.engine = DbEngine
        self.Session = sessionmaker(bind=self.engine)

    def Append(self, values):
        session = self.Session()

        cList = self.GetExistingEntites(values)
        curVl = session.query(Petrol_Transactions).filter(Petrol_Transactions.Transaction_Id.in_(cList)).all()
        for vl in values:
            if vl in curVl:
                ind = curVl.index(vl)
                curVl[ind].UpdateByValue(vl)
            else:
                session.add(vl)

        #session.add_all(values)
        session.commit()

    def GetExistingEntites(self, values):
        retVal = []
        for vl in values:
            retVal.append(vl.Transaction_Id)
        return retVal