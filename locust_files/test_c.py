import time
from locust import HttpUser, task, between
from sendcxhaintx import Sender
from web3 import Web3, HTTPProvider
import random
import config.config_c_chain as config

class CChainLocustTest(HttpUser):

    chain_id = config.CHAIN_ID

    #account with funds used to send funds to the new accounts, by the default is the ewoq account.
    default_address_with_funds = config.DEFAULT_ADDRESS_WITH_FUNDS
    
    #Locust creates an instance of this class for each simulated user that is to be spawned.
    def __init__(self, environment):
        super().__init__(environment)

        #read the host
        self.rpc_node = environment.host

        # initialize web3
        self.web3 = Web3(HTTPProvider(self.rpc_node))

        #load account with private key
        self.account_with_funds = self.web3.eth.account.privateKeyToAccount(self.default_address_with_funds)

        #create new account using web3
        account = self.web3.eth.account.create()
        self.send_funds(account)

        self.nonce = self.web3.eth.getTransactionCount(account.address)
        self.client = Sender(self.web3, self.nonce, account.privateKey.hex(), account.address, self.chain_id, 
        request_event=environment.events.request)

    @task
    def send_c_chain_tx(self):
        result = self.client.send_tx()
        # autoincrement nonce
        return result

    def send_funds(self, account):

        transaction_data = {
            'nonce' : self.web3.eth.getTransactionCount(self.account_with_funds.address),
            'maxFeePerGas': config.MAX_FEE_PER_GAS,
            'maxPriorityFeePerGas': config.MAX_PRIORITY_FEE_PER_GAS,
            'gas': config.GAS,
            'to': account.address,
            'from': self.account_with_funds.address,
            'value': self.web3.toWei(1, config.TOWEI_VALUE),
            'chainId': self.chain_id
        }

        signed_transaction = self.web3.eth.account.signTransaction(transaction_data, self.account_with_funds.privateKey.hex())
        send_transaction_hash = self.web3.eth.sendRawTransaction(signed_transaction.rawTransaction)
        self.web3.eth.wait_for_transaction_receipt(send_transaction_hash, timeout=config.TIMEOUT)