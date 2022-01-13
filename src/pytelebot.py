# PoHelper (PoHelper Telegram bot powered by Python)
# Copyright (C) 2022  drlorente97.eth <drlorente97@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# General Declarations
import sys
from curses import wrapper
import threading
import signalHandler
import logger
import dbEngine
import gInterface
import telegramInterface
import messageEngine
import time
import restApi


# Main code
def main(screen):
	# Draw main window
	mainWindow = gInterface.intro()
	mainWindow.build()
	mainWindow.border()
	mainWindow.write('PoHelper: Telegram bot powered by Python', y=1, x=1)
	mainWindow.write('Copyright (C) 2022  drlorente97.eth <drlorente97@gmail.com>', y=2, x=1)
	mainWindow.refresh()

	# Draw log window
	logBox = gInterface.logbox()
	logBox.build()
	logBox.scroll_on()

	# Init Log Handler
	log = logger.Log(logBox)

	# Init Signal Handler
	sig = signalHandler.signalHandler(log)

	# Init Database Engine
	db = dbEngine.dbEngine(log)

	# Init Telegram Interface
	teleInt = telegramInterface.telegramInterface(log, sig.start_shutdown)

	# Define worker
	def messageEngine_worker(teleInt, log, num):
		worker = messageEngine.messageEngine(teleInt, num)

	# Define worker threads amount
	workerAmount = 1

	# Set up Message Engine Threads
	worker_threads = []
	i = 0
	while i < workerAmount:
		worker_threads.append(threading.Thread(target=messageEngine_worker, name=str(i+1), args=(teleInt, log, str(i+1))))
		i += 1

	# Start threads
	try:
		for thread in worker_threads:
			thread.start()
			time.sleep(0.1)
		while True:
            # Watchdog
			if sig.start_shutdown.is_set():
				break
			# Scroll log window
			log.logbox.read_key()
	except:
		log.error('Bot has been crash :(')
		sig.start_shutdown.set()
	finally:
		for thread in worker_threads:
			thread.join()
			name = thread.getName()
			log.warning(f"Message engine thread {name} is stoped")
		log.warning("Telebot stoped, have a nice day :)")
		# Exit curses environment

		gInterface.terminate()
		sys.exit(0)

if __name__ == '__main__':
	# Launch wrapper on main
	wrapper(main)
