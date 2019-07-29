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
from flask import render_template,Blueprint



bp_eth = Blueprint('bp_eth', __name__)


@bp_eth.route('/eth',methods=['GET','POST'])
def eth():
    user = {'nickname':'xq'}

    return render_template("eth.html",
                           title = "ETH",
                           user = user)

