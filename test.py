import time
from locust import HttpUser, task, between
from sendcxhaintx import Sender
from web3 import Web3, HTTPProvider
import random


logins = [ 
            '56289e99c94b6912bfc12adc093c9b51124f0dc54ac7a766b2bc5ccf558d8027',
            'f80b9b8e2ec9cd662acd5dc8055f715085004f2e5e1eb5185685e7a75a10eb93',
            '8f7f0166bb337c9789dac186dad1b9521147d1a3b26d7b0c45d02351daf7548c',
            'b1fe390e4daf53a07ac617713441aefa80e0dc41c3a92e0f7f1acb3d97956386',
            '34233709fc9d0afad8a6718715e0c69f426942cddab656ceb06006047d13c955'
        ]

random.shuffle(logins)
login_pass = [(elem) for elem in logins]

class MyUser(HttpUser):

    rpcnode = "http://127.0.0.1:55338/ext/bc/C/rpc"

    def __init__(self, environment):

        print(self)
        #initialize web3
        self.web3 = Web3(HTTPProvider(self.rpcnode))

        #convert private key to account using web3
       
        privatekey = login_pass.pop()
        account = self.web3.eth.account.privateKeyToAccount(privatekey)
        account = account.address
        super().__init__(environment)
        self.nonce = self.web3.eth.getTransactionCount(account)
        self.client = Sender(self.web3, self.nonce, privatekey, account, request_event=environment.events.request)

    #wait_time = between(1, 5)

    @task
    def sendcchaintx(self):

        result = self.client.sendtx()
        #autoincrement nonce
        return result