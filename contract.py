import time
import json
import web3
from eth_account import Account
from web3.auto import w3
from web3.providers.websocket import WebsocketProvider
from web3 import Web3
from solc import compile_standard
from solcx import install_solc
install_solc(version='latest')
from solcx import compile_source

with open("Greeter.sol") as c:
 contractText=c.read()
with open("../.pk") as pkfile:
 privateKey=pkfile.read()
with open("../.infura") as infurafile:
 infuraKey=infurafile.read()

compiled_sol = compile_source(contractText, output_values=["abi", "bin"])
contract_id, contract_interface = compiled_sol.popitem()
bytecode = contract_interface['bin']
abi = contract_interface['abi']

#diagnostics
#print(abi)
#print(bytecode)

W3 = Web3(WebsocketProvider('wss://ropsten.infura.io/ws/v3/%s'%infuraKey))
account1=Account.from_key(privateKey);
address1=account1.address
Greeter = W3.eth.contract(abi=abi, bytecode=bytecode)

nonce = W3.eth.getTransactionCount(address1)
#GroupD
#print(nonce)
# Submit the transaction that deploys the contract
tx_dict = Greeter.constructor().buildTransaction({
  'chainId': 3,
  'gas': 1400000,
  'gasPrice': w3.toWei('40', 'gwei'),
  'nonce': nonce,
  'from':address1
})

signed_txn = W3.eth.account.sign_transaction(tx_dict, private_key=privateKey)
#diagnostics
#print(signed_txn)
print("Deploying the Smart Contract")
result = W3.eth.sendRawTransaction(signed_txn.rawTransaction)
#diagnostics
#print(result)
#print('-----------------------------------')
tx_receipt = None#W3.eth.getTransactionReceipt(result)

count = 0
while tx_receipt is None and (count < 30):
  time.sleep(2)
  try:
    tx_receipt = W3.eth.getTransactionReceipt(result)
  except:
    print('.')

if tx_receipt is None:
  print (" {'status': 'failed', 'error': 'timeout'} ")
#diagnostics
#print (tx_receipt)

print("Contract address is:",tx_receipt.contractAddress)

greeter = W3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=abi
)
print("Output from greet()")
print(greeter.functions.greet().call())

nonce = W3.eth.getTransactionCount(address1)
tx_dict = greeter.functions.setGreeting('Hello, this is Group D - executing smart contract for TRADE FINANCE').buildTransaction({
  'chainId': 3,
  'gas': 1400000,
  'gasPrice': w3.toWei('40', 'gwei'),
  'nonce': nonce,
  'from':address1
})

signed_txn = W3.eth.account.sign_transaction(tx_dict, private_key=privateKey)
result = W3.eth.sendRawTransaction(signed_txn.rawTransaction)
tx_receipt = None#W3.eth.getTransactionReceipt(result)

count = 0
while tx_receipt is None and (count < 30):
  time.sleep(2)
  try:
    tx_receipt = W3.eth.getTransactionReceipt(result)
  except:
    print('.')

if tx_receipt is None:
  print (" {'status': 'failed', 'error': 'timeout'} ")

#tx_hash = greeter.functions.setGreeting('Nihao').transact({"from":account1.address})
#tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print("Output from greet()")
print(greeter.functions.greet().call({"from":account1.address}))
#'GroupD'
