# General Declarations
import sqlite3
import time

class dbEngine():
    def __init__(self, log):
        """
        SQLite Database handler
        Usage:
        Use execute method for execute sql sentences on the database and get the results
        """
        self.connection = sqlite3.Connection('pytelebot.db')
        self.cursor = self.connection.cursor()
        if self.testDB() == False:
            log.warning("Database not found, REBUILDING from default")
            self.rebuildDatabase()
            self.initializeDatabase()

    def execute(self, sentence):
        """
        Execute sql sequences on database and return result
        """
        self.cursor.execute(sentence)
        try:
            self.connection.commit()
        except:
            None
        return self.cursor.fetchall()

    def testDB(self):
        """
        Test if existing DB is empty
        """
        tables = self.execute('SELECT name FROM sqlite_master WHERE type = "table";')
        if len(tables) == 0:
            return False
        else:
            return True

    def readDefaultDB(self):
        """
        Read default database from botDB.sql file
        """
        file = open('botDB.sql')
        defaultdb = file.read()
        file.close()
        return defaultdb

    def rebuildDatabase(self):
        """
        Rebuild database from default preset
        """
        defaultdb = self.readDefaultDB()
        self.connection.executescript(defaultdb)
        self.connection.commit()

    def initializeDatabase(self):
        """
        Initialize bot parameters in database
        TODO: Get bot parameters
        """
        self.execute('INSERT INTO "ServerInfo" ("Initialized") VALUES ("True");')
