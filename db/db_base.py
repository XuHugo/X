#!/usr/bin/env python
# encoding: utf-8
'''
@author: xuqiang
@license: (C) Copyright 2013-2022.
@contact: xq-310@163.com
@software: wallet
@file: db.py
@time: 2019/6/1 上午9:41
@desc:
'''

from db.db_mySQL import MySQLDB
from common.decorators import *
from common.tools import logger
import binascii
import pymysql

class Db(object):

    def __init__(self, coin_type=None):
        self.coin_type = coin_type
        self.db = MySQLDB(coin_type).conn
        self.cursor = self.db.cursor()

    def execute(self, sql, *args):
        return self.cursor.execute(sql, args)

    def executemany(self, sql, args):
        return self.cursor.executemany(sql, args)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def commit(self):
        try:
            self.db.commit()
            return True
        except Exception as e:
            logger.error("commit faild: " + str(e))
            self.db.rollback()
            return False

    def rollback(self):
        self.db.rollback()

    def reset_connection(self):
        self.cursor.close()
        self.db.close()
        self.db = MySQLDB(self.coin_type).get_conn()
        self.cursor = self.db.cursor()


if __name__ == '__main__':

    db = Db('eth')
    sql="select amount from address;"
    db.execute(sql)
    ret = db.fetchone()
    if ret:
        print(ret)
    db.cursor.close()
    db.db.close()

"""
    address="0x27a439f14334421783a793fd58f03373dd9f962b"
    private="974fcab269e5b6f6dcf7f0a1426f0339de029d02871447278573136ff28f25b1"
    #a = [address, binascii.b2a_hex(private), 0,0]
    a = [address, (private), 1, 99]
    sql = "insert into address(addr, wallet_id,platform,addr_type) values(%s,%s,%s,%s)"
    db.execute(sql, address, (private), 1, 99)
    db.commit()
"""


