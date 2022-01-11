# General Declarations
import ethConnector
import time
import datetime
from telepot.namedtuple import KeyboardButton, ReplyKeyboardMarkup

class general():
    def __init__(self, telegram, database):
        '''
        Constructor
        '''
        # Connect to web3
        self.eth = ethConnector.EthConnector(self.props.testnet)

        # Set up alias
        self.db = databased
        self.bot = telegram.bot
        self.props = telegram.props
        self.log = telegram.log
        self.msg = telegram.sendMsg

class private(general):
    def __init__(self, bot, database):
        super().__init__(bot, database)

class admin(general):
    def __init__(self, bot, database):
        super().__init__(bot, database)

class crowdfunding(general):
    def __init__(self, bot, database):
        super().__init__(bot, database)

    def check_balance(self, msg):
        if len(text.split()) == 1:
            self.sendMsg(chat_id, "Por favor proporcione su direccion de Ethereum a continuacion del comando")
        return

        # Obtain address
        address = text.split()[1]

        # Validate address
        if self.eth.validate(address) == False:
            self.sendMsg(chat_id, "La direccion de Ethereum proporcionada es invalida")
            return

        # Check balance
        if self.eth.balance(address) < 0.06:
            self.sendMsg(chat_id, "La direccion de Ethereum proporcionada no contiene suficientes Ether para el registro. \n\nBalance actual: " + str(self.eth.balance(address)) + " ETH\n\nPor favor asegure un balance de al menos 0.06 ETH")
            return
        # Balance completo
        self.sendMsg(chat_id, "La direccion de Ethereum contiene un balance de: " + str(self.eth.balance(address)) + " ETH")

class crowdvoucher(general):
    def __init__(self, bot, database):
        super().__init__(bot, database)
