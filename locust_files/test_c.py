import time
from locust import HttpUser, task, between, events
from sendcxhaintx import Sender
from web3 import Web3, HTTPProvider
import random
import config.config_c_chain as config
import configparser

@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--default_address_with_funds", type=str, env_var="LOCUST_MY_ARGUMENT", default="", help="It's working")
    # Set `include_in_web_ui` to False if you want to hide from the web UI
    parser.add_argument("--my-ui-invisible-argument", include_in_web_ui=False, default="I am invisible")

@events.test_start.add_listener
def _(environment, **kw):
    print(f"Custom argument supplied: {environment.parsed_options.default_address_with_funds}")


# read_accounts = open("locust_files/accounts.txt","r")
# accounts =  read_accounts.readlines()

class CChainLocustTest(HttpUser):

    conf = configparser.ConfigParser()
    chain_id = config.CHAIN_ID

    #account with funds used to send funds to the new accounts, by the default is the ewoq account.
    default_address_with_funds = ''

    #Locust creates an instance of this class for each simulated user that is to be spawned.
    def __init__(self, environment):
        super().__init__(environment)

        #read the host
        self.rpc_node = environment.host

        # initialize web3
        self.web3 = Web3(HTTPProvider(self.rpc_node))
        self.default_address_with_funds = environment.parsed_options.default_address_with_funds
        #load account with private key
        self.account_with_funds = self.web3.eth.account.privateKeyToAccount(self.default_address_with_funds)
        #create new account using web3
        account = self.web3.eth.account.create()
        #account = self.web3.eth.account.privateKeyToAccount(accounts.pop())
        print("Account created: " + account.address)
        self.send_funds(account)
        self.nonce = self.web3.eth.getTransactionCount(account.address)
        self.client = Sender(self.web3, self.nonce, account.privateKey.hex(), account.address, self.chain_id,
        request_event=environment.events.request)


    @task
    def send_c_chain_tx(self):
        result = self.client.send_tx()
        #autoincrement nonce
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
