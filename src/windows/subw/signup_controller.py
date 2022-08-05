from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QPushButton, QLineEdit

from processing.management.database.db_manager import DBManager
from processing.management.objects.objects_manager import ObjectsManager
from src import Log, connect_object


class SignUp(QDialog):

    def __init__(self):
        super().__init__()

        Log.debug("Loading UI...")
        self.__window = uic.loadUi("..\\..\\..\\Dep\\ui\\sign_up_window.ui", self)
        Log.info("UI has been loaded Successfully!")

        self.__acc_1_username_entry = self.findChild(QLineEdit, "account_1_username")
        self.__acc_1_password_entry = self.findChild(QLineEdit, "account_1_password")
        self.__acc_1_sign_up = self.findChild(QPushButton, "account_1_sign_up")

        self.__acc_2_username_entry = self.findChild(QLineEdit, "account_2_username")
        self.__acc_2_password_entry = self.findChild(QLineEdit, "account_2_password")
        self.__acc_2_sign_up = self.findChild(QPushButton, "account_2_sign_up")

        connect_object(self.__acc_1_sign_up,
                       lambda: self.__sign_up(self.__acc_1_username_entry.text(), self.__acc_1_password_entry.text())
                       )

        connect_object(self.__acc_2_sign_up,
                       lambda: self.__sign_up(self.__acc_2_username_entry.text(), self.__acc_2_password_entry.text())
                       )

        self.__cancel = self.findChild(QPushButton, "cancel_button")
        self.__cancel_2 = self.findChild(QPushButton, "cancel_button_2")

    def __sign_up(self, username, password):

        if not DBManager.is_open():
            DBManager.re_connect()

        data = DBManager.db().execute("SELECT * FROM Credentials WHERE Name = ?", (username,)).fetchall()

        if data:
            print("Username Exist!")

        else:
            print("Signing Up..")

    def closeEvent(self, event) -> None:
        ObjectsManager.delete_object("SignUp")
        ObjectsManager.get_object_by_name("MainMenu").show()
