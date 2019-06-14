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
from common.config import *
import pysnooper

BLOCK_INFO=["number","hash","parentHash","sha3Uncles","logsBloom","transactionsRoot","stateRoot","receiptsRoot","miner",
       "difficulty","totalDifficulty","extraData","size","gasLimit","gasUsed","timestamp","uncles","nonce","mixHash","transactions"]
TX_RECRIPT=["blockHash","blockNumber","contractAddress","cumulativeGasUsed","from","gasUsed","logs","logsBloom","status","to",
            "transactionHash","transactionIndex"]

class EthRpcClient(object):

    def __init__(self, host=None, port=None):
        self.host = host or rpc_config['eth']['host']
        self.port = port or rpc_config['eth']['port']
        self.way = rpc_config['eth']['way'].lower().strip()
        self.ethClient = self.__getclient(self.host, self.port, self.way)

    def __getclient(self, host, port, way):
        return{'geth':None,
        'parity':None,
        'infura':Web3(HTTPProvider(host))}.get(way,'error')

    @property
    def getBlockNumber(self):
        try:
            blocknumber = self.ethClient.eth.blockNumber
            return blocknumber
        except Exception as e:
            logger.info(e)
            return False

    def call(self,transaction):
        try:
            ret = self.ethClient.eth.call(transaction)
            return ret
        except Exception as e:
            logger.info(e)
            return False

    def getBlockInfoByNumber(self, number):
        try:
            block = self.ethClient.eth.getBlock(number)
            return block
        except Exception as e:
            logger.info(e)
            return False

    def getBlockInfosByNumber(self, number):
        try:
            block = self.ethClient.eth.getBlock(number,full_transactions=True)
            return block
        except Exception as e:
            logger.info(e)
            return False

    def getTransaction(self, txhash):
        try:
            tx = self.ethClient.eth.getTransaction(txhash)
            return tx
        except Exception as e:
            logger.info(e)
            return False

    def getTransactionCount(self, account):
        try:
            account = self.ethClient.toChecksumAddress(account)
            num = self.ethClient.eth.getTransactionCount(account)
            return num
        except Exception as e:
            logger.info(e)
            return False

    def getBalance(self, account):
        try:
            account = self.ethClient.toChecksumAddress(account)
            num = self.ethClient.eth.getBalance(account)
            return num
        except Exception as e:
            logger.info(e)
            return False

    def getTransactionReceipt(self, txhash):
        try:
            txreceipt = self.ethClient.eth.getTransactionReceipt(txhash)
            return txreceipt
        except Exception as e:
            logger.info(e)
            return False

    def getBlockHashByNumber(self, number):
        try:
            blockhash = self.getBlockInfoByNumber(number)
            return blockhash["hash"].hex()
        except Exception as e:
            logger.info(e)
            return False

    def getParentHashByNumber(self, number):
        try:
            blockhash = self.getBlockInfoByNumber(number)
            return blockhash["parentHash"].hex()
        except Exception as e:
            logger.info(e)
            return False

    def getTansactionsInfoByBlockNumber(self, number):
        try:
            block = self.getBlockInfosByBlockNumber(number)
            return block["transactions"]
        except Exception as e:
            logger.info(e)
            return False

    def getTansactionsIdByBlockNumber(self, number):
        try:
            block = self.getBlockInfoByNumber(number)
            return block["transactions"]
        except Exception as e:
            logger.info(e)
            return False


if  __name__=="__main__":
    w =  EthRpcClient()
    #a = w.getBlockHashByNumber(7870697)
    #b = w.getBlockNumber
    #c = w.getTansactionsByBlockNumber(7870697)
    #d = w.getBlockInfosByBlockNumber(7870697)
    e = w.getTransactionReceipt("0x0825579f4141bdda785e8e197054a7acf291c67dfd4fdd85b13dbb1d133b9d02")
    #e = w.getTransaction("0x09e306e3afc429bcf0e7c30561d48ede8d32d325899dfdcb87f122b14844b9da")
    addr="0x2683b857043c011c5ee9610f878a191a3b76461e"
    #e=w.getTransactionCount(addr)
    #e=w.getBalance(addr)
    print("hello:")
    #print ("@",a,type(a))
    #print("@", b,type(b))
    print("@", e)
    print("@", e["logs"])
    print("@", len(e["logs"]))
    print("@", e["logs"][0]["data"])
    print("@", int(e["logs"][0]["data"],16))
    print("@", e["logs"][0]["topics"][0].hex())
    print("@", e["logs"][0]["topics"][1].hex())
    print("@", e["logs"][0]["topics"][1].hex()[26:])
    print("@", e["logs"][0]["topics"][2].hex())
    print(type(e["logs"]))

    """
    print(d["number"])
    print(d["hash"].hex())
    print(d["parentHash"].hex())
    print(d["sha3Uncles"].hex())
    print(d["logsBloom"].hex())
    print(d["transactionsRoot"].hex())
    print(d["stateRoot"].hex())
    print(d["receiptsRoot"].hex())
    print(d["miner"])
    print(d["difficulty"])
    print(d["totalDifficulty"])
    print(d["extraData"].hex())
    print(d["size"])
    print(d["gasLimit"])
    print(d["gasUsed"])
    print(d["timestamp"])
    print(d["uncles"])
    print(d["nonce"].hex())
    print(d["mixHash"].hex())
    """

    pass


