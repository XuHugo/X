# -*- coding:utf-8 -*-
from  db.db import Db

class EthDb(Db):

    def __init__(self):
        super(EthDb, self).__init__()

    def getBlockHashByNumber(self, number):
        try:
            self.execute("select hash from block where height = %s and state =1", number)
            ret = self.fetchone()
            if ret:
                return ret.get("hash").decode()
        except Exception as e:
            print(e)

    def getBlockNumber(self):
        try:
            self.execute("select max(height) as h from block where state=1")
            ret = self.fetchone()
            ret = ret['h']
            return ret if ret != None else -1
        except:
            return -1

    def markUnclelock(self, block_hash):
        sql = ("update block left join tx on block.hash = tx.block_hash set block.state = 0, tx.block_state = 0 "
               "where block.hash = %s")
        self.execute(sql, block_hash)

    def insertBlockRecord(self, height, size, timestamp, hash, previous, state):
        sql = "insert into block(height, `size`, `timestamp`, hash, previous, state) values(%s) " \
              "on DUPLICATE KEY UPDATE timestamp=values(timestamp) ,state=values(state)"
        sql = sql % ",".join(["%s"] * 6)
        self.execute(sql, height, size, timestamp, hash, previous, state)
        pass