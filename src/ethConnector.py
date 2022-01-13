# General Declarations
from web3 import Web3
from eth_account.messages import encode_defunct

class EthConnector:
    def __init__(self, testnet=False):
        #Select Network
        if testnet == True:
            full_node = 'https://ropsten.infura.io/v3/53d4e926836541a48f44272f4fa0c0fd'
        else:
            full_node = 'https://mainnet.infura.io/v3/53d4e926836541a48f44272f4fa0c0fd'

        # Load PoH contract address
        self.poh_contract = '0xC5E9dDebb09Cd64DfaCab4011A0D5cEDaf7c9BDb'

        # Load PoH contract ABI
        try:
            f = open('abi.json')
            self.abi = json.load(f)
            f.close()
        except:
            None

        # Start API
        self.w3 = Web3(Web3.HTTPProvider(full_node))

    def balance(self, address):
        csAddress = self.checksum(address)
        balance_wei = self.w3.eth.get_balance(csAddress)
        balance = round(self.w3.fromWei(balance_wei, "ether"),5)
        return balance

    def validate_address(self, address):
        is_valid = bool(self.w3.isAddress(address))
        return is_valid

    def checksum(self, address):
        if self.w3.isChecksumAddress(address) == False:
            csAddress = self.w3.toChecksumAddress(address)
        else:
            csAddress = address
        return csAddress

    def validate_signature(self, message, signature, original_address):
        encoded_message = encode_defunct(text=message)
        try:
            signature_address = w3.eth.account.recover_message(message, signature=signed_message.signature)
            if signature_address == original_address:
                return True
            else:
                return False
        except:
            return "BadSignature"

    def validate_humanity(self, address):
        try:
            contractDeployed = w3.eth.contract(address=self.poh_contract, abi=self.abi)
            is_human = contractDeployed.functions.isRegistered(address).call()
            return is_human
        except:
            return "UnknownError"
