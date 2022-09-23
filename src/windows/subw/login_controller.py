from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QLineEdit, QMessageBox, QPushButton, QRadioButton

from classes.player.player_class import Player
from processing.cryptography.cryptomanager import CryptoManager
from processing.management.database.db_manager import DBManager
from processing.management.logger.logger import Log
from processing.management.objects.objects_manager import ObjectsManager
from src import last_login_info, connect_object
from src.windows import CURRENT_FONT, STYLE, WEIGHT


class LoginWindow(QDialog):

    def __init__(self, disabled_buttons):
        super().__init__()

        self.__disabled_buttons = disabled_buttons

        self.__current_player = None

        Log.debug("Loading UI...")
        self.__window = uic.loadUi("..\\..\\..\\Dep\\ui\\log_in_window.ui", self)
        Log.info("UI has been loaded Successfully!")

        self.setStyleSheet(f"font-family: {CURRENT_FONT}; font-style: {STYLE}; font-weight: {WEIGHT};")

        self.__player_1_radio = self.findChild(QRadioButton, "Player1")
        self.__player_2_radio = self.findChild(QRadioButton, "Player2")

        self.__username_entry: QLineEdit = self.findChild(QLineEdit, "account_username")
        self.__password_entry: QLineEdit = self.findChild(QLineEdit, "account_password")
        self.__sign_in_button = self.findChild(QPushButton, "account_sign_in")

        self.__clear_button = self.findChild(QPushButton, "clear_button")

        connect_object(self.__player_1_radio, self.__on_select)
        connect_object(self.__player_2_radio, self.__on_select)
        connect_object(self.__sign_in_button, self.__sign_in)
        connect_object(self.__clear_button, self.__clear_entries)

    def __on_select(self):
        self.__current_player = self.sender().objectName()

    def __clear_entries(self):
        self.__username_entry.setText("")
        self.__password_entry.setText("")

    def __sign_in(self):

        current_player = self.__current_player

        username = self.__username_entry.text()
        password = self.__password_entry.text()

        self.__clear_entries()

        if current_player is None:
            QMessageBox.critical(self, "Error", "Please choose either (Player1, Player2) to log in with!")
            return

        if current_player in ObjectsManager.get_objects():
            QMessageBox.critical(self, "Error", "Player logged in!")
            return

        if "" in {username, password}:
            QMessageBox.critical(self, "Error", "Either username or password is empty!")
            return

        if not DBManager.is_open():
            DBManager.re_connect()

        db = DBManager.db()

        data = db.execute("SELECT * FROM Credentials WHERE Name = ?", (username,)).fetchall()

        if len(data):
            _encrypted_pass_as_string_list = data[0][2]

            *_encrypted_pass_as_list, key = \
                (int(x) for x in _encrypted_pass_as_string_list[1:-1].split(', '))

            if password == CryptoManager.decrypt(_encrypted_pass_as_list, key):

                ObjectsManager.create_object(Player, current_player, username, custom_name=current_player)

                QMessageBox.information(self, "Info", f"User {username} Logged-In successfully!")

                last_login_info[current_player] = username

                for button in self.__disabled_buttons:
                    button.setDisabled(False)

            else:
                QMessageBox.critical(self, "Error", "Wrong password!")

        else:
            QMessageBox.critical(self, "Error", f"Username {username} doesn't exist!")

    def closeEvent(self, event):
        Log.info("LoginWindow ha been closed!")
        DBManager.close_db()
        ObjectsManager.delete_object("LoginWindow")
        ObjectsManager.get_object_by_name("MainMenu").show()
