#!/usr/bin/env python
# encoding: utf-8
'''
@author: xuqiang
@license: (C) Copyright 2013-2022.
@contact: xq-310@163.com
@software: wallet
@file: login.py.py
@time: 2019/7/20 下午1:22
@desc:
'''

from flask import render_template, request, url_for, flash, redirect,Blueprint
from flask_login import login_user,login_required,logout_user
from app.model.user import User,query_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired


bp_login = Blueprint('bp_login', __name__)

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')

@bp_login.route('/')
@bp_login.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        print(username)
        user = query_user(username)
        if user is not None and request.form['password']==user['password']:
            curr_user = User()
            curr_user.id = username

            login_user(curr_user, remember=True)

            next = request.args.get('next')
            #return redirect(next or url_for('bp_views.index'))
            #return redirect(url_for('bp_eth.eth'))
            return render_template('index.html')

        flash('wrong username or password !!!')
    #return render_template('login.html')
    return render_template('index.html')


@bp_login.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login.html'))