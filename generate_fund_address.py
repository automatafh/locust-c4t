from web3 import Web3, HTTPProvider

rpc_node = "https://columbus.camino.foundation/ext/bc/C/rpc"
web3 = Web3(HTTPProvider(rpc_node))

private_key = '981248d80aee4ee030a17b285306ceb84e641f02ad48f86de43c7502dda340c0'
account_from = web3.eth.account.privateKeyToAccount(private_key)

for n in range(10):
    address_to = web3.eth.account.create()
    print(address_to.privateKey.hex())

    transaction_data = {
        'nonce' : web3.eth.getTransactionCount(account_from.address),
        'maxFeePerGas': 50000000000,
        'maxPriorityFeePerGas': 1000000000,
        'gas': 100000,
        'to': address_to.address,
        'from': account_from.address,
        'value': web3.toWei(1, 'ether'),
        'chainId': 502
    }

    signed_transaction = web3.eth.account.signTransaction(transaction_data, "0x" + private_key)
    send_transaction_hash = web3.eth.sendRawTransaction(signed_transaction.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(send_transaction_hash, timeout=500)