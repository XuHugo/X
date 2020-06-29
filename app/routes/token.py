#!/usr/bin/env python
# encoding: utf-8
'''
@author: xuqiang
@license: (C) Copyright 2013-2022.
@contact: xq-310@163.com
@software: wallet
@file: views.py.py
@time: 2019/7/14 下午6:23
@desc:
'''
from flask import Blueprint,request
from rpc.eth_rpc_client import EthRpcClient
from db.eth_db import EthDb
from decimal import Decimal, ROUND_DOWN
from common import  component

bp_token = Blueprint('bp_token', __name__)


@bp_token.route('/token/tx',methods=['GET','POST'])
def sendtoken():
    rpc = EthRpcClient()
    db =  EthDb()
    print(request.get_json())
    transaction= request.get_json()
    try:
        txhash = rpc.sendRawTansaction(transaction["rawtx"])
        print("transaction txhash:", txhash)
    except Exception as e:
        print("transaction error:",e)
        raise e

    print("process token!")
    params = dict()

    params["token_addr_from"] = transaction['from'].lower()
    params["token_addr_to"] = transaction['to'].lower()
    params["token_amount"] = transaction["value"]
    params["tx_hash"] = txhash
    params["contract_addr"] = transaction["contract"].lower()
    params["token_decimals"] = transaction["decimals"]
    params["nonce"] = transaction["nonce"]

    ret = db.insert_tokentx_first(params)
    db.commit()

    return {"th":"0x"+txhash}

@bp_token.route('/token/txlist',methods=['POST'])
def gettokenlist():
    address = request.get_json()["address"]
    contract = request.get_json()["contract"]
    db = EthDb()
    items = db.get_token_address(address, contract)
    infos = []
    for item in items:
        tx={}
        tx["from"] = item["from_addr"]
        tx["to"]=item["to_addr"]
        tx["contract"] = item["contract_addr"]
        tx["hash"]=item["tx_hash"]
        tx["nonce"]=item["nonce"]
        tx["value"]=str(item["amount"])
        tx["time"]=item["update_time"]
        tx["state"]=item["status"]
        infos.append(tx)
    print('#######Token List::',len(infos))
    result={"result":infos}

    return result

@bp_token.route('/token/token',methods=['POST'])
def gettoken():
    print("gettoken~~:",request.get_json())
    address = request.get_json()["address"]
    token = request.get_json()["token"]
    result={}
    try:
        db = EthDb()
        infos = db.get_token_balance(token, address)

        #如果不存在，则添加
        if infos:
            result["balance"]= str(infos["balance"])
            result["decimals"] = infos["decimals"]
        else:
            component.update_contract_addr(token)
            balance,decimals = component.token_balance_updata(token, address)
            result["balance"] = str(balance)
            result["decimals"] = decimals

        return result
    except Exception as e:
        return False

