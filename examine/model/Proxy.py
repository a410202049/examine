#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from sqlalchemy import Column, Integer, DateTime, Numeric, VARCHAR
from config import Config
from model.BaseModel import BaseModel


class Proxy(BaseModel):
    __tablename__ = 'proxys'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(VARCHAR(16), nullable=False)
    port = Column(VARCHAR, nullable=False, doc="端口号")
    type = Column(VARCHAR, nullable=False, doc="0高匿名，1透明")
    protocol = Column(Integer, nullable=False, default=0, doc='0 http,1 https')
    country = Column(VARCHAR(100), nullable=False, doc="国家")
    area = Column(VARCHAR(100), nullable=False, doc="地区 省市")
    speed = Column(VARCHAR, nullable=False, doc="连接速度")
    score = Column(Integer, nullable=False, default=Config.DEFAULT_SCORE, doc="分数")
    expire_time = Column(DateTime())
    update_time = Column(DateTime(), default=datetime.datetime.utcnow)
    create_time = Column(DateTime(), default=datetime.datetime.utcnow)


class SubmitCount(BaseModel):
    __tablename__ = 'submit_count'
    id = Column(Integer, primary_key=True, autoincrement=True)
    count = Column(Integer, nullable=False, default=Config.DEFAULT_SCORE, doc="提交次数")
    update_time = Column(DateTime(), default=datetime.datetime.utcnow)
    create_time = Column(DateTime(), default=datetime.datetime.utcnow)