# Readme

- when creating a local blockchain by default will be a wallet with enough funds to create the users.

for each user the script automatically will create and address and send 1 AVAX to run the transactions.

## Requirements

- Network Runner running
- Python >= 3.7 
 
## Configuration 

On locust_files/test_c.py

- Deploy "SimpleContract" and set contract address
- Set the Private Key With the funds to create the Users.

On test_c_chain_local.conf
    
- set the RPC node and the users, these parameters will load by default.

## Execution

 execute bash script loadtesting.sh, Locust will create a server on 8089
