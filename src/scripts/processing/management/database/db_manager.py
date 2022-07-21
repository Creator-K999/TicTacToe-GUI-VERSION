from os.path import expanduser
from sqlite3 import connect

from processing.cryptography.cryptomanager import CryptoManager
from src import Log


class DBManager:
    DB_LOCATION = f"{expanduser('~')}\\TicTacToe.db"

    opened = True
    __db = connect(DB_LOCATION)
    __db.execute("CREATE TABLE IF NOT EXISTS Credentials(ID INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, "
                 "Password TEXT)")
    __db.execute("CREATE TABLE IF NOT EXISTS Scoreboard(ID INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, "
                 "Score TEXT)")

    @classmethod
    def log_in(cls, username, password):

        try:
            db_data = cls.__db.execute("SELECT * FROM Credentials WHERE Name = ? OR Password = ?", (username, password))

            users = set()
            passwords = set()

            for _, user, _pass in db_data:
                users.add(user)
                *_pass, key = [int(x.replace('[', '').replace(']', '')) for x in _pass.split(', ')]
                passwords.add(CryptoManager.decrypt(_pass, key))

            if username in users:
                if password in passwords:
                    Log.info(f"{username} Found! wrote the right password!")

                else:
                    Log.info(f"{username} Found! wrote the wrong password!")
                    return "Wrong"

            else:
                Log.info(f"Registering {username} as a new User!")
                cls.__db.execute(
                    "INSERT INTO Credentials(Name, Password) VALUES(?, ?)",
                    (username, f"[{', '.join([*CryptoManager.encrypt(password), f'{CryptoManager.get_key()}'])}]")
                )
                cls.__db.commit()

        except Exception as E:
            Log.exception(E)
            return "Error"

        return "LoggedIn"

    @classmethod
    def re_connect(cls):
        cls.__db = connect(cls.DB_LOCATION)
        cls.opened = True

    @classmethod
    def close_db(cls):
        cls.opened = False
        cls.__db.close()
