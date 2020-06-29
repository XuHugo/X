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
import re
from web3 import Web3,HTTPProvider
from web3.auto import w3
from common.tools import *
from common.config import *
import pysnooper
from decimal import Decimal, ROUND_DOWN

BLOCK_INFO=["number","hash","parentHash","sha3Uncles","logsBloom","transactionsRoot","stateRoot","receiptsRoot","miner",
       "difficulty","totalDifficulty","extraData","size","gasLimit","gasUsed","timestamp","uncles","nonce","mixHash","transactions"]
TX_RECRIPT=["blockHash","blockNumber","contractAddress","cumulativeGasUsed","from","gasUsed","logs","logsBloom","status","to",
            "transactionHash","transactionIndex"]
_GET_BALANCE = "0x70a08231000000000000000000000000"
_DECIMALS = "0x313ce567"
_NAME = "0x06fdde03"
_SYMBOL = "0x95d89b41"

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

    def sendRawTansaction(self, rawtx):
        try:
            txhash = self.ethClient.eth.sendRawTransaction(rawtx).hex()
            return txhash
        except Exception as e:
            logger.info(e)
            return False

    def getTokenBalance(self, contract, address):
        try:
            contract =  self.ethClient.toChecksumAddress(contract)
            balance = int(self.call({"to": contract, "data": _GET_BALANCE + address[2:]}).hex(), 16)
            token_decimals = int(self.call({'to': contract, 'data': _DECIMALS}).hex(),16)
            balance = format_value(balance, 10 ** token_decimals)
            return {"balance":balance, "token_decimals":token_decimals}
        except Exception as e:
            logger.info(e)
            return False

    def getTokenInfo(self, contract):
        try:
            contract_addr = self.ethClient.toChecksumAddress(contract)
            token_name = self.call({'to':contract_addr, 'data':_NAME})
            token_name = re.sub(b'\x00'.decode(), "", token_name.decode()).strip()

            token_symbol = self.call({'to': contract_addr, 'data': _SYMBOL})
            token_symbol = re.sub(b'\x00'.decode(), "", token_symbol.decode()).strip()

            token_decimals = self.call({'to':contract_addr, 'data':_DECIMALS})
            token_decimals = int(token_decimals.hex(),16)

            return {"name":token_name,"symbol":token_symbol, "decimals":token_decimals}
        except Exception  as e:
            return False



if  __name__=="__main__":
    w =  EthRpcClient()
    #a = w.getBlockHashByNumber(7870697)
    #b = w.getBlockNumber
    #c = w.getTansactionsByBlockNumber(7870697)
    #d = w.getBlockInfosByBlockNumber(7870697)
    #e = w.getTransactionReceipt("0xdbb409993be4890212c8caf6a13936f8819e5989c4d37a1096974627e90d6352")
    #print(e)
    #e = w.getTransaction("0xdbb409993be4890212c8caf6a13936f8819e5989c4d37a1096974627e90d6352")
    #print(e)
    addr="0x2683b857043c011c5ee9610f878a191a3b76461e"
    #e=w.getTransactionCount(addr)
    #e=w.getBalance(addr)
    #print ("@",a,type(a))
    #print("@", b,type(b))
    # print("@", e)
    # print("@", e["logs"])
    # print("@", len(e["logs"]))
    # print("@", e["logs"][0]["data"])
    # print("@", int(e["logs"][0]["data"],16))
    # print("@", e["logs"][0]["topics"][0].hex())
    # print("@", e["logs"][0]["topics"][1].hex())
    # print("@", e["logs"][0]["topics"][1].hex()[26:])
    # print("@", e["logs"][0]["topics"][2].hex())
    # print(type(e["logs"]))

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
    # rawtx="0xf86c088504a817c800825208949ca53a80ebd1d28b78f43a50e74e527284196af5880de0b6b3a76400008029a02d956dc9ca7fe5198017bee45b0e4be7f7324f71273022dc1b6042968ef906f7a05487404bb90ebea17778a094df03a31e5b68d82cc545a025b8b570deae5a18f3"
    # th = w.sendRawTansaction(rawtx)
    # print(th,type(th))
    t=b"\xdb\xb4\t\x99;\xe4\x89\x02\x12\xc8\xca\xf6\xa196\xf8\x81\x9eY\x89\xc4\xd3z\x10\x96\x97F'\xe9\rcR"

    print(t.hex())
    a= "0x04a817c800"
    b=int(a,16)
    print(b,type(b))

    #account = w.ethClient.toChecksumAddress(account)
    _GET_BALANCE = "0x70a08231000000000000000000000000"
    contract_addr="0x33C33815A9dca51232578b30e7e0D222b57ea3cA".lower()

    #v = w.getTokenBalance(contract_addr,addr)
    print(contract_addr)
    v =w.getTokenInfo(contract_addr)
    print(v,type(v))
    print(v["name"], type(v["name"]))
    pass


