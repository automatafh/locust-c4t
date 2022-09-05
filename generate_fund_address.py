from web3 import Web3, HTTPProvider

rpc_node = "http://44.210.106.38:8083/ext/bc/C/rpc"
web3 = Web3(HTTPProvider(rpc_node))
private_key = '56289e99c94b6912bfc12adc093c9b51124f0dc54ac7a766b2bc5ccf558d8027'
address_from = web3.eth.account.privateKeyToAccount(private_key)
web3.eth.accounts.wallet.add(private_key)
for n in range(2):
    address_to = web3.eth.account.create()

    transfer = web3.eth.send_transaction({'from': address_from.address, 'to': address_to.address,
                                          'value': web3.toWei(100000, 'ether')})
    print(address_to.address)
    print(transfer)
