import time
from locust import HttpUser, task, between
from sendcxhaintx import Sender
from web3 import Web3, HTTPProvider
import random

logins = [
    '56289e99c94b6912bfc12adc093c9b51124f0dc54ac7a766b2bc5ccf558d8027',
    'f64dcb0f694d39a5ca05df858d007b89db5332a78b5fbaa944726e45df2bd61e',
    'f5dbb3f1be6941d5fb66ec1d93873738dbf1a5f9c7d9e6066d4f924badf74660',
    '78615cfa19828d41b0fcd15c1f4931c00a9c80c702e77c9548beaade73b6d1c7',
    '8d3f2f5a9f47e87154e68f38e83739c569b3829c1a6b222d15c5da8992a5b4cb',
    'e3576b1ac0289e3fb31b4894ac54a03bcbd031cb53817e6e782dd151b4e7bcbf',
    'b618024f827fef747992d2c4eb48c04dfe332de902d1ed3c930159b739557162',
    '9af43367f63e5884a18eee6cdf19d19dde635e56f5063deb550aa47ca29a7e44',
    'b8468781145be9855ccd9d43ae90402db5afa7dc3759a0f955c67164c872f65f',
    '01e0ed9809d28cddaa2dfb9a24560912bf39f42285425467016ab0870cf7bce6',
    'd0423a7de3af5c9cb3fa8766fcb5fc6f08412dde9fad3d26ca06d98078f62a1e'
]

random.shuffle(logins)
login_pass = [x for x in logins]


class CChainLocustTest(HttpUser):
    rpc_node = "http://44.210.106.38:8083/ext/bc/C/rpc"

    def __init__(self, environment):
        print(self)
        # initialize web3
        self.web3 = Web3(HTTPProvider(self.rpc_node))

        # convert private key to account using web3
        private_key = login_pass.pop()
        account = self.web3.eth.account.privateKeyToAccount(private_key)
        account = account.address
        super().__init__(environment)
        self.nonce = self.web3.eth.getTransactionCount(account)
        self.client = Sender(self.web3, self.nonce, private_key, account, request_event=environment.events.request)

    @task
    def send_c_chain_tx(self):
        result = self.client.send_tx()
        # autoincrement nonce
        return result
