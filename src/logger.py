# PoHelper (PoHelper Telegram bot powered by Python)
# Copyright (C) 2022  drlorente97.eth <drlorente97@gmail.com>

# General Declarations
import time
import traceback

class Log():
	def __init__(self, logWindow, logLevel=4):
		self.loglevel = logLevel
		self.logbox = logBox(logWindow)
	def __get_time__(self):
		date = time.strftime('%d/%m-%H:%M> ')
		return date
	def debug(self, text):
		if self.loglevel >=4:
			self.logbox.add(self.__get_time__(), 'debug', text)
	def info(self, text):
		if self.loglevel >=3:
			self.logbox.add(self.__get_time__(), 'info', text)
	def warning(self, text):
		if self.loglevel >=2:
			self.logbox.add(self.__get_time__(), 'warning', text)
	def error(self, text):
		if self.loglevel >=1:
			self.logbox.add(self.__get_time__(), 'error', text + traceback.format_exc())

class logBox():
    def __init__(self, logwindow):
        self.logwindow = logwindow
        self.recordbuffer = []
        self.screenbuffer = []
        self.prebuffer = []
        self.do_process = True

    def add(self, date, messagetype, text):
        self.prebuffer.append([date,messagetype,text])
        if self.do_process == True:
            self.move_down()

    def move_down(self):
        if not len(self.prebuffer) == 0:
            if len(self.screenbuffer) == self.logwindow.maxlines:
                a = self.screenbuffer.pop(0)
                self.recordbuffer.append(a)
            b = self.prebuffer.pop(0)
            self.screenbuffer.append(b)
        if len(self.prebuffer) == 0:
            self.do_process = True
        self.draw()

    def move_up(self):
        if len(self.screenbuffer) == self.logwindow.maxlines:
            a = self.screenbuffer.pop()
            self.prebuffer.insert(0, a)
        if not len(self.recordbuffer) == 0:
            self.do_process = False
            b = self.recordbuffer.pop()
            self.screenbuffer.insert(0, b)
        self.draw()

    def draw(self):
        self.logwindow.clean()
        for line in self.screenbuffer:
            self.logwindow.write(line[0])
            if line[1] == 'debug':
                self.logwindow.write('DEBUG:', color=4)
            if line[1] == 'info':
                self.logwindow.write('INFO:', color=3)
            if line[1] == 'warning':
                self.logwindow.write('WARNING:', color=2)
            if line[1] == 'error':
                self.logwindow.write('ERROR:', color=1)
            self.logwindow.write(line[2] + '\n')
        if self.do_process == False:
            self.logwindow.write('Scroll to last to reenable updating in real time', color=2, y=self.logwindow.maxlines, x=0)
        else:
            self.logwindow.write(' ' * 50, color=2, y=self.logwindow.maxlines, x=0)
        self.logwindow.refresh()

    def read_key(self):
        key = self.logwindow.read()
        if key == 65:
            self.move_up()
        elif key == 66:
            self.move_down()
