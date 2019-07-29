#!/usr/bin/env python
# encoding: utf-8
'''
@author: xuqiang
@license: (C) Copyright 2013-2022.
@contact: xq-310@163.com
@software: wallet
@file: models.py.py
@time: 2019/7/14 下午9:05
@desc:
'''

from flask_login import UserMixin

users = [
    {'id':'Tom','username':'Tom','password':'666666'},
    {'id':'Michael','username':'Michael','password':'666666'}
]

class User(UserMixin):
    def __init__(self):
        self.id=None
        self.username=None
        self.task_count=None
        self.sample_count=None

    def todict(self):
        return self.__dict__

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return self.id
    pass


def query_user(user_id):
    for user in users:
        if user_id == user['id']:
            return user