# PoHelper (PoHelper Telegram bot powered by Python)
# Copyright (C) 2022  drlorente97.eth <drlorente97@gmail.com>

# General Declarations
import queue
import threading
import telepot
import time
import botProps

class telegramInterface():
    def __init__(self, log, shutdown):
        '''
        Constructor
        '''
        self.message_queue = queue.Queue()
        self.log = log
        self.props = botProps.botProps()
        self.bot = telepot.Bot(self.props.token)
        self.log.info('Telegram Inteface started sucessfuly, starting connection')
        handler_thread = threading.Thread(target=self.message_handler, name='Telegram Interface',args=(self.bot, self.message_queue, log, self.props, shutdown))
        handler_thread.start()
        restApi.run_API()

    def sendMsg(self, chat_id, text, **kwargs):
        while True:
            try:
                if self.props.connection_status == True:
                    self.bot.sendMessage(chat_id, text, **kwargs)
                    break
            except:
                self.log.error('Error sending message')

    def message_handler(self, bot, message_queue, log, props, shutdown):
        # Starting connection
        offset = 0
        time.sleep(1)
        while True:
            # Detect termination signal
            if shutdown.isSet():
                message_queue.put('shutdown_threads')
                log.warning('Telegram Interface Thread Stopped')
                break
            try:
                # Get update list (only one item in list)
                updateList = bot.getUpdates(offset, limit=1, allowed_updates='message')
                if props.connection_status == False:
                    log.info('Succesfully connected to Telegram API')
                    props.connection_status = True
                if updateList:
                    update = updateList[0]
                    # Mark update as received
                    offset = int(update['update_id']) + 1
                    # Get message from update
                    msg = update.get('message')
                    if msg:
                        message_queue.put(msg)
            except:
                log.warning("Can't connect to Telegram API, retriying in 5s...")
                props.connection_status = False
                time.sleep(5)
