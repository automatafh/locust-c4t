import json
import time

class Sender:

    def __init__(self, web3,private_key, address_from, chainId, request_event):
        self._request_event = request_event
        self.web3 = web3
        self.private_key = private_key
        self.address_from = address_from
        self.chainId = chainId

    # python function to send a transaction to the blockchain

    def send_tx(self):

        request_meta = {
            "request_type": "xmlrpc",
            "name": "Cchain",
            "start_time": time.time(),
            "response_length": 0,  # calculating this for an xmlrpc.client response would be too hard
            "response": None,
            "context": {},  # see HttpUser if you actually want to implement contexts
            "exception": None,
        }

        #querying nonce
        nonce = self.web3.eth.getTransactionCount(self.address_from)
        start_perf_counter = time.perf_counter()

        try:
            # with EIP1559 It is not necessary to send the gas price and gas limit.
            transaction_data = {
                'nonce': nonce,
                'maxFeePerGas': 50000000000,
                'maxPriorityFeePerGas': 1000000000,
                'gas': 100000,
                'from': self.address_from,
                'to':  self.address_from,
                'value':  self.web3.toWei(0.001, 'ether'),
                'chainId': self.chainId
            }

            # use web3 to sign transaction
            signed_transaction = self.web3.eth.account.signTransaction(transaction_data, self.private_key)

            # send signed transaction to the network
            send_transaction_hash = self.web3.eth.sendRawTransaction(signed_transaction.rawTransaction)

            # get transaction hash
            get_transaction_hash = self.web3.toHex(send_transaction_hash)
            receipt = self.web3.eth.wait_for_transaction_receipt(get_transaction_hash, timeout=500)
            print("receipt :", receipt["status"],"nonce",nonce,"account:",self.address_from)

        except Exception as e:
            request_meta["exception"] = e

        request_meta["response_time"] = (time.perf_counter() - start_perf_counter) * 1000
        self._request_event.fire(**request_meta)  # This is what makes the request actually get logged in Locust

        print("account ", str(self.address_from) + " - " + str(nonce))
        return request_meta

