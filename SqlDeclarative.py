#!/usr/bin/python3

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, func, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Petrol_Transactions(Base):
    __tablename__ = 'Petrol_Transactions'
    id = Column(Integer, primary_key = True)
    Transaction_Id = Column(String, unique = True, index = True, nullable=False)
    CardNum = Column(Integer)
    Date = Column(DateTime(timezone = True))
    #Date = Column(DateTime(timezone = True), default = func.utcnow())
    ServicePointDescription = Column(String)
    CardHolder = Column(String)
    ServicePointAddress = Column(String)
    OperationDescription = Column(String)
    ServiceDescription = Column(String)
    Amount = Column(Float)
    Price = Column(Float)
    OverAllPrice = Column(Float)
    Discount = Column(Float)

DbEngine = create_engine('sqlite:///PetrolDb.db')

Base.metadata.create_all(DbEngine)
