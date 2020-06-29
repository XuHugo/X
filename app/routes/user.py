#!/usr/bin/env python
# encoding: utf-8
'''
@author: xuqiang
@license: (C) Copyright 2013-2022.
@contact: xq-310@163.com
@software: f8s
@file: user.py
@time: 2020/5/2 上午9:38
@desc:
'''
from flask import render_template,Blueprint,request
from db.eth_db import EthDb
from rpc.eth_rpc_client import EthRpcClient
from common.tools import format_value

bp_user = Blueprint('bp_user', __name__)


@bp_user.route('/user',methods=['POST'])
def user():
    data={"result":"false"}
    print(request.get_json())
    address = request.get_json()["address"].lower()
    db=EthDb()
    r = db.check_address_exist(address)
    try:
        if r:
            balance = r.get("balance")
            nonce = r.get("nonce")
            print("user already exist!",nonce, balance)

        else:
            print("user new !")
            rpc = EthRpcClient()
            nonce = rpc.getTransactionCount(address)
            balance = rpc.getBalance(address)
            amount = format_value(balance, 10.0 ** 18)
            balance = hex(balance)
            ret = db.insert_address_new(address, address,  int(nonce), amount, balance)
            db.commit()
    except Exception as e:
        print(e)
        return data


    data = {
        "result": "OK",
        "nonce": nonce,
        "balance": balance
    }

    return data