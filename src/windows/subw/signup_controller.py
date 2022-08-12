from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QPushButton, QLineEdit, QMessageBox

from processing.cryptography.cryptomanager import CryptoManager
from processing.management.database.db_manager import DBManager
from processing.management.objects.objects_manager import ObjectsManager
from src import Log, connect_object


def clear_entries(entry1, entry2):
    entry1.clear()
    entry2.clear()


class SignUp(QDialog):

    def __init__(self):
        super().__init__()

        Log.debug("Loading UI...")
        self.__window = uic.loadUi("..\\..\\..\\Dep\\ui\\sign_up_window.ui", self)
        Log.info("UI has been loaded Successfully!")

        self.__username_entry = self.findChild(QLineEdit, "account_1_username")
        self.__password_entry = self.findChild(QLineEdit, "account_1_password")
        self.__sign_up_button = self.findChild(QPushButton, "account_1_sign_up")

        self.__clear_button = self.findChild(QPushButton, "clear_button")

        connect_object(self.__sign_up_button, self.__sign_up)
        connect_object(self.__clear_button, clear_entries)

    def __sign_up(self):

        username = self.__username_entry.text()
        password = self.__password_entry.text()

        if "" in {username, password}:
            return

        if not DBManager.is_open():
            DBManager.re_connect()

        db = DBManager.db()

        data = db.execute("SELECT * FROM Credentials WHERE Name = ?", (username,)).fetchall()

        if data:
            QMessageBox.critical(self, "Error", f"Username {username} already exist!")

        else:

            db.execute("INSERT INTO Credentials(Name, Password) VALUES(?, ?)",
                       (username, f"[{', '.join(CryptoManager.encrypt(password, CryptoManager.get_new_key()))}]"))
            db.execute("INSERT INTO Scoreboard(Name, Score) VALUES(?, ?)",
                       (username, 0))
            db.commit()

            QMessageBox.information(self, "Info", f"User {username} registered successfully!")

            DBManager.close_db()

    def closeEvent(self, event) -> None:
        ObjectsManager.delete_object("SignUp")
        ObjectsManager.get_object_by_name("MainMenu").show()
