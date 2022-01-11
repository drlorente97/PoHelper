# General Declarations
import dbEngine
import time
import botCommands
import traceback


class messageEngine():
    def __init__(self, telegram, num):
        '''
        Constructor
        '''
        # Set up alias
        self.bot = telegram
        self.queue = telegram.message_queue
        self.props = telegram.props
        self.tb = traceback
        self.log = telegram.log

        # Init Database Engine
        self.db = dbEngine.dbEngine(self.log)

        # Start logging
        self.log.info(f'Message engine thread {num} has been started')

        # Load commands
        self.privateCmd = botCommands.private(self.bot, self.db)
        self.adminCmd = botCommands.admin(self.bot, self.db)
        self.crowdfundingCmd = botCommands.crowdfunding(self.bot, self.db)
        self.crowdvoucherCmd = botCommands.crowdvoucher(self.bot, self.db)

        # Start engine!
        self.__readmessages__()

    def __readmessages__(self):
        '''
        Message processor loop
        '''
        while True:
            try:
                # Extract message from queue
                msg = self.queue.get()
                self.queue.task_done()

                # Check for shutdown message
                if msg == 'shutdown_threads':
                    self.queue.put('shutdown_threads')
                    break

                # Read message
                text = str(msg.get('text'))
                chat_id = str(msg.get('chat').get('id'))
                cmd_text = ''.join(filter(str.isalpha, text.split()[0].lower()))

                # Resolve origin
                self.bot.sendMsg(str(msg))

            except:
                self.log.error('Unknown error found, log sent to admin')
                self.bot.sendMsg(self.props.admin, "⚠Unknown error found: \n\n " + self.tb.format_exc())
