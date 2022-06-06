from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QLineEdit

from src import PLAYERS_INFO
from processing.management.logger.logger_threads_manager import LoggerThreadManager
from processing.management.objects.objects_manager import ObjectsManager


class LoginWindow(QDialog):

    def __init__(self):
        super().__init__()

        LoggerThreadManager.debug("Loading UI...")
        self.__window = uic.loadUi("..\\..\\..\\Dep\\ui\\login_window.ui", self)
        LoggerThreadManager.info("UI has been loaded Successfully!")

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
        try:
            self.destroy()
            ObjectsManager.get_object_by_name("MainMenu").show()
            ObjectsManager.delete_object("LoginWindow")

        except Exception:
            LoggerThreadManager.exception("Error LOL!")
