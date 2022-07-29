from os.path import expanduser
from sqlite3 import connect

from classes.player.player_class import Player
from processing.cryptography.cryptomanager import CryptoManager
from src import Log


class DBManager:
    DB_LOCATION = f"{expanduser('~')}\\TicTacToe.db"

    __db = connect(DB_LOCATION)
    __opened = True

    __db.execute("CREATE TABLE IF NOT EXISTS Credentials(ID INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, "
                 "Password TEXT)")
    __db.execute("CREATE TABLE IF NOT EXISTS Scoreboard(ID INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, "
                 "Score int)")

    @classmethod
    def is_open(cls):
        return cls.__opened

    @classmethod
    def register_login(cls, username, password):

        try:
            data = cls.__db.execute("SELECT * FROM Credentials WHERE Name = ?", (username,)).fetchall()

            if data:
                _, user, _encrypted_pass_as_string_list = data[0]

                *_encrypted_pass_as_list, key = \
                    (int(x.replace('[', '').replace(']', '')) for x in _encrypted_pass_as_string_list.split(', '))

                if password == CryptoManager.decrypt(_encrypted_pass_as_list, key):
                    Log.info(f"{username} Found! wrote the right password!")

                else:
                    Log.info(f"{username} Found! wrote the wrong password!")
                    return "Wrong"

            else:
                Log.info(f"Registering {username} as a new User!")

                key = CryptoManager.get_new_key()

                cls.__db.execute(
                    "INSERT INTO Credentials(Name, Password) VALUES(?, ?)",
                    (username, f"[{', '.join(CryptoManager.encrypt(password, key))}]")
                )
                cls.__db.execute(
                    "INSERT INTO Scoreboard(Name, Score) VALUES(?, ?)",
                    (username, 0)
                )
                cls.__db.commit()

        except Exception as E:
            Log.exception(E)
            return "Error"

        return "LoggedIn"

    @classmethod
    def update_players_scores(cls, player1: Player, player2: Player):
        player_1_name = player1.name
        player_2_name = player2.name

        player_1_score = int(
                cls.__db.execute("SELECT Score FROM Scoreboard WHERE Name = ?", (player_1_name,)).fetchall()[0][0]
            ) + player1.score

        player_2_score = int(
            cls.__db.execute("SELECT Score FROM Scoreboard WHERE Name = ?", (player_2_name,)).fetchall()[0][0]
        ) + player2.score

        cls.__db.execute("UPDATE Scoreboard SET Score=? WHERE Name=?", (player_1_score, player_1_name))
        cls.__db.execute("UPDATE Scoreboard SET Score=? WHERE Name=?", (player_2_score, player_2_name))
        cls.__db.commit()

    @classmethod
    def re_connect(cls):
        cls.__db = connect(cls.DB_LOCATION)
        cls.__opened = True

    @classmethod
    def close_db(cls):
        cls.__opened = False
        cls.__db.close()
