# -*- coding=utf8 -*-

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
            return -1

    def getBlockHashByNumber(self, number):
        try:
            blockhash = self.ethClient.eth.getBlock(number)
            return blockhash
        except Exception as e:
            logger.info(e)
            return -1

    def getTansactionByBlockNumber(self, number):
        try:
            block = self.ethClient.eth.getBlock(number,full_transactions=True)
            return block
        except Exception as e:
            logger.info(e)
            return -1


if  __name__=="__main__":
    w3 = Web3(HTTPProvider(Node_1))
    bh = w3.eth.getBlock(1234)
    he = w3.eth.blockNumber
    print("hello:")
    print ("@",bh)
    print("@", he,type(he))
    pass


