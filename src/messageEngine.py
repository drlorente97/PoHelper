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
        self.active_session = telegram.props.active_session

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
                type = str(msg.get('chat').get('type'))
                chat_id = str(msg.get('chat').get('id'))
                cmd_text = ''.join(filter(str.isalpha, text.split()[0].lower()))

                # Elaborate answer
                if type == "supergroup":
                    if chat_id == self.props.crowdfunding:
                        if cmd_text in self.crowdfundingCmd.list:
                            self.crowdfundingCmd.list[cmd_text](msg)
                            continue
                    elif chat_id == self.props.crowdvoucher:
                        if cmd_text in self.crowdvoucherCmd.list:
                            self.crowdvoucherCmd.list[cmd_text](msg)
                            continue
                elif type == "private":
                    if chat_id == self.props.admin:
                        if cmd_text in self.adminCmd.list:
                            self.active_session.pop(chat_id, None)
                            self.adminCmd.list[cmd_text](msg)
                            continue
                        if self.active_session.get(chat_id):
                            self.adminCmd.status[self.active_session.get(chat_id).split[0]](msg)
                    else:
                        if cmd_text in self.privateCmd.list:
                            self.active_session.pop(chat_id, None)
                            self.privateCmd.list[cmd_text](msg)
                            continue
                        if self.active_session.get(chat_id):
                            self.privateCmd.status[self.active_session.get(chat_id).split[0]](msg)
                            continue
                    # Invalid command
                    self.bot.sendMsg(chat_id, "No envies comandos al bot, usa los botones")
            except:
                self.log.error('Unknown error found, log sent to admin')
                self.bot.sendMsg(self.props.admin, "⚠Unknown error found: \n\n " + self.tb.format_exc())
