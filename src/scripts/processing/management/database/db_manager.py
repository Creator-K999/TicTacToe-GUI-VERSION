from os.path import expanduser
from sqlite3 import connect

from src import Log


class DBManager:
    DB_LOCATION = f"{expanduser('~')}\\TicTacToe.db"

    __db = connect(DB_LOCATION)
    __db.execute("CREATE TABLE IF NOT EXISTS Credentials(ID INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, "
                 "Password TEXT)")
    __db.execute("CREATE TABLE IF NOT EXISTS Scoreboard(ID INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, "
                 "Score TEXT)")

    @classmethod
    def log_in(cls, username, password):

        try:
            db_data = cls.__db.execute("SELECT * FROM Credentials WHERE Name = ?", (username,))
            if any(name[1] == username for name in db_data):
                Log.info("User Found!")

            else:
                Log.info(f"Registering {username} as a new User!")
                cls.__db.execute("INSERT INTO Credentials(Name, Password) VALUES(?, ?)", (username, password))
                cls.__db.commit()

        except Exception as E:
            Log.exception(E)
            return False

        return True

    @classmethod
    def re_open(cls):
        cls.__db = connect(cls.DB_LOCATION)

    @classmethod
    def close_db(cls):
        cls.__db.close()
