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
from flask import render_template,Blueprint,request
from rpc.eth_rpc_client import EthRpcClient
from db.eth_db import EthDb
from decimal import Decimal, ROUND_DOWN

bp_eth = Blueprint('bp_eth', __name__)


@bp_eth.route('/eth/tx',methods=['GET','POST'])
def sendtx():
    rpc = EthRpcClient()
    db =  EthDb()
    print(request.get_json())
    transaction= request.get_json()
    try:
        txhash = rpc.sendRawTansaction(transaction["rawtx"])
    except Exception as e:
        raise e
    if transaction["token"]:
        #to do
        print("process token!")
        pass
    else:
        print("process tx!")
        params = dict()
        params["is_token"] = 0
        params["nonce"] = transaction["nonce"]
        params["value"] = int(transaction['value']["_hex"],16)
        params["from"] = transaction['from'].lower()
        params["to"] = transaction['to'].lower()
        params["hash"] = txhash
        params["gasPrice"] = int(transaction["gasPrice"]["_hex"],16)
        params["mark_state"] = 1  # 第一次插入的的=1

        ret = db.insert_tx_record_first(params)
        db.commit()

    return {"th":"0x"+txhash}

@bp_eth.route('/eth/txlist',methods=['POST'])
def gettxlist():
    address = request.get_json()["address"]
    db = EthDb()
    items = db.get_tx_address(address)
    infos = []
    for item in items:
        tx={}
        tx["from"] = item["from"]
        tx["to"]=item["to"]
        tx["hash"]=item["hash"]
        tx["nonce"]=item["nonce"]
        tx["value"]=str((item["value"] / Decimal(10.0 ** 18)).quantize(Decimal('.00000001'), ROUND_DOWN))
        tx["time"]=item["time"]
        tx["state"]=item["mark_state"]
        infos.append(tx)
    print('ssss:',len(infos))
    result={"result":infos}

    return result

