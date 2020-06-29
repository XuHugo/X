#!/usr/bin/env python
# encoding: utf-8
'''
@author: xuqiang
@license: (C) Copyright 2013-2022.
@contact: xq-310@163.com
@software: wallet
@file: eth_db.py
@time: 2019/6/1 上午9:41
@desc:
'''
from  db.db_base import Db
from decimal import Decimal, ROUND_DOWN,getcontext

class EthDb(Db):

    def __init__(self, coin_type="eth"):
        super(EthDb, self).__init__(coin_type if coin_type else 'eth')

    def getBlockHashByNumber(self, number):
        try:
            self.execute("select hash from block where height = %s and state =1", number)
            ret = self.fetchone()
            if ret:
                return ret.get("hash")
        except Exception as e:
            print(e)

    def getParentHashByNumber(self, number):
        try:
            self.execute("select previous from block where height = %s and state =1", number)
            ret = self.fetchone()
            if ret:
                #print(ret.get("previous"))
                return ret.get("previous")
        except Exception as e:
            print(e)

    def getBlockNumber(self):
        try:
            self.execute("select max(height) as h from block where state=1")
            ret = self.fetchone()
            ret = ret['h']
            return ret if ret != None else -1
        except:
            return False

    def delete_tx_record(self, blockhash):
        sql = "delete from tx_record where blockHash=%s"
        self.execute(sql, blockhash)
        pass

    def mod_block_state(self, blockhash):
        try:
            sql = "update block set state=0 where hash=%s"
            self.execute(sql, blockhash)
        except:
            return False
        pass

    def markUnclelock(self, block_hash):
        try:
            sql = ("update block left join tx on block.hash = tx.block_hash set block.state = 0, tx.block_state = 0 "
                   "where block.hash = %s")
            self.execute(sql, block_hash)
        except:
            return False

    def insertBlockRecord(self, height, size, timestamp, hash, previous, state):
        try:
            sql = "insert into block(height, `size`, `timestamp`, hash, previous, state) values(%s) " \
                  "on DUPLICATE KEY UPDATE timestamp=values(timestamp) ,state=values(state)"
            sql = sql % ",".join(["%s"] * 6)
            self.execute(sql, height, size, timestamp, hash, previous, state)
        except:
            return False
        pass

    def related_to_user(self, address):
        try:
            sql = "select 1 from address where addr = %s limit 1"
            return address if self.execute(sql, address) else False
        except:
            return False
        pass

    def insert_tx_record(self, params):
        try:
            sql = "insert into tx_record(`nonce`, `from`, `blockHash`, `raw`, " \
                  "`rsv`,`gas`, `value`, `blockNumber`, `to`, `input`, `publicKey`, " \
                  "`transactionIndex`, `hash`, `gasPrice`, `gasUsed`, `status`, " \
                  "`mark_state`, `fee`) values(%s) on duplicate key update time=now(), raw=values(raw)," \
                  "status=values(status), mark_state=values(mark_state),blockHash=values(blockHash),"\
                  "rsv=values(rsv),gas=values(gas),blockNumber=values(blockNumber),input=values(input)," \
                  "publicKey=values(publicKey),transactionIndex=values(transactionIndex),gasUsed=values(gasUsed),fee=values(fee)"
            sql = sql % ",".join(["%s"] * 19)
            ret = self.execute(sql, params["nonce"], params["from"],
                         params["blockHash"], params["raw"], params["rsv"],params["gas"],
                         params["value"], params["blockNumber"], params["to"], params["hex_input"],
                         params["publicKey"], params["transactionIndex"], params["hash"], params["gasPrice"],
                         params["gasUsed"], params["status"], params["mark_state"], params["fee"])
            return ret
        except:
            return False
        pass

    def insert_tx_record_first(self, params):
        try:
            sql = "insert into tx_record(`nonce`, `from`, " \
                  "`value`,`to`, `hash`, `gasPrice`, " \
                  "`mark_state`,`is_token`) values(%s) on duplicate key update  " \
                  " mark_state=values(mark_state)"
            sql = sql % ",".join(["%s"] * 8)
            ret = self.execute(sql, params["nonce"], params["from"],
                               params["value"],  params["to"], params["hash"],
                               params["gasPrice"],params["mark_state"],params["is_token"])
            return ret
        except Exception as e:
            print(e)
            return False
        pass

    def update_address_table(self, user_nonce, user_amount, addr):
        try:
            sql = "update address set nonce=%s, unconfirm_amount=0, tmp_unconfirm_amount=0, amount=%s where addr=%s"
            ret = self.execute(sql, user_nonce, user_amount, addr)
            return ret
        except:
            return False
        pass

    def is_contract_address(self, address):
        # contract_addr
        try:
            self.execute("select 1 from token where lower(contract_addr) = %s limit 1; ", address.lower())
            ret = self.fetchone()
            if ret:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False
    def insert_token(self, *args):
        """contract_addr, type, fullname, name, decimals, deciml, from, canShift, logo, daddy = args"""
        try:
            sql = "insert into token(contract_addr, `type`,fullname, `name`, decimals, deciml, logo, " \
                  "daddy)  values(%s) on DUPLICATE KEY UPDATE update_time = NOW()"
            arglist = ','.join(['%s'] * len(args))
            ret = self.execute(sql % arglist, *args)
            return ret
        except Exception as e:
            return False
        pass

    def get_token_decimals(self, contract_addr):
        try:
            self.execute("select decimals from token where contract_addr = %s", contract_addr.lower())
            ret = self.fetchone()
            if ret:
                return ret.get("decimals")
            return False
        except Exception as e:
            return False

    def get_token_balance(self, contract_addr, addr):
        try:
            self.execute("select * from token_balance where `contract_addr` = %s and `addr`= %s", contract_addr, addr)
            ret = self.fetchone()
            return ret
        except Exception as e:

            return False

    def get_tx_address(self, address):
        try:
            self.execute("select * from tx_record where `from` = %s or `to` = %s", address.lower(),address.lower())
            ret = self.fetchall()
            if ret:
                return ret
            return False
        except Exception as e:
            return False

    def insert_token_balance_tx_record(self, params):
        try:
            sql = "insert into token_balance(addr, contract_addr, balance, decimals, added,unconfirm_amount) values(%s) on " \
                  " DUPLICATE KEY UPDATE balance=values(balance), unconfirm_amount=0"
            arg_list = ",".join(["%s"] * 6)
            ret = self.execute(sql % arg_list, params["addr"], params["contract_addr"],
                         params["balance"], params["decimals"], params["added"],params["unconfirm_amount"])
            return ret
        except Exception as e:
            return False
        pass

    def insert_token_tx_tx_record(self, params):
        try:
            sql = "insert into token_tx(`from_addr`, `to_addr`, `amount`, `tx_hash`, `contract_addr`, " \
                  "`decimals`, `logindex`, `block_time`,`blockNumber`," \
                  "nonce,gas,gasPrice,fee,gasUsed,status) values(%s) on duplicate key update update_time=now()" \
                  ",logindex=values(logindex) "
            sql = sql % ",".join(["%s"] * 15)
            ret = self.execute(sql, params["token_addr_from"], params["token_addr_to"], params["token_amount"],
                         params["tx_hash"], params["contract_addr"], params["token_decimals"], params["logindex"],
                         params["block_timestamp"],params["blockNumber"],params["nonce"],params["gas"],
                         params["gasPrice"],params["fee"],params["gasUsed"],params["status"])
            return ret
        except Exception as e:
            return False
        pass

    def insert_tokentx_first(self, params):
        try:
            sql = "insert into token_tx(`from_addr`, `to_addr`, `amount`, `tx_hash`, `contract_addr`, " \
                  "`decimals`, nonce) values(%s) on duplicate key update update_time=now()"
            sql = sql % ",".join(["%s"] * 7)
            ret = self.execute(sql, params["token_addr_from"], params["token_addr_to"], params["token_amount"],
                         params["tx_hash"], params["contract_addr"], params["token_decimals"],params["nonce"])
            return ret
        except Exception as e:
            return False
        pass

    def get_token_address(self, address, contract):
        try:
            self.execute("select * from token_tx where `from_addr` = %s and `contract_addr` = %s or `to_addr` = %s and `contract_addr` = %s", address.lower(), contract.lower(),address.lower(), contract.lower())
            ret = self.fetchall()
            if ret:
                return ret
            return False
        except Exception as e:
            return False

    def update_tx_record(self, param):
        try:
            sql = "update tx_record set is_token=1 where hash=%s"
            ret = self.execute(sql, param)
            return ret
        except Exception as e:
            return False
        pass

    def insert_address_new(self, wallet_id, addr, nonce, amount, balance,t_type=99, platform=1):
        try:
            sql = "insert into address (wallet_id, addr,  nonce, amount,balance,addr_type, platform) values(%s) " \
                  "on DUPLICATE KEY UPDATE update_time=now(), addr_type=values(addr_type)," \
                  "platform=values(platform)"
            sql = sql % ",".join(["%s"] * 7)
            ret = self.execute(sql, wallet_id, addr, nonce, amount,balance,t_type, platform)
            return ret
        except Exception as e:
            print(e)
            return False

    def check_address_exist(self, addr):
        try:
            sql = "select * from address where addr=%s"
            ret = self.execute(sql, addr)
            ret = self.fetchone()
            if ret:
                return ret
            else:
                return False
        except Exception as e:

            return False


if  __name__=="__main__":
    db = EthDb()
    #db.getParentHashByNumber(7894481)
    # addr="0x2683b857043c011c5ee9610f878a191a3b76461e"
    # ret = db.related_to_user(addr)
    # print(ret)
    # p={'nonce': 190, 'raw': 'raw', 'fee': 42000000000000, 'value': 53376000000000, 'gasUsed': 21000, 'status': 1, 'from': '0x2683b857043c011c5ee9610f878a191a3b76461e', 'to': '0xc03eaa21257e257cdf64e92ce6799c946af6f233', 'blockHash': '0x203367ec08821f7057cb477df0754bf18537a52379e6529211d738e4475554cc', 'rsv': '0x803955c9eb6d4d9cd4e9f2e9259df461fc8230bc7d4ce4f6ba33fa1e4fe29adc%0x7f95a3f70ce433df82d148ad023a3b9b009da2d652e069f1672e2b1d834f43d6%37', 'gas': 21000, 'blockNumber': 7894481, 'hex_input': '0x', 'publicKey': 'publicKey', 'transactionIndex': 66, 'hash': '0x4c8b372dbecbaf3dad7b99a32e5f4d3852d453720dfab35c66a083a670524a0a', 'gasPrice': 2000000000, 'block_timestamp': 1}
    # r=db.insert_tx_record(p)
    # print(r)
    # addr = "0xfc30d103a7984ecdac8bd7498ecba700c158827d"
    # addr2 = "0x5341ae85a5d67fa32d25b26ed4ef5427f4644d8f"
    # r = db.check_address_exist(addr)
    # balance = r.get("amount")
    # nonce = r.get("nonce")
    # print("user already exist!", nonce, balance)
    # print(type(balance))
    # items= db.get_tx_address("0xfc30d103a7984ecdac8bd7498ecba700c158827d")
    # infos = []
    # for item in items:
    #     tx = {}
    #     tx["to"] = item["to"]
    #     tx["hash"] = item["hash"]
    #     tx["nonce"] = item["nonce"]
    #     tx["value"] = item["value"]
    #     tx["time"] = item["time"]
    #     tx["state"] = item["mark_state"]
    #     infos.append(tx)
    # print('ssss:', len(infos))
    # result = {"result": infos}


    # a = (balance.quantize(Decimal('0.000000000')))
    # print(type(a), a)
    # print("!!!!!!")
    # b=int(a)
    # print(type(b),b)
    # r = (b * (10.0 ** 18))
    # print(type(r), r)
    token="0x33c33815a9dca51232578b30e7e0d222b57ea3ca"
    addr="0x9ca53a80ebd1d28b78f43a50e74e527284196af5"
    tb = db.get_token_address( addr,token)
    print(tb)

