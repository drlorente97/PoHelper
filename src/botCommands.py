# General Declarations
import ethConnector
import time
import datetime
from telepot.namedtuple import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

class general():
    def __init__(self, telegram, database):
        '''
        Constructor
        '''
        # Set up alias
        self.db = database
        self.bot = telegram
        self.props = telegram.props
        self.log = telegram.log

        # Connect to web3
        self.eth = ethConnector.EthConnector(self.props.testnet)

class private(general):
    def __init__(self, bot, database):
        super().__init__(bot, database)
        self.list = {'start':self.connect_wallet}

    def connect_wallet (self, msg):
        chat_id = str(msg.get('chat').get('id'))
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Connect Wallet', url='https://bafybeihqinm2fw4vy6q2zou3lif6ffh3lcbcl2s4xdzuu6qm2p2odnsm6y.ipfs.infura-ipfs.io/?tguid=' + chat_id)],
                   ])
        self.bot.sendMsg(chat_id, "Por favor haga click en el siguiente botón para conectar tu wallet con el bot:", reply_markup=keyboard)


class admin(private):
    def __init__(self, bot, database):
        super().__init__(bot, database)
        self.list = {'start':self.connect_wallet}

class crowdfunding(general):
    def __init__(self, bot, database):
        super().__init__(bot, database)
        self.list = {'add':self.check_balance}
        self.chat = self.props.crowdfunding

    def check_balance(self, msg):
        text = str(msg.get('text'))
        messageid = str(msg.get('message_id'))

        if len(text.split()) == 1:
            self.bot.sendMsg(self.chat, "Por favor proporcione su direccion de Ethereum a continuacion del comando", reply_to_message_id=messageid)
            return

        # Obtain address
        address = text.split()[1]

        # Validate address
        if self.eth.validate(address) == False:
            self.bot.sendMsg(self.chat, "La direccion de Ethereum proporcionada es invalida", reply_to_message_id=messageid)
            return

        # Check balance
        if self.eth.balance(address) < 0.06:
            self.bot.sendMsg(self.chat, "La direccion de Ethereum proporcionada no contiene suficientes Ether para el registro. \n\nBalance actual: " + str(self.eth.balance(address)) + " ETH\n\nPor favor asegure un balance de al menos 0.06 ETH", reply_to_message_id=messageid)
            return
        # Balance completo
        self.bot.sendMsg(self.chat, "La direccion de Ethereum contiene un balance de: " + str(self.eth.balance(address)) + " ETH", reply_to_message_id=messageid)

class crowdvoucher(general):
    def __init__(self, bot, database):
        super().__init__(bot, database)
        self.list = {}
        self.chat = self.props.crowdvoucher
