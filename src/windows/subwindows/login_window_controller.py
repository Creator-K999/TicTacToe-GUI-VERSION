from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QLineEdit, QMessageBox

from src import PLAYERS_INFO
from processing.management.logger.logger_threads_manager import LoggerThreadManager
from processing.management.objects.objects_manager import ObjectsManager


class LoginWindow(QDialog):

    def __init__(self, disabled_buttons):
        super().__init__()

        self.__disabled_buttons = disabled_buttons

        LoggerThreadManager.debug("Loading UI...")
        self.__window = uic.loadUi("..\\..\\..\\Dep\\ui\\login_window.ui", self)
        LoggerThreadManager.info("UI has been loaded Successfully!")

        LoggerThreadManager.debug("Looking for login objects...")
        self.__player1_fields = {
            "name": self.findChild(QLineEdit, "player1Name"),
            "password": self.findChild(QLineEdit, "player1Password")
        }
        self.__player2_fields = {
            "name": self.findChild(QLineEdit, "player2Name"),
            "password": self.findChild(QLineEdit, "player2Password")
        }

        if None in {self.__player1_fields.values(), self.__player2_fields.values()}:
            LoggerThreadManager.error("Failed to find login objects!")

        else:
            LoggerThreadManager.info("Found login objects!")

        LoggerThreadManager.info("Connecting the 'ok' button with 'self.__register_user' method")
        self.accepted.connect(self.__register_user)

    @staticmethod
    def clean_things_up():
        LoggerThreadManager.info("LoginWindow ha been closed!")
        ObjectsManager.get_object_by_name("MainMenu").show()
        ObjectsManager.delete_object("LoginWindow")

    def __register_user(self):

        # BUILD_DICT

        LoggerThreadManager.info("'self.__register_user' has been called!")

        LoggerThreadManager.info("Getting the data user provided us...")
        self.__player1_info = {
            "name": self.__player1_fields["name"].text(),
            "password": self.__player1_fields["password"].text()
        }

        self.__player2_info = {
            "name": self.__player2_fields["name"].text(),
            "password": self.__player2_fields["password"].text()
        }

        for player_1, player_2 in zip(self.__player1_info.values(), self.__player2_info.values()):
            if not all({player_1, player_2}):
                LoggerThreadManager.info("Provided wrong information!")
                QMessageBox.critical(self, "Error", "Please provide valid info!")
                self.show()
                return

        LoggerThreadManager.info(f"Storing {self.__player1_info['name']} and {self.__player2_info['name']} "
                                 f"information in PLAYERS_INFO global dictionary!")
        PLAYERS_INFO["player1"] = self.__player1_info
        PLAYERS_INFO["player2"] = self.__player2_info

        for button in self.__disabled_buttons:
            button.setDisabled(False)

        self.clean_things_up()

    def closeEvent(self, event):
        self.clean_things_up()
