#!/usr/bin/env python
# encoding: utf-8
'''
@author: xuqiang
@license: (C) Copyright 2013-2022.
@contact: xq-310@163.com
@software: f8s
@file: component.py
@time: 2020/5/17 下午4:47
@desc:
'''

from db.eth_db  import EthDb
from rpc.eth_rpc_client  import EthRpcClient
import re
from common.tools import format_value

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

def update_contract_addr(contract_addr):
    if contract_addr:
        # 先从数据库里判断
        db = EthDb()
        ret = db.is_contract_address(contract_addr.lower())
        if not ret:
            # 如果数据库里没有，则添加到数据库里
            rpc = EthRpcClient()
            infos = rpc.getTokenInfo(contract_addr)
            token_name = infos["name"]
            token_symbol = infos["symbol"]
            token_decimals = infos["decimals"]
            # 异常处理
            token_name = _DEFAULT_NAME if token_name in _WEIRD_NAME else token_name
            token_symbol = _DEFAULT_SYMBOL if token_symbol in _WEIRD_SYMBOL else token_symbol

            print("name:%s | %s", token_name, token_symbol)
            print("contract:%s | %s", contract_addr, token_decimals)
            db.insert_token(contract_addr.lower(), _DEFAULT_TYPE, token_name[:66], token_symbol[:32],
                                 token_decimals,
                                 10 ** token_decimals, _DEFAULT_ICON, _DEFAULT_DADDY)
            db.commit()
            ret = True
    else:
        ret = False
    return ret

def token_balance_updata(contract_addr, addr):
    # 通过合约的方法获取账户余额
    rpc = EthRpcClient()
    db = EthDb()
    # __token_call = rpc.call
    # balance = __token_call({"to":contract_addr,"data":_GET_BALANCE + addr[2:]})
    # balance = int(balance.hex(),16)
    # balance = format_value(balance, 10 ** token_decimals)
    infos = rpc.getTokenBalance(contract_addr, addr)
    token_balance_params = dict(
        addr=addr,
        balance=infos["balance"],
        contract_addr=contract_addr.lower(),
        unconfirm_amount=0,
        decimals=infos["token_decimals"],
        added="1",
    )
    # 更新数据库余额
    db.insert_token_balance_tx_record(token_balance_params)
    db.commit()
    return infos["balance"],infos["token_decimals"]