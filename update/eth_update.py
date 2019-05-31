# -*- coding:utf-8 -*-
from db.eth_db  import EthDb
from rpc.eth_rpc_client  import EthRpcClient
from common.tools import *
import time
import sys

class EthBlockUpdater(object):

    def __init__(self, min_height=0):
        self.coin_type = 'eth'
        self.rpc = EthRpcClient()
        self.db = EthDb()
        self.mempool_sleep_time = waitting_pending_block_config.eth
        self.sleep_time = 0
        self.min_height = int(min_height)
        self.max_rollback_block = max_rollback_block_config.eth
        self.way = eth_way

    def update(self):

        number = max(self.min_height, int(self.db.getBlockNumber()))
        while True:

            db_number = int(self.db.getBlockNumber())
            rpc_number = int(self.rpc.getBlockNumber())

            number = self.fork_handler(number)


    def fork_handler(self, number):

        while number >= self.min_height:
            rpc_blockhash = self.rpc.getBlockHashByNumber(number)
            db_blockhash = self.db.getBlockHashByNumber(number)

            if rpc_blockhash   == db_blockhash:
                return
            else:
                logger.info("rollback block %s",number)
                self.db.delete_tx_record(db_blockhash)
                self.db.modif_block_state(db_blockhash)
                self.db.commit()
            number -= 1
        exit("stop rollback at blocknumber %d!!!" % number)

    def process_block(self, number):

        block_date,transactions = self.rpc.getTansactionByBlockNumber(number)
        self.store_block_data(block_date)
        self.process_transactions(transactions)

        logger.info('processing block...')
        self.database_operation(block_data, number, treated_tx, block_state, state)

        self.process_txs(txs, height, int(block_data["timestamp"], 16), block_state=1, pending_block=0, commit=False)
        # self.db.update_asset(height, self.rpcClient, commit = False)

    def store_block_data(self, block_data):
        height, size, timestamp = (block_data["number"], block_data["size"],
                                                        block_data["timestamp"])
        hash = block_data["hash"]
        previous = block_data["parentHash"]
        state = 1
        self.db.insertBlockRecord(height, size, timestamp, hash, previous, state)

    def process_transactions(self, transactions):
        for transaction in transactions:
            self.process_transaction(transaction)
        pass

    def process_transaction(self, transaction):
        account1, account2 = self.db.related_to_the_user(addr_from), \
                             self.db.related_to_the_user(addr_to)\

        tx_receipt = None
        tx_receipt = self.rpc.eth_getTransactionReceipt(params["hash"])
        if any([account1, account2]):
            #tx_receipt = self.rpc.eth_getTransactionReceipt(params["hash"])
            gas_used, status = self.dispose_hex_data(tx_receipt['gasUsed'], tx_receipt['status'])
            fee = self.format_value(gas_used * params["gasPrice"], self.precision)
            value = self.format_value(params["value"], self.precision)

            params["fee"] = fee
            params["value"] = value
            params["gasUsed"] = gas_used
            params["status"] = status
            params["from"] = addr_from
            params["to"] = addr_to

            self.db.insert_tx_record(params)
            self.db.diff_tx_extra_info(1, params["hash"])
            logger.info("insert_tx_record account1=%s account2=%s", account1, account2)
            # 删除token_tx记录
            self.db.delete_token_tx_record(params["hash"])
            # todo  更新账户余额和nonce
            if len(addr_from) > 2:
                user_nonce1, user_amount1 = self.rpc.eth_getTransactionCount(addr_from), self.rpc.eth_getBalance(
                    addr_from)
                self.db.update_address_table(user_nonce1, self.format_value(user_amount1, self.precision), addr_from)

            if len(addr_to) > 2:
                user_nonce2, user_amount2 = self.rpc.eth_getTransactionCount(addr_to), self.rpc.eth_getBalance(addr_to)
                self.db.update_address_table(user_nonce2, self.format_value(user_amount2, self.precision), addr_to)
        #检测合约内部eth转账
        #txreceipt = self.rpc.eth_getTransactionReceipt(params["hash"])
        try:
            if tx_receipt and tx_receipt["logs"]:
                self.contract_internal_transactions_analyze(tx_receipt["logs"],params["hash"])
        except Exception as e:
            logger.error("contract_internal_transactions_analyze error! %s", e)
        # 处理token交易
        self.process_token(params, tx_receipt)
        pass

    def process_token(self, params, tx_receipt):
        __token_call = self.rpc.eth_call
        if tx_receipt:
            pass
        else:
            try:
                tx_receipt = self.rpc.eth_getTransactionReceipt(params["hash"])
            except Exception as ex:
                logger.error("Error for eth_getTransactionReceipt,%s", ex)
                return

        if tx_receipt["logs"] is None:
            return
        # 根据erc20标志，token交易都会出发transfer事件，
        for log in tx_receipt["logs"]:
            try:
                if log["topics"] and log["topics"][0] == _TRANSACTION_TOPIC:
                    contract_addr = log["address"]

                    token_addr_from, token_addr_to, logindex, token_amount = self.analysis_logs(log)
                    token_addr_from, token_addr_to = self.format_address(token_addr_from, token_addr_to)

                    # 判断是否是atoken用户
                    account1, account2 = self.db.related_to_the_user(token_addr_from), \
                                         self.db.related_to_the_user(token_addr_to)
                    if any([account1, account2]):
                        # 更新合约和精度
                        self.updata_contract_addr(contract_addr)
                        token_decimals = self.db.get_token_decimals(contract_addr)

                        if not token_decimals:
                            token_decimals = __token_call(to_address=contract_addr, data=_DECIMALS)
                            token_decimals = self.dispose_hex_data(token_decimals)[0]

                        param = dict(
                            token_decimals=token_decimals,
                            token_amount=token_amount,
                            token_addr_from=token_addr_from,
                            token_addr_to=token_addr_to,
                            logindex=logindex,
                        )

                        self.token_tx_insert(contract_addr, tx_receipt, params, param)
                        self.token_balance_updata(contract_addr, token_addr_from, token_addr_to, token_decimals)
                    else:
                        # 非atoken用户
                        pass
                else:
                    pass
            except Exception as ex:
                logger.error("Error for tx_receipt,%s", ex)
        pass

