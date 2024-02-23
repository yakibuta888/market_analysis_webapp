# coding: utf-8
from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, Date
from sqlalchemy import text

from archive.infrastructure.database.database import Base
import datetime


# Table情報
class Data(Base):
    # TableNameの設定
    __tablename__ = 'data'
    # Column情報を設定する
    id = Column(Integer, primary_key=True, autoincrement=True)
    month = Column(String, unique=False)
    open = Column(Float, unique=False)
    high = Column(Float, unique=False)
    low = Column(Float, unique=False)
    last = Column(Float, unique=False)
    change = Column(Float, unique=False)
    settle = Column(Float, unique=False)
    est_volume = Column(Integer, unique=False)
    prior_day_OI = Column(Integer, unique=False)
    timestamp = Column(DateTime, default=datetime.datetime.now())
    type = Column(String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'data',
        'polymorphic_on': type
    }

    def __init__(self, month=None, open=None, high=None, low=None, last=None,
                 change=None, settle=None, est_volume=None, prior_day_OI=None,
                 timestamp=None):
        self.month = month
        self.open = open
        self.high = high
        self.low = low
        self.last = last
        self.change = change
        self.settle = settle
        self.est_volume = est_volume
        self.prior_day_OI = prior_day_OI
        self.timestamp = timestamp


class CrudeOilData(Data):
    __tablename__ = 'crude_oil'
    id = Column(Integer, primary_key=True, autoincrement=True)
    __mapper_args__ = {
        'polymorphic_identity': 'crude_oil',
        'inherit_condition': text('id == Data.id')
    }
    __table_args__ = {

    }


class Gold(Data):
    __tablename__ = 'gold'
    id = Column(Integer, primary_key=True, autoincrement=True)
    __mapper_args__ = {
        'polymorphic_identity': 'gold',
        'inherit_condition': text('id == Data.id')
    }
    __table_args__ = {

    }
