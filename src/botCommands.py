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
        self.active_session = telegram.props.active_session

        # Connect to web3
        self.eth = ethConnector.EthConnector(self.props.testnet)

class private(general):
    def __init__(self, bot, database):
        super().__init__(bot, database)
        self.list = {'start':self.start,
                     'cancelar':self.start,
                     'conectar': self.read_address,
                    }
        self.status = {'connect':self.connect_wallet,
                       'validate':self.validate_signature
                        }
        self.keyboard_newcommer = ReplyKeyboardMarkup(keyboard=[
						[KeyboardButton(text='Conectar Wallet')]
						], resize_keyboard=True)
        self.keyboard_cancel = ReplyKeyboardMarkup(keyboard=[
						[KeyboardButton(text='Cancelar')]
						], resize_keyboard=True)
        self.keyboard = ReplyKeyboardMarkup(keyboard=[
						[KeyboardButton(text='Still in development!')]
						], resize_keyboard=True)

    def start (self, msg):
        chat_id = str(msg.get('chat').get('id'))
        if self.__new_user__(chat_id) == True:
            self.bot.sendMsg(chat_id, "Bienvenido al bot PoHelper!\nPara conectar su address por favor presione el boton debajo", reply_markup=self.keyboard_newcommer)
        elif not self.__get_address__(chat_id):
            self.bot.sendMsg(chat_id, "Es necesario para hacer uso de las ventajas del bot que connecte su address", reply_markup=self.keyboard_newcommer)
        else:
            is_human = self.eth.validate_humanity(self.__get_address__(chat_id))
            if is_human == 'true':
                self.bot.sendMsg(chat_id, "Address conectada, humanidad validada", reply_markup=self.keyboard)
            elif is_human == 'false':
                self.bot.sendMsg(chat_id, "Address conectada, aun no validada su humanidad", reply_markup=self.keyboard)
            elif is_human == 'UnknownError':
                self.log.error('Unknown error detected on ethConnector module')
                self.bot.sendMsg(self.props.admin, "⚠Unknown error on ethConnector module: \n\n{}".format(self.tb.format_exc()))
                self.bot.sendMsg(chat_id, "Address conectada, no es posible validar humanidad, error reportado al administrador", reply_markup=self.keyboard_cancel)

    def __get_address__ (self, chat_id):
        address = self.db.execute('SELECT "address" FROM "users" WHERE "id"="{}";'.format(chat_id))[0][0]
        return address

    def __new_user__ (self, chat_id):
        cursor = self.db.execute('SELECT * FROM "users" WHERE "id"="{}";'.format(chat_id))
        if len(cursor) == 0:
            self.db.execute('INSERT INTO "users" ("id") VALUES ("{}");'.format(chat_id))
            return True
        else:
            return False

    def read_address (self, msg):
        chat_id = str(msg.get('chat').get('id'))
        self.bot.sendMsg(chat_id, "Por favor introduzca el address a continuacion:", reply_markup=self.keyboard_cancel)
        self.active_session[chat_id] = "connect"

    def connect_wallet (self, msg):
        text = str(msg.get('text'))
        chat_id = str(msg.get('chat').get('id'))
        # Validate address
        if self.eth.validate_address(text) == False:
            self.bot.sendMsg(chat_id, "La direccion de Ethereum proporcionada es invalida. Vuelva a intentarlo a continuacion", reply_markup=self.keyboard_cancel)
            return

        # Clear active session
        self.active_session.pop(chat_id, None)

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Connect Wallet', url='https://bafybeihqinm2fw4vy6q2zou3lif6ffh3lcbcl2s4xdzuu6qm2p2odnsm6y.ipfs.infura-ipfs.io/?tguid={}'.format(chat_id))]
                   ])
        self.bot.sendMsg(chat_id, "Por favor haga click en el siguiente botón para conectar tu wallet con el bot. Luego introduzca el codigo recibido a continuacion", reply_markup=keyboard)
        self.active_session[chat_id] = ['validate',text]

    def validate_signature (self, msg):
        text = str(msg.get('text'))
        chat_id = str(msg.get('chat').get('id'))
        address = self.active_session.get(chat_id)[1]
        result = self.eth.validate_signature(chat_id,text,address)
        if result == True:
            self.db.execute('UPDATE "users" SET "address" = "{}" WHERE "id"="{}";'.format(address, chat_id))
            self.active_session.pop(chat_id, None)
            self.log.info('User {} has been connected address {}'.format(chat_id, address))
            self.bot.sendMsg(chat_id, "Address validada correctamente")
        elif result == False:
            self.bot.sendMsg(chat_id, "La firma no coincide con el address proporcionada, por favor asegurese en Metamask que el address en uso es la proporcionada", reply_markup=self.keyboard_newcommer)
            self.active_session.pop(chat_id, None)
        elif result == "BadSignature":
            self.bot.sendMsg(chat_id, "La firma proporcionada es incorrecta o esta incompleta, asegurese de copiar todo el resultado obtenido de la pagina", reply_markup=self.keyboard_cancel)




class admin(private):
    def __init__(self, bot, database):
        super().__init__(bot, database)
        admin_list = {}
        admin_status_list = {}
        # Perform dict merge with private class inheritance
        self.list.update(admin_list)
        self.status.update(admin_status_list)

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
        balance = self.eth.balance(address)
        if balance < 0.06:
            self.bot.sendMsg(self.chat, "La direccion de Ethereum proporcionada no contiene suficientes Ether para el registro. \n\nBalance actual: {} ETH\n\nPor favor asegure un balance de al menos 0.06 ETH".format(str(balance)), reply_to_message_id=messageid)
            return
        # Balance completo
        self.bot.sendMsg(self.chat, "La direccion de Ethereum contiene un balance de: {} ETH".format(str(balance)), reply_to_message_id=messageid)

class crowdvoucher(general):
    def __init__(self, bot, database):
        super().__init__(bot, database)
        self.list = {}
        self.chat = self.props.crowdvoucher
