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
        session.add_all(values)
        session.commit()
