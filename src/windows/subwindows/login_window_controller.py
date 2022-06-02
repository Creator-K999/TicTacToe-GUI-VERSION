from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QLineEdit

from src import PLAYERS_INFO
from pobject.player_class import Player
from processing.management.logger.logger_threads_manager import LoggerThreadManager
from processing.management.objects.objects_manager import ObjectsManager


class LoginWindow(QDialog):

    def __init__(self):
        super().__init__()

        self.__logger = LoggerThreadManager()
        self.__objects_manager = ObjectsManager()

        self.__logger.debug("Loading UI...")
        self.__window = uic.loadUi("..\\..\\Dep\\ui\\login_window.ui", self)
        self.__logger.info("UI has been loaded Successfully!")

        self.__player1_fields = {
            "name": self.findChild(QLineEdit, "player1Name"),
            "password": self.findChild(QLineEdit, "player1Password")
        }

        self.__player2_fields = {
            "name": self.findChild(QLineEdit, "player2Name"),
            "password": self.findChild(QLineEdit, "player2Password")
        }

        self.accepted.connect(self.__register_user)

    def __register_user(self):

        # BUILD_DICT

        self.__player1_info = {
            "name": self.__player1_fields["name"].text(),
            "password": self.__player1_fields["password"].text()
        }

        self.__player2_info = {
            "name": self.__player2_fields["name"].text(),
            "password": self.__player2_fields["password"].text()
        }

        PLAYERS_INFO["player1"] = self.__player1_info
        PLAYERS_INFO["player2"] = self.__player2_info
        self.close()

    def closeEvent(self, event):
        self.close()
        self.__objects_manager["MainMenu"].show()
        self.__objects_manager.delete_object("LoginWindow")
