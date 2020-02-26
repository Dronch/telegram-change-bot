# -*- coding: utf-8 -*-
from sqlalchemy import Column, MetaData, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, String, DateTime, Float, Date
)

import datetime as dt


meta = MetaData()


class Model(declarative_base(metadata=meta)):
    """Base model"""
    __abstract__ = True
    id = Column(Integer, primary_key=True)


class Cache(Model):
    """Cache model"""
    __tablename__ = 'Cache'
    created_at = Column(DateTime, default=dt.datetime.utcnow)
    key = Column(String(16))
    exchange_rates = relationship('ExchangeRateModel')


class ExchangeRateModel(Model):
    """Exchange rate model"""
    __tablename__ = 'ExchangeRate'
    from_currency = Column(String(3))
    to_currency = Column(String(3))
    rate = Column(Float)
    source = Column(String(32))
    date = Column(Date)
    cache_id = Column(Integer, ForeignKey('Cache.id'))
