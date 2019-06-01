#!/usr/bin/env python
# encoding: utf-8
'''
@author: xuqiang
@license: (C) Copyright 2013-2022.
@contact: xq-310@163.com
@software: wallet
@file: eth_rpc_client.py.py
@time: 2019/6/1 上午9:41
@desc:
'''

from web3 import Web3,HTTPProvider
from web3.auto import w3
from common.tools import *
from config import *

class EthRpcClient(object):

    def __init__(self, Node_Addr=""):
        if Node_Addr == "":
            self.ethClient = w3
        else:
            self.ethClient =Web3(HTTPProvider(Node_Addr))

    @property
    def getBlockNumber(self):
        try:
            blocknumber = self.ethClient.eth.blockNumber
            return blocknumber
        except Exception as e:
            logger.info(e)
            return False

    def getBlockHashByNumber(self, number):
        try:
            blockhash = self.ethClient.eth.getBlock(number)
            return blockhash["hash"].hex()
        except Exception as e:
            logger.info(e)
            return False

    def getTansactionByBlockNumber(self, number):
        try:
            block = self.ethClient.eth.getBlock(number,full_transactions=True)
            return block
        except Exception as e:
            logger.info(e)
            return False


if  __name__=="__main__":
    w =  EthRpcClient(Node_1)
    a = w.getBlockHashByNumber(7870697)
    b = w.getBlockNumber
    c = w.getTansactionByBlockNumber(7870697)
    print("hello:")
    print ("@",a)
    print("@", type(a))
    print("@", b,type(b))
    print("@", c, type(c))
    pass


