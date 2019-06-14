#!/usr/bin/env python
# encoding: utf-8
'''
@author: xuqiang
@license: (C) Copyright 2013-2022.
@contact: xq-310@163.com
@software: wallet
@file: config.py
@time: 2019/6/1 上午9:41
@desc:
'''
from common.decorators  import *
import yaml
import os

# CONFIG_FILE = r"C:\Users\yhz\Desktop\work\gembackend\common\config.yml"#"common/config.yml"
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.yaml")  # "common/config.yml"

config = yaml.load(open(CONFIG_FILE, 'r'), Loader=yaml.FullLoader)

@singleton
class MysqlConfig(object):
    def __init__(self):
        self.config = config
        self.cfg = {}
        for coin_type in config['coin']:
            section = 'mysql-' + coin_type
            self.cfg[coin_type] = self.config[section]

    def set_coin_type(self, coin_type='eth'):
        section = 'mysql-' + coin_type
        self.coin_type = coin_type
        self.__dict__.update(config[section])

    def __getitem__(self, key):
        return self.cfg[key]

@singleton
class RpcConfig(object):
    def __init__(self):
        self.config = config
        self.cfg = {}
        for coin_type in config['coin']:
            section = coin_type + '-rpc'
            self.cfg[coin_type] = self.config[section]

    def set_coin_type(self, coin_type='eth'):
        section = coin_type + '-rpc'
        self.coin_type = coin_type
        self.__dict__.update(config[section])

    def __getitem__(self, key):
        return self.cfg[key]

class CoinConfig(object):
    def __init__(self):
        self.coin_types = config['coin']
        self.coin_types_dict = {coin_type: True for coin_type in self.coin_types}

    def is_supported(self, coin_type):
        return coin_type in self.coin_types_dict

Node_1 = "https://mainnet.infura.io/v3/19de6a4c0ccb416287b18bc81fa0b3b1"


mysql_config = MysqlConfig()
rpc_config = RpcConfig()
coin_config = CoinConfig()
