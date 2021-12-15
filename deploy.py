from solcx import compile_standard, install_solc
from web3 import Web3
from dotenv import load_dotenv
import json
import os

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simpleStorageFile = file.read()

# Complie solidity code
install_solc("0.8.10")
compiledSol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simpleStorageFile}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.10",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiledSol, file)


# Get bytecode
bytecode = compiledSol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# Get abi
abi = compiledSol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# Connect to ganache
w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/42a9caa3e9f94585b8d6360fb17c8a95")
)
chainId = 4
address = "0xD53cB28A4290360712C417E7De2a20375D09BF37"
privateKey = os.getenv("PRIVATE_KEY")  # Add 0x in front

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the latest transaction
nonce = w3.eth.getTransactionCount(address)

# 1. Build a transaction
print("Deploying contract...")
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chainId,
        "gasPrice": w3.eth.gas_price,
        "from": address,
        "nonce": nonce,
    }
)

# 2. Sign a transaction
signedTx = w3.eth.account.sign_transaction(transaction, private_key=privateKey)

# 3. Send a signed transaction
txHash = w3.eth.send_raw_transaction(signedTx.rawTransaction)
txReceipt = w3.eth.wait_for_transaction_receipt(txHash)
print("Deployed!")


# Working with the contract
# Contract Address
# Contract ABI
simple_storage = w3.eth.contract(address=txReceipt.contractAddress, abi=abi)

# Call -> Simulate making the call and getting a return value
# Transact -> Actually make a state change
# print(simple_storage.functions.retrieve().call())

print("Updating contract...")
storeTransaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chainId,
        "gasPrice": w3.eth.gas_price,
        "from": address,
        "nonce": nonce + 1,
    }
)

signedStoreTx = w3.eth.account.sign_transaction(
    storeTransaction, private_key=privateKey
)

storeTxHash = w3.eth.send_raw_transaction(signedStoreTx.rawTransaction)
storeTxReceipt = w3.eth.wait_for_transaction_receipt(storeTxHash)
print("Updated!")
