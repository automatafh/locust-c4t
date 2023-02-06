import time
from locust import HttpUser, task, between
from sendcxhaintx import Sender
from web3 import Web3, HTTPProvider
import random

class CChainLocustTest(HttpUser):

    chainId = 502

    #account with funds used to send funds to the new accounts, by the default is the ewoq account.
    default_address_with_funds = "7a14fdf6bb1d53e28384f70209280dd8848bdc96b5f9eb7fdde9fcddc7ef1a0d"
    
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

        self.client = Sender(self.web3, account.privateKey.hex(), account.address, self.chainId, request_event=environment.events.request)

    @task
    def send_c_chain_tx(self):
        result = self.client.send_tx()
        # autoincrement nonce
        return result

    def send_funds(self, account):

        transaction_data = {
            'nonce' : self.web3.eth.getTransactionCount(self.account_with_funds.address),
            'maxFeePerGas': 50000000000,
            'maxPriorityFeePerGas': 1000000000,
            'gas': 100000,
            'to': account.address,
            'from': self.account_with_funds.address,
            'value': self.web3.toWei(1, 'ether'),
            'chainId': self.chainId
        }

        signed_transaction = self.web3.eth.account.signTransaction(transaction_data, self.account_with_funds.privateKey.hex())
        send_transaction_hash = self.web3.eth.sendRawTransaction(signed_transaction.rawTransaction)
        receipt = self.web3.eth.wait_for_transaction_receipt(send_transaction_hash, timeout=500)