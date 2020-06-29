#!/usr/bin/env python
# encoding: utf-8
'''
@author: xuqiang
@license: (C) Copyright 2013-2022.
@contact: xq-310@163.com
@software: wallet
@file: __init__.py.py
@time: 2019/7/14 下午6:21
@desc:
'''

from flask import Flask
from flask_login import LoginManager
from app.routes.login import  bp_login
from app.routes.views import  bp_views
from app.routes.eth import  bp_eth
from app.routes.user import  bp_user
from app.routes.token import  bp_token

app = Flask(__name__)
app.config.from_object('config')

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Access denied.'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    from app.model.user import User
    user = User()
    return user.get_id()

app.register_blueprint(bp_login)
app.register_blueprint(bp_views)
app.register_blueprint(bp_eth)
app.register_blueprint(bp_user)
app.register_blueprint(bp_token)
from app.routes import views
