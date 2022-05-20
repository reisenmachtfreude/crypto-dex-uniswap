import sys, os
import json
import web3
import ERC20_ABI

# Paths and includes
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
workspace_root = os.path.dirname(project_dir)
sys.path.append(project_dir)
sys.path.append(workspace_root)

geth_ipc_path = os.path.join(os.getenv("HOME"),'.ethereum/geth.ipc')
if not os.path.exists(geth_ipc_path):
	raise Exception("ME: Please make sure eth light node is reachable under %s" % geth_ipc_path)

w3 = web3.Web3(web3.Web3.IPCProvider(geth_ipc_path))
print(w3.eth.get_block('latest')['number'])
uniswap_contract = '0x5c69bee701ef814a2b6a3edd4b1652cb9cc5aa6f'
checksum_address =  web3.Web3.toChecksumAddress(uniswap_contract)

# ABI read from https://etherscan.io/address/0x5c69bee701ef814a2b6a3edd4b1652cb9cc5aa6f#code
abi_folder = os.path.join(project_dir, 'data', 'abi')
with open(os.path.join(abi_folder, 'uniswap_v2_main.json')) as f:
	uniswap_main_contract_abi = json.load(f)
with open(os.path.join(abi_folder, 'uniswap_v2_pair.json')) as f:
	uniswap_pair_contract_abi = json.load(f)
with open(os.path.join(abi_folder, 'erc20.json')) as f:
	erc20_contract_abi = json.load(f)

contract_instance = w3.eth.contract(address=checksum_address, abi=uniswap_main_contract_abi)

# read state:
all_pairs_length = contract_instance.functions.allPairsLength().call()
print(all_pairs_length)

def _getNameOfErc20(token_addr):
	address = w3.toChecksumAddress(token_addr)
	token_contract = contract = w3.eth.contract(address, abi=erc20_contract_abi)

	print(token_contract.functions.symbol().call())
	print(token_contract.functions.name().call())



# Read all pairs contract addresses
for i in range(1, all_pairs_length):
  pair_addr = contract_instance.functions.allPairs(i).call()
  print(pair_addr)
  pair_checksum_addr = web3.Web3.toChecksumAddress(pair_addr)
  contract = w3.eth.contract(address=pair_checksum_addr, abi=uniswap_pair_contract_abi)
#   symbol = contract.functions.name().call() # This is always Uniswap V2
  token0 = contract.functions.token0().call()
  token1 = contract.functions.token1().call()
  _getNameOfErc20(token0)
  _getNameOfErc20(token1)
