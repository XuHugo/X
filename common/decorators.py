#!/usr/bin/env python
# encoding: utf-8
'''
@author: xuqiang
@license: (C) Copyright 2013-2022.
@contact: xq-310@163.com
@software: wallet
@file: decorators.py.py
@time: 2019/6/1 上午9:41
@desc:
'''


def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        key = (cls, args)
        if key not in instances:
            instances[key] = cls(*args, **kwargs)
        return instances[key]
    return get_instance