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
from flask import render_template,Blueprint,redirect,request,url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired


bp_views = Blueprint('bp_views', __name__)

@bp_views.route('/index',methods=['GET','POST'])
def index():
    user = {'nickname':'xq'}
    if request.method == 'POST':
        print(request.form.to_dict())
        coin = request.form.to_dict()
        print(request.json)
        if coin["COINTYPE"] == "eth":
            return redirect(url_for('bp_eth.eth'))
    return render_template("index.html",
                           title = "Home",
                           user = user)

