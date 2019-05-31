# -*- coding:utf-8 -*-

from db.dbMySQL import MySQLDB
from common.decorators import *
from common.tools import logger
import binascii


class Db(object):

    def __init__(self):
        self.db = MySQLDB().conn
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
        self.db = MySQLDB().get_conn()
        self.cursor = self.db.cursor()


if __name__ == '__main__':
    db = MySQLDB('eth')
    db.execute("select * from address")
    ret = db.fetchone()
    if ret:
        print(ret)

    address="0x27a439f14334421783a793fd58f03373dd9f962b"
    private="974fcab269e5b6f6dcf7f0a1426f0339de029d02871447278573136ff28f25b1"
    a = [address, binascii.b2a_hex(private), 0,0]
    sql = "insert into address(addr, `addr_p`,balance, `echo`) values(%s,%s,%s,%s)"
    db.execute(sql, address, binascii.b2a_hex(private), 0,0)