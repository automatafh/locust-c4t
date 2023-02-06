# Read me

- when creating a local blockchain by default a wallet will be created with enough funds to create users.

## Description
the test_c.py file contains the funding transaction, where the desired value to send to the accounts to be created is defined.
in this same file in line 12 is defined the main private key from which funds will be sent to the accounts initially created.
then in the file sendcxhaintx.py is the transaction that will be executed repeatedly to create network load.
these transactions are executed from one account to the same account then you must make sure that the initial offers sent are sufficient to complete your tests.

## Requirements

- Local node running on port 9650
- Python >= 3.7 
 
## Configuration 

In locust_files/test_c.py

- Deploy "SimpleContract" and set the contract address.
- Set the private key with the funds to create the users.
- In the transaction found in this file set the initial value of funds to be transferred to each of the accounts.

In test_c_chain_coper.conf

- set the RPC node and the users, these parameters will be loaded by default.

## Execution

 run the bash script loadtesting.sh, Locust will create a server on 8089