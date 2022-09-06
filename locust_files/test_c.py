import time
from locust import HttpUser, task, between
from sendcxhaintx import Sender
from web3 import Web3, HTTPProvider
import random

logins = [
    'b6c327a5b8a0de76a8ca875dc8073bd53668f2b8366b22c43be2ef5161d1da6d',
    '9fe121eb41197b6e50779da5cf82f6147d7665ec52db0a65c9d99d68539d7007',
    '8753dafabd2e19aeca3d84e462d43a0e4f37d049f5869a6a2270134727fb1572',
    '3ade2c0f324986db7a92ec52366ebdd3e765e5e9b8f21b7513ecbfb96cf4ca4d',
    '2b875f301db19cddec588616100ac484e52c761d4d357cd0e2ef7f1c8c275e86',
    'a7b9046f72b74cad3ce155e5a9f19317b4b71b622fe3eadfa017f56a947b3a0b',
    'ef3bdf4336fc717aaee85869626cffa93a153921ec806f3e814fa072e8674769',
    'fa48008893729dec7e6adc0b8c4509f44ff0cf91d6c4398edf1539e8301689eb',
    '6de0ced45d39fc4028d089b2c0de2d0d10430b8e51a23b11fb5d5a8a259ba4e3',
    '9631036b64e68f5761487b7e309a9ede6c66ddec4b9cf8294ee3dc6a8fa1f0d9',
    '3454f11dece75fbaee6b26de621f6b3b61d5978d10377d00fe1bba849d85d7c5',
    'ca957d4efed6c9388ca06644b6b82f5cfbfb33b967d9772dbce21178cf0d15d6',
    '5e9cdfbffa2b6d00b8c6030887363e31622ec421408d4b0580c85aabb89cd705',
    '41e3c97855cf082125924989539b55682c30fa7416b18d1528e921962aabd51d',
    'c021a2888674512141694bae845d7962a77a5f6bf9130d50b844a37134953e5c',
    '44371ab67221a57d434529d3a545877438598f24fea3ce347daf57ff5e0d5ab7',
    'ddf2bcbed1c77d6be8060c00e7683a612257b8603ba1263d4543da72b1c24b3c',
    '5bea1d290b93c3a3a0bccabb0b77dc774304791d34fdeb9102a6408089fb4e10',
    '357d645bd0099b49a2e57eff3c2b66181f836e87687bc6d67e01410273042ef5',
    'a8f0af3eed266dd1dded30104889e6bc3fa8a7951b4e58d9d3fb9dd0ca96b74e',
    'd0d1a3652e1997a18fea10d7c10d64ad1eb4d9f57cc4bbe8c96442e54f672b9c',
    '3e0d900625f3113703a7b1f618e450a67b43f0218aa4bd9eb6e824a37a4c1336',
    'dad42c8d016128ddbd01476736ff1b0953a582d234c6afd038eae7c4f3ee7375',
    'afa1b24da5849c3f463556908a1d7d56fe4da7e0bdc14c2bbe0f1635ed41d5d7',
    'f732b2249502527b0ff4ed9f7de7698572f7c62c36ce89ab3ce9b62bcf37edc1',
    '0a326788ce0457f81933165c09a430f2f86985243f9eac3d7965ae2b415fa1b7',
    '33e09f608fa082955d0eefa2d0cb5821781cf7aa71ec308eb973a58fb7b2d6f7',
    '99f83ece5e5d9a35936cc842229ec4694987978f68fe7d3e3ddbfd76208f1cd6',
    '21c6a55a1c559413be15c8003abd2f50bec3d5c8ae132d3d804f2b51f9a7b70b',
    '871d7de34676b041ebd233a5b93f6f994412d9c4605a78bb898d1818fd2acd0d',
    '8de7c929843b763d62f0a62ff67493a489cee0534a06792b1ddc37456bca5ae5',
    'a405eb297d2ea5cf19b68bb61f4d454c9db802c65c047291c741090b7a23c7c6',
    '39984619a1bad88524f9a8c7da8a54f2ee506ce43fd9a3fc177c0d0b107912c7',
    '949304a8521ebf4256d62c7d8615154324694ebce2904a27c7512a9cbd74e656',
    '2319db57360b91f33aed4dcddf6b726962bf14ae20e8dc2e3dab215eb844ee1b'
]

random.shuffle(logins)
login_pass = [x for x in logins]


class CChainLocustTest(HttpUser):
    rpc_node = "http://127.0.0.1:9650/ext/bc/C/rpc"

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
