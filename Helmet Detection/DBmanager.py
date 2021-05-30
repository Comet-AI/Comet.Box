import sqlite3

class DBmanager():
    def __init__(self, DBfile):
        # Connect DB
        self.conn = sqlite3.connect(DBfile)
        # Cursor from connection
        self.cur = self.conn.cursor()

    def InitDB(self):
        self.cur.execute("DROP TABLE if EXISTS 'WORKER';")

        self.cur.execute("CREATE TABLE IF NOT EXISTS 'WORKER' ("
                         "'ID'      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
                         "'NAME'    TEXT NOT NULL,"
                         "'RECENT'  TEXT,"
                         "'WARNINGS' INTEGER );")
        self.conn.commit()

    def InsertWorker(self, ID, name):
        ID = str(ID)

        try:
            self.cur.execute("INSERT INTO WORKER (ID, NAME, RECENT, WARNINGS) "
                             "VALUES ("+ID+", '"+name+"', CURRENT_TIMESTAMP, 0);")
            self.conn.commit()
        except sqlite3.Error as e:
            print(e.args[0])
    def DeleteAllWorker(self):
        try:
            self.cur.execute("DELETE FROM WORKER;")
            self.conn.commit()
        except sqlite3.Error as e:
            print(e.args[0])
    def DeleteWorker(self, ID):
        ID = str(ID)

        try:
            self.cur.execute("DELETE FROM WORKER WHERE ID="+ID+";")
            self.conn.commit()
        except sqlite3.Error as e:
            print(e.args[0])
    def ShowAllWorker(self):
        self.cur.execute("SELECT * FROM WORKER;")
        # Data fetch
        rows = self.cur.fetchall()
        for row in rows:
            print(row)
    def GetWorkerByID(self, ID):
        ID = str(ID)

        self.cur.execute("SELECT * FROM WORKER WHERE ID=" + ID+";")
        # Data fetch
        rows = self.cur.fetchall()
        for row in rows:
            print(row)
    def GetWorkerByName(self, name):
        try:
            self.cur.execute("SELECT * FROM WORKER WHERE NAME='"+name+"';")
            # Data fetch
            rows = self.cur.fetchall()
            for row in rows:
                print(row)
        except sqlite3.Error as e:
            print(e.args[0])
    def GetIDByName(self, name):
        try:
            self.cur.execute("SELECT ID FROM WORKER WHERE NAME='"+name+"';")
            # Data fetch
            rows = self.cur.fetchall()
            for row in rows:
                return row
        except sqlite3.Error as e:
            print(e.args[0])
    def UpdateRecent(self, ID):
        ID = str(ID)

        try:
            self.cur.execute("UPDATE WORKER SET RECENT=CURRENT_TIMESTAMP WHERE ID="+ID+";")
            self.conn.commit()
        except sqlite3.Error as e:
            print(e.args[0])
    def ResetAllRecent(self):
        try:
            self.cur.execute("UPDATE WORKER SET RECENT=CURRENT_TIMESTAMP;")
            self.conn.commit()
        except sqlite3.Error as e:
            print(e.args[0])
    def AddWarnings(self, ID):
        ID = str(ID)
        try:
            self.cur.execute("UPDATE WORKER SET RECENT=CURRENT_TIMESTAMP WHERE ID="+ID+";")
            self.cur.execute("UPDATE WORKER SET WARNINGS=WARNINGS + 1 WHERE ID="+ID+";")
            self.UpdateRecent(ID)
            self.conn.commit()
        except sqlite3.Error as e:
            print(e.args[0])
    def SetWarnings(self, ID, Warnings):
        ID = str(ID)
        Warnings = str(Warnings)

        try:
            self.cur.execute("UPDATE WORKER SET WARNINGS="+Warnings+" WHERE ID="+ID+";")
            self.conn.commit()
        except sqlite3.Error as e:
            print(e.args[0])
    def SetAllWarnings(self, Warnings):
        Warnings = str(Warnings)

        try:
            self.cur.execute("UPDATE WORKER SET WARNINGS="+Warnings+";")
            self.conn.commit()
        except sqlite3.Error as e:
            print(e.args[0])

# Main Code
if __name__ == "__main__":
    DBmanager = DBmanager("log.db")
    print("=============================<DB MANAGER COMMAND LIST>=============================")
    print("InitDB : Initialize All DB")
    print("InsertWorker ID NAME : Insert DATA::Worker(ID,NAME) to DB")
    print("DeleteAllWorker : Delete All DATA in DB")
    print("DeleteWorker ID : Delete DATA::Worker(ID) from DB")
    print("ShowAllWorker || ls : Display DB")
    print("GetWorkerByID ID : Display DATA::Worker(ID,NAME) from DB")
    print("GetWorkerByName NAME : Display DATA::Worker(ID,NAME) from DB")
    print("GetIDByName NAME : Display ID from Worker(ID,NAME) in DB")
    print("UpdateRecent ID : Update DATA::Worker(DATE) to Now")
    print("ResetAllRecent :  Update All DATA::Worker(DATE) to Now")
    print("AddWarnings ID : Add 1 Points in DATA::Worker(WARNINGS) from DB")
    print("SetWarnings ID VALUE : Initialize Value of DATA::Worker(WARNINGS) to COUNT")
    print("SetAllWarnings VALUE : Initialize Value of All DATA::Worker(WARNINGS) to COUNT")
    print("help : Show <DB MANAGER COMMAND LIST> Again")
    print("exit : Shutdown Program")
    print("===================================================================================\n")
    while True:
        command = input('COMMAND >> ')
        if command == "InitDB":
            DBmanager.InitDB()
        elif command == "InsertWorker":
            ID = input('ID >> ')
            NAME = input('NAME >> ')
            DBmanager.InsertWorker(ID, NAME)
        elif command == "DeleteAllWorker":
            DBmanager.DeleteAllWorker()
        elif command == "DeleteWorker":
            ID = input('ID >> ')
            DBmanager.DeleteWorker(ID)
        elif command == "ShowAllWorker" or command == "ls":
            DBmanager.ShowAllWorker()
        elif command == "GetWorkerByID":
            ID = input('ID >> ')
            print(DBmanager.GetWorkerByID(ID))
        elif command == "GetWorkerByName":
            NAME = input('NAME >> ')
            print(DBmanager.GetWorkerByName(NAME))
        elif command == "GetIDByName":
            NAME = input('NAME >> ')
            print(DBmanager.GetIDByName(NAME))
        elif command == "UpdateRecent":
            ID = input('ID >> ')
            DBmanager.UpdateRecent(ID)
        elif command == "ResetAllRecent":
            DBmanager.ResetAllRecent()
        elif command == "AddWarnings":
            ID = input('ID >> ')
            DBmanager.AddWarnings(ID)
        elif command == "SetWarnings":
            ID = input('ID >> ')
            VALUE = input('VALUE >> ')
            DBmanager.SetWarnings(ID,VALUE)
        elif command == "SetAllWarnings":
            VALUE = input('VALUE >> ')
            DBmanager.SetAllWarnings(VALUE)
        elif command == "help":
            print("=============================<DB MANAGER COMMAND LIST>=============================")
            print("InitDB : Initialize All DB")
            print("InsertWorker ID NAME : Insert DATA::Worker(ID,NAME) to DB")
            print("DeleteAllWorker : Delete All DATA in DB")
            print("DeleteWorker ID : Delete DATA::Worker(ID) from DB")
            print("ShowAllWorker || ls : Display DB")
            print("GetWorkerByID ID : Display DATA::Worker(ID,NAME) from DB")
            print("GetWorkerByName NAME : Display DATA::Worker(ID,NAME) from DB")
            print("GetIDByName NAME : Display ID from Worker(ID,NAME) in DB")
            print("UpdateRecent ID : Update DATA::Worker(DATE) to Now")
            print("ResetAllRecent :  Update All DATA::Worker(DATE) to Now")
            print("AddWarnings ID : Add 1 Points in DATA::Worker(WARNINGS) from DB")
            print("SetWarnings ID VALUE : Initialize Value of DATA::Worker(WARNINGS) to COUNT")
            print("SetAllWarnings VALUE : Initialize Value of All DATA::Worker(WARNINGS) to COUNT")
            print("help : Show <DB MANAGER COMMAND LIST> Again")
            print("exit : Shutdown Program")
            print("===================================================================================\n")
        elif command == "exit":
            exit()
        else:
            print('INVALID COMMAND, PLEASE ENTER COMMAND CORRECTLY')


