# General Declarations
import signal
import sys
import threading

class signalHandler():
    def __init__(self,log):
        """
        Create threading event start_shutdown
        It will be triggered when receive escape signal
        This class need a log handler with the following sintax log.info('Example error')
        """
        self.log = log
        self.start_shutdown = threading.Event()
        for sig in (signal.Signals.SIGINT, signal.Signals.SIGABRT, signal.Signals.SIGTERM):
            signal.signal(sig, self.__shutdown__)

    def __shutdown__(self, sig, frame):
        """
        This method will be called when escape signal is triggered
        """
        self.log.warning('Received escape signal, starting shutdown...')
        self.start_shutdown.set()
