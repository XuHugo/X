# -*- coding:utf-8 -*-

import MySQLdb
from DBUtils.PooledDB import PooledDB
from MySQLdb.cursors import DictCursor

from common.decorators import *


@singleton
class MySQLDB(object):
    def __init__(self):
        self._conn = self.__getConn()
        self._cursor = self._conn.cursor()

    @staticmethod
    def __getConn():
        __pool = PooledDB(creator=MySQLdb, mincached=1, maxcached=20,
                          host="127.0.0.1", port=3306,
                          user="root", passwd="",
                          db="eth_address", use_unicode=False, charset="ascii",
                          cursorclass=DictCursor, setsession=['SET AUTOCOMMIT = 0'])

        return __pool.connection()

    @property
    def cursor(self):
        return self._cursor

    @property
    def conn(self):
        return self._conn

    def get_conn(self):
        self._conn = self.__getConn()
        return self._conn

    def get_cursor(self):
        self._cursor = self._conn.cursor()
        return self._cursor


