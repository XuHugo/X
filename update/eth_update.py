#!/usr/bin/env python
# encoding: utf-8
'''
@author: xuqiang
@license: (C) Copyright 2013-2022.
@contact: xq-310@163.com
@software: wallet
@file: eth_update.py.py
@time: 2019/6/1 上午9:41
@desc:
'''

from db.eth_db  import EthDb
from rpc.eth_rpc_client  import EthRpcClient
from common.tools import *
from common.config import *
import time
import sys
from decimal import Decimal, ROUND_DOWN
import operator
import string
import binascii
import re
import pysnooper
from web3 import Web3,HTTPProvider

BLOCK_INFO=["number","hash","parentHash","sha3Uncles","logsBloom","transactionsRoot","stateRoot","receiptsRoot","miner",
       "difficulty","totalDifficulty","extraData","size","gasLimit","gasUsed","timestamp","uncles","nonce","mixHash","transactions"]
TX_RECRIPT=["blockHash","blockNumber","contractAddress","cumulativeGasUsed","from","gasUsed","logs","logsBloom","status","to",
            "transactionHash","transactionIndex"]
TX = ["blockHash","blockNumber","gas","from","gasUsed","hash","gasPrice","input","nonce","to","v","s","r"
            "value","transactionIndex"]

_NAME = "0x06fdde03"
_SYMBOL = "0x95d89b41"
_DECIMALS = "0x313ce567"
_DEFAULT_SYMBOL = "WonderCookies"
_DEFAULT_NAME = "MysteriousMan"
_DEFAULT_DECIMALS = 18
_WEIRD_DECIMALS = ["0x"]
_WEIRD_NAME = [""]
_WEIRD_SYMBOL = [""]
_DEFAULT_ICON = "icon_DEFAULT.png"
_DEFAULT_DADDY = "ETH"
_DEFAULT_TYPE = 60
_GET_BALANCE = "0x70a08231000000000000000000000000"
_TRANSACTION_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"

class EthBlockUpdater(object):

    def __init__(self, expect_number=0):
        self.coin_type = 'eth'
        self.rpc = EthRpcClient()
        self.db = EthDb()
        self.resis = None
        self.sleep_time = 0
        self.expect_number = expect_number
        self.precision = 10.0 ** 18

    def toChecksumAddress(self,addr):
        addr = Web3(HTTPProvider()).toChecksumAddress(addr)
        return addr

    def format_value(self, v, d):
        r = (Decimal(v) / Decimal(d)).quantize(Decimal('.00000001'), ROUND_DOWN)
        return r

    def update(self):

        number = max(self.expect_number, self.db.getBlockNumber())
        while True:
            print("number:",number)
            #处理分叉
            number = self.fork_handler(number)

            #处理新块
            ret = self.process_block(number)

            if ret:
                number += 1
            else:
                time.sleep(5)
                pass

    def fork_handler(self, number):
        print("fork_handler:", number)
        while number > self.expect_number:

            rpc_blockhash = self.rpc.getBlockHashByNumber(number-1)
            db_blockhash = self.db.getBlockHashByNumber(number-1)

            if rpc_blockhash == db_blockhash:
                return number
            else:
                logger.info("rollback block %s",number)
                self.db.delete_tx_record(db_blockhash)
                self.db.mod_block_state(db_blockhash)
                self.db.commit()
                number -= 1

            if number<self.expect_number:
                exit("stop rollback at blocknumber %d!!!" % number)
        return number

    def process_block(self, number):
        logger.info('processing block...')
        print("process_block:", number)

        block_info = self.rpc.getBlockInfoByNumber(number)
        self.store_block_data(block_info)

        self.process_transactions(block_info["transactions"])
        return True

    def store_block_data(self, block_data):
        height = block_data["number"]
        size = block_data["size"]
        timestamp = block_data["timestamp"]
        hash = block_data["hash"].hex()
        previous = block_data["parentHash"].hex()
        state = 1
        #print(height,size,timestamp,hash,previous,state)
        #print(timestamp,type(timestamp))
        self.db.insertBlockRecord(height, size, timestamp, hash, previous, state)
        self.db.commit()

    def process_transactions(self, txs_hash):
        for tx_hash in txs_hash:

            # 普通交易
            params, tx_receipt = self.process_eth_transaction(tx_hash.hex())
            # token交易
            self.process_token_transaction(params, tx_receipt)
            # 内部交易
            #self.process_internal_transaction(params, tx_receipt)
            # 合约交易
            #self.process_contract_transaction(params, tx_receipt)
            pass
        pass

    def process_eth_transaction(self, tx):
        try:
            transaction = self.rpc.getTransaction(tx)
            #print(transaction["from"].lower(),type(transaction["from"]))

            user_from = self.db.related_to_user(transaction["from"].lower())
            user_to = self.db.related_to_user(transaction["to"].lower())
            #print(transaction["from"].lower(),transaction["to"].lower())
            #print(user_from,user_to)
            tx_receipt = self.rpc.getTransactionReceipt(transaction["hash"])

            params = dict()
            fee = tx_receipt['gasUsed'] * transaction["gasPrice"]

            params["nonce"] = transaction["nonce"]
            params["raw"] = "raw"
            params["fee"] = fee
            params["value"] = transaction['value']
            params["gasUsed"] = tx_receipt['gasUsed']
            params["status"] = tx_receipt['status']
            params["from"] = tx_receipt['from'].lower()
            params["to"] = tx_receipt['to'].lower()
            params["blockHash"]=tx_receipt['blockHash'].hex()
            params["rsv"]=transaction['r'].hex()+"%"+transaction['s'].hex()+"%"+str(transaction['v'])
            params["gas"]=transaction["gas"]
            params["blockNumber"]=transaction["blockNumber"]
            params["hex_input"]=transaction["input"]
            params["publicKey"]="publicKey"
            params["transactionIndex"]=tx_receipt['transactionIndex']
            params["hash"]= transaction["hash"].hex()
            params["gasPrice"]=transaction["gasPrice"]
            params["block_timestamp"]=1
            #print(params)

            if any([user_from, user_to]):
                print('find relate user!!!')
                self.db.insert_tx_record(params)

                # todo  更新账户余额和nonce
                if any([user_from]) > 2:
                    user_nonce, user_amount = self.rpc.getTransactionCount(user_from), self.rpc.getBalance(user_from)
                    self.db.update_address_table(user_nonce, self.format_value(user_amount, self.precision), user_from)

                if any([user_to]) > 2:
                    user_nonce, user_amount = self.rpc.getTransactionCount(user_to), self.rpc.getBalance(user_to)
                    self.db.update_address_table(user_nonce, self.format_value(user_amount, self.precision), user_to)

                self.db.commit()
            return params, tx_receipt

        except Exception as e:
            logger.error("Error for process_eth_transaction,%s", e)
            return None,None
        pass

    #@pysnooper.snoop()
    def analysis_logs(self, content):
        """addr_from, addr_to, logindex, amount"""
        if len(content['topics']) < 3 or operator.eq(content['topics'][0], _TRANSACTION_TOPIC):
            return [False] * 4
        addr_from = "0x"+content['topics'][1].hex()[26:]
        addr_to = "0x"+content['topics'][2].hex()[26:]
        return addr_from, addr_to, content['logIndex'], int(content['data'],16)

    # 新增数据库里没有token类型
    def token_add(self, contract_addr):
        # 处理非入库的token
        __token_call = self.rpc.call
        token_name = __token_call({'to':contract_addr, 'data':_NAME})
        token_name = re.sub(b'\x00'.decode(), "", token_name.decode()).strip()

        token_symbol = __token_call({'to': contract_addr, 'data': _SYMBOL})
        token_symbol = re.sub(b'\x00'.decode(), "", token_symbol.decode()).strip()

        token_decimals = __token_call({'to':contract_addr, 'data':_DECIMALS})
        token_decimals = int(token_decimals.hex(),16)

        # 异常处理
        token_name = _DEFAULT_NAME if token_name in _WEIRD_NAME else token_name
        token_symbol = _DEFAULT_SYMBOL if token_symbol in _WEIRD_SYMBOL else token_symbol

        print("name:%s | %s", token_name, token_symbol)
        print("contract:%s | %s", contract_addr, token_decimals)
        self.db.insert_token(contract_addr.lower(), _DEFAULT_TYPE, token_name[:66], token_symbol[:32], token_decimals,
                             10 ** token_decimals, _DEFAULT_ICON, _DEFAULT_DADDY)
        self.db.commit()
        pass

    # 更新合约地址数据库
    def updata_contract_addr(self, contract_addr):
        if contract_addr:
            # 先从数据库里判断
            ret = self.db.is_contract_address(contract_addr.lower())
            if not ret:
                # 如果数据库里没有，则添加到数据库里
                self.token_add(contract_addr)
                ret = False
        else:
            ret = False
        return ret

    # 更新token交易
    def token_tx_insert(self, contract_addr, tx_receipt, params, param):
        # 插入交易信息
        try:
            param["token_amount"] = self.format_value(param["token_amount"], 10.0 ** param["token_decimals"])
        except Exception as ex:
            logger.error("format_value Error tx_hash = %s", params["hash"])

        print("token_amount=%s", param["token_amount"])
        print("token_decimals=%s", param["token_decimals"])

        token_params = dict(
            fee=params["fee"],
            token_decimals=param["token_decimals"],
            token_amount=param["token_amount"],
            contract_addr=contract_addr,
            token_addr_from=param["token_addr_from"],
            token_addr_to=param["token_addr_to"],
            logindex=param["logindex"],
            tx_hash=params["hash"],
            block_timestamp=params["block_timestamp"],
            blockNumber=params["blockNumber"],
            nonce=params["nonce"],
            gasPrice=params["gasPrice"],
            gas=params["gas"],
            gasUsed=tx_receipt['gasUsed'],
            status=tx_receipt['status']
        )

        self.db.insert_token_tx_tx_record(token_params)
        self.db.update_tx_record(token_params["tx_hash"])
        self.db.commit()

    # 更新token余额
    def token_balance_updata(self, contract_addr, token_addr_from, token_addr_to, token_decimals):
        # 通过合约的方法获取账户余额
        if not token_addr_from or not token_addr_to or len(token_addr_from) < 42 or len(token_addr_to) < 42:
            return
        __token_call = self.rpc.call
        from_balance = __token_call({"to":contract_addr,"data":_GET_BALANCE + token_addr_from[2:]})
        to_balance = __token_call({"to":contract_addr,"data":_GET_BALANCE + token_addr_from[2:]})

        from_balance = int(from_balance.hex(),16)
        to_balance = int(to_balance.hex(),16)

        from_balance = self.format_value(from_balance, 10 ** token_decimals)
        to_balance = self.format_value(to_balance, 10 ** token_decimals)

        from_token_balance_params = dict(
            addr=token_addr_from,
            balance=from_balance,
            contract_addr=contract_addr,
            unconfirm_amount=0,
            decimals=token_decimals,
            added="1",
        )

        to_token_balance_params = dict(
            addr=token_addr_to,
            balance=to_balance,
            contract_addr=contract_addr,
            unconfirm_amount=0,
            decimals=token_decimals,
            added="1",
        )
        # 更新数据库余额
        self.db.insert_token_balance_tx_record(from_token_balance_params)
        self.db.insert_token_balance_tx_record(to_token_balance_params)
        self.db.commit()

    #@pysnooper.snoop()
    def process_token_transaction(self, params, tx_receipt):

        if tx_receipt["logs"] is None:
            print("don't have logs!")
            return
        # 根据erc20标志，token交易都会出发transfer事件，
        for log in tx_receipt["logs"]:
            try:

                if log["topics"] and log["topics"][0].hex() == _TRANSACTION_TOPIC:
                    contract_addr = log["address"]

                    token_addr_from, token_addr_to, logindex, token_amount = self.analysis_logs(log)

                    # 判断是否是关联用户
                    account1, account2 = self.db.related_to_user(token_addr_from), \
                                         self.db.related_to_user(token_addr_to)

                    if any([account1, account2]):
                        # 更新合约和精度
                        print("token relate user!!",account1,account2)

                        self.updata_contract_addr(contract_addr)
                        token_decimals = self.db.get_token_decimals(contract_addr)

                        if not token_decimals:
                            __token_call = self.rpc.call
                            token_decimals = __token_call({'to': contract_addr, 'data': _DECIMALS})
                            token_decimals = int(token_decimals.hex(), 16)

                        param = dict(
                            token_decimals=token_decimals,
                            token_amount=token_amount,
                            token_addr_from=token_addr_from,
                            token_addr_to=token_addr_to,
                            logindex=logindex,
                        )

                        self.token_tx_insert(contract_addr, tx_receipt, params, param)
                        self.token_balance_updata(contract_addr, token_addr_from, token_addr_to, token_decimals)
                    else:
                        # 非关联用户
                        pass
                else:
                    pass
            except Exception as ex:
                logger.error("Error for process_token_transaction,%s", ex)
        pass

if  __name__=="__main__":
    p = EthBlockUpdater(7894473)
    p.update()
    pass