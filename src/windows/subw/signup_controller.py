from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QPushButton, QLineEdit, QMessageBox

from processing.cryptography.cryptomanager import CryptoManager
from processing.management.database.db_manager import DBManager
from processing.management.objects.objects_manager import ObjectsManager
from src import Log, connect_object


class SignUp(QDialog):

    def __init__(self):
        super().__init__()

        Log.debug("Loading UI...")
        self.__window = uic.loadUi("..\\..\\..\\Dep\\ui\\sign_up_window.ui", self)
        Log.info("UI has been loaded Successfully!")

        self.__username_entry: QLineEdit = self.findChild(QLineEdit, "account_username")
        self.__password_entry: QLineEdit = self.findChild(QLineEdit, "account_password")
        self.__sign_up_button = self.findChild(QPushButton, "account_sign_up")

        self.__clear_button = self.findChild(QPushButton, "clear_button")

        connect_object(self.__sign_up_button, self.__sign_up)
        connect_object(self.__clear_button, self.__clear_entries)

    def __clear_entries(self):
        self.__username_entry.setText("")
        self.__password_entry.setText("")

    def __sign_up(self):

        username = self.__username_entry.text()
        password = self.__password_entry.text()

        self.__clear_entries()

        if "" in {username, password}:
            QMessageBox.critical(self, "Error", "Either username or password is empty!")
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

    def closeEvent(self, event) -> None:
        DBManager.close_db()
        ObjectsManager.delete_object("SignUp")
        ObjectsManager.get_object_by_name("MainMenu").show()
