#!/usr/bin/python
# -*- encoding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model.BaseModel import BaseModel

from config import Config


class Db(object):

    def __init__(self):
        connect_args = {'check_same_thread': False}
        self.engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=False, connect_args=connect_args)
        DB_Session = sessionmaker(bind=self.engine)
        self.session = DB_Session()

    def init_db(self):
        BaseModel.metadata.create_all(self.engine)

    def drop_db(self):
        BaseModel.metadata.drop_all(self.engine)
