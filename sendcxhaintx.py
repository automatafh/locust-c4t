# import web3
import json
import time
from web3 import Web3, HTTPProvider

class Sender():

    addressFrom = "0x8db97C7cEcE249c2b98bDC0226Cc4C2A57BF52FC"
    contractAddress = "0xb6a59DAEB45eB5fEBA2F5E84719cBd58cbFD3F2b"
    gasPrice = 50000000000   
    gasLimit = 21216

    def __init__(self, web3, nonce, privatekey, addressfrom, request_event):
        self._request_event = request_event
        self.web3 = web3
        self.privatekey = privatekey
        self.addressfrom = addressfrom
        self.nonce = nonce

    #python functtion to send a transaction to the blockchain
    def sendtx(self):

        request_meta = {
            "request_type": "xmlrpc",
            "name": "Cchain",
            "start_time": time.time(),
            "response_length": 0,  # calculating this for an xmlrpc.client response would be too hard
            "response": None,
            "context": {},  # see HttpUser if you actually want to implement contexts
            "exception": None,
        }
        
        start_perf_counter = time.perf_counter()

        try:

            #use web3 to load contract with abi and contract address
            with open('abi.json') as f:
                abi = json.load(f)

            contract = self.web3.eth.contract(abi=abi, address=self.contractAddress)
            data = contract.encodeABI(fn_name="store", args=[10])

            #with EIP1559 It is not necessary to send the gas price and gas limit.
            txData = {
                'nonce': self.nonce,
                'maxFeePerGas' : 50000000000,
                'maxPriorityFeePerGas' : 1000000000,
                'gas': 100000,
                'from': self.addressfrom,
                'to': self.contractAddress,
                'value': self.web3.toHex(0),
                'data': data,
                'chainId': 43112
            }

            #use web3 to sign transaction
            signedTx = self.web3.eth.account.signTransaction(txData, "0x" + self.privatekey)

            #send signed transaction to the network
            txHash = self.web3.eth.sendRawTransaction(signedTx.rawTransaction)

            #get transaction hash
            txHash = self.web3.toHex(txHash)
            receipt = self.web3.eth.wait_for_transaction_receipt(txHash, timeout=500)
            print(receipt.status)
            request_meta["response"] = receipt
        
        except Exception as e:
            request_meta["exception"] = e


        request_meta["response_time"] = (time.perf_counter() - start_perf_counter) * 1000
        self._request_event.fire(**request_meta)  # This is what makes the request actually get logged in Locust

        self.nonce += 1
        print("account ", str(self.addressfrom) + " - " + str(self.nonce))  
        return request_meta

    def sendxchaintx(self):
        pass