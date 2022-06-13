from sqlite3 import connect


class DBManager:
    DB_LOCATION = "C:\\TicTacToe.db"

    def __init__(self):

        self.__db = connect(DBManager.DB_LOCATION)
