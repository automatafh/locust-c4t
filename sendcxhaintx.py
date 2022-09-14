import json
import time
import config.config_c_chain as config

class Sender:

    contract_address = config.CONTRACT_ADDRESS

    def __init__(self, web3, nonce, private_key, address_from, chain_id, request_event):
        self._request_event = request_event
        self.web3 = web3
        self.private_key = private_key
        self.address_from = address_from
        self.nonce = nonce
        self.chain_id = chain_id

    # python function to send a transaction to the blockchain

    def send_tx(self):

        request_meta = {
            "request_type": config.REQUEST_TYPE,
            "name": config.NAME,
            "start_time": time.time(),
            "response_length": 0,  # calculating this for an xmlrpc.client response would be too hard
            "response": None,
            "context": {},  # see HttpUser if you actually want to implement contexts
            "exception": None,
        }

        start_perf_counter = time.perf_counter()

        try:

            # use web3 to load contract with abi and contract address
            with open('abi.json') as f:
                abi = json.load(f)

            contract = self.web3.eth.contract(abi=abi, address=self.contract_address)
            data = contract.encodeABI(fn_name="store", args=[10])

            # with EIP1559 It is not necessary to send the gas price and gas limit.
            transaction_data = {
                'nonce': self.nonce,
                'maxFeePerGas': config.MAX_FEE_PER_GAS,
                'maxPriorityFeePerGas': config.MAX_PRIORITY_FEE_PER_GAS,
                'gas': config.GAS,
                'from': self.address_from,
                'to': self.contract_address,
                'value': self.web3.toHex(0),
                'data': data,
                'chainId': self.chain_id
            }

            # use web3 to sign transaction
            signed_transaction = self.web3.eth.account.signTransaction(transaction_data, self.private_key)

            # send signed transaction to the network
            send_transaction_hash = self.web3.eth.sendRawTransaction(signed_transaction.rawTransaction)

            # get transaction hash
            get_transaction_hash = self.web3.toHex(send_transaction_hash)
            self.web3.eth.wait_for_transaction_receipt(get_transaction_hash, timeout=config.TIMEOUT)

        except Exception as e:
            request_meta["exception"] = e

        request_meta["response_time"] = (time.perf_counter() - start_perf_counter) * 1000
        self._request_event.fire(**request_meta)  # This is what makes the request actually get logged in Locust

        self.nonce += 1
        print("account ", str(self.address_from) + " - " + str(self.nonce))
        return request_meta

