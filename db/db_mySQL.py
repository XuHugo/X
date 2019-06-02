#!/usr/bin/env python
# encoding: utf-8
'''
@author: xuqiang
@license: (C) Copyright 2013-2022.
@contact: xq-310@163.com
@software: wallet
@file: db_mySQL.py
@time: 2019/6/1 上午9:41
@desc:
'''

import pymysql
from DBUtils.PooledDB import PooledDB
from pymysql.cursors import DictCursor
from common.decorators import *
from common.config import *

@singleton
class MySQLDB(object):
    def __init__(self, coin_type=None):
        self.coin_type = coin_type
        self._conn = self.__getConn(coin_type)
        self._cursor = self._conn.cursor()

    @staticmethod
    def __getConn(coin_type=None):
        __pool = PooledDB(creator=pymysql, mincached=1, maxcached=20,
                          host=mysql_config[coin_type]['host'], port=mysql_config[coin_type]['port'],
                          user=mysql_config[coin_type]['user'], passwd=mysql_config[coin_type]['password'],
                          db=mysql_config[coin_type]['db'], use_unicode=mysql_config[coin_type]['unicode'], charset=mysql_config[coin_type]['charset'],
                          cursorclass=DictCursor, setsession=['SET AUTOCOMMIT = 0'])

        return __pool.connection()

    @property
    def cursor(self):
        return self._cursor

    @property
    def conn(self):
        return self._conn

    def get_conn(self):
        self._conn = self.__getConn(self.coin_type)
        return self._conn

    def get_cursor(self):
        self._cursor = self._conn.cursor()
        return self._cursor

if  __name__=="__main__":
    db = MySQLDB('eth')
    sql = "select * from address where addr = %s limit 1"
    addr = "0x27a439f14334421783a793fd58f03373dd9f962b"
    db.cursor.execute(sql,addr)
    ret = db.cursor.fetchone()
    if ret:
        print(ret)
    pass


