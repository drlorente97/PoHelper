# General Declarations
from web3 import Web3

class EthConnector:
    def __init__(self, testnet=False):
        #Select Network
        if testnet == True:
            full_node = 'https://ropsten.infura.io/v3/53d4e926836541a48f44272f4fa0c0fd'
        else:
            full_node = 'https://mainnet.infura.io/v3/53d4e926836541a48f44272f4fa0c0fd'

        # Start API
        self.w3 = Web3(Web3.HTTPProvider(full_node))

    def balance(self, address):
        csAddress = self.checksum(address)
        balance_wei = self.w3.eth.get_balance(csAddress)
        balance = round(self.w3.fromWei(balance_wei, "ether"),5)
        return balance
    
    def validate(self, address):
        is_valid = bool(self.w3.isAddress(address))
        return is_valid

    def checksum(self, address):
        if self.w3.isChecksumAddress(address) == False:
            csAddress = self.w3.toChecksumAddress(address)
        else:
            csAddress = address
        return csAddress
