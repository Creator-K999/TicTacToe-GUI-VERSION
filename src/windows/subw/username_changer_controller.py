from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QPushButton, QLineEdit, QMessageBox

from processing.management.database.db_manager import DBManager
from processing.management.objects.objects_manager import ObjectsManager
from src import Log, connect_object
from src.windows import font_settings


class UserNameChanger(QDialog):

    def __init__(self):
        super().__init__()

        Log.debug("Loading UI...")
        self.__window = uic.loadUi("..\\..\\..\\Dep\\ui\\username_changer_window.ui", self)
        Log.info("UI has been loaded Successfully!")

        self.setStyleSheet(
            f"font-family: {font_settings['font']}; font-style: {font_settings['style']};"
            f"font-weight: {font_settings['weight']};")

        self.__new_username_entry: QLineEdit = self.findChild(QLineEdit, "new_username_entry")
        self.__password_entry: QLineEdit = self.findChild(QLineEdit, "password_entry")

        self.__change_username_button_1: QPushButton = self.findChild(QPushButton, "change_username_button_1")
        self.__change_username_button_2: QPushButton = self.findChild(QPushButton, "change_username_button_2")

        connect_object(self.__change_username_button_1, lambda: self.__change_username(ObjectsManager.get_object_by_name("Player1").name))
        connect_object(self.__change_username_button_2, lambda: self.__change_username(ObjectsManager.get_object_by_name("Player2").name))

    def __change_username(self, username: str):

        if username in {"Player1", "Player2"}:
            return

        password = self.__password_entry.text()

        if password == "":
            QMessageBox.critical(self, "Error", "Password isn't provided !")
            return

        if not DBManager.is_open():
            DBManager.re_connect()

        db = DBManager.db()

        encrypted_user_password = db.execute("SELECT Password From Credentials WHERE Name=?", (username,))

        # Continue from here !
