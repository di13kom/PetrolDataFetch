#!/usr/bin/python3

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, func, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Petrol_Transactions(Base):
    __tablename__ = 'Petrol_Transactions'
    id = Column(Integer, primary_key=True)
    Transaction_Id = Column(String(length=100), unique=True,
                            index=True, nullable=False)  # MsSql lenght is required
    CardNum = Column(Integer)
    Date = Column(DateTime(timezone=True))
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

    def __eq__(self, other):
        return self.Transaction_Id == other.Transaction_Id

    def __cmp__(self, other):
        return self.Transaction_Id == other.Transaction_Id

    def UpdateByValue(self, other):
        self.CardNum = other.CardNum
        self.Date = other.Date
        self.ServiceDescription = other.ServiceDescription
        self.ServicePointAddress = other.ServicePointAddress
        self.ServicePointDescription = other.ServicePointDescription
        self.CardHolder = other.CardHolder
        self.OperationDescription = other.OperationDescription
        self.Amount = other.Amount
        self.Price = other.Price
        self.OverAllPrice = other.OverAllPrice
        self.Discount = other.Discount


DbEngine = create_engine('sqlite:///PetrolDb.db')

Base.metadata.create_all(DbEngine)
