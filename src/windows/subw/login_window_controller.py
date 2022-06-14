from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QLineEdit, QMessageBox

from pobject.player_class import Player
from processing.management.database.db_manager import DBManager
from processing.management.logger.logger import Log
from processing.management.objects.objects_manager import ObjectsManager


class LoginWindow(QDialog):

    def __init__(self, disabled_buttons):
        super().__init__()

        self.__disabled_buttons = disabled_buttons

        Log.debug("Loading UI...")
        self.__window = uic.loadUi("..\\..\\..\\Dep\\ui\\login_window.ui", self)
        Log.info("UI has been loaded Successfully!")

        Log.debug("Looking for login objects...")
        self.__player1_fields = {
            "name": self.findChild(QLineEdit, "player1Name"),
            "password": self.findChild(QLineEdit, "player1Password")
        }
        self.__player2_fields = {
            "name": self.findChild(QLineEdit, "player2Name"),
            "password": self.findChild(QLineEdit, "player2Password")
        }

        if None in {self.__player1_fields.values(), self.__player2_fields.values()}:
            Log.error("Failed to find login objects!")

        else:
            Log.info("Found login objects!")

        Log.info("Connecting the 'ok' button with 'self.__register_user' method")
        self.accepted.connect(self.__register_user)

    def __check_login_result(self, result):
        if result == "LoggedIn":
            return True

        elif result == "Wrong":
            QMessageBox.warning(self, "Warning", "Possible wrong password!")
            self.show()
            return False

        else:
            QMessageBox.critical(self, "Error", "Possible Error happened!\nPlease try again!")
            self.show()
            return False

    @staticmethod
    def __clean_things_up():
        Log.info("LoginWindow ha been closed!")
        DBManager.close_db()
        ObjectsManager.delete_object("LoginWindow")
        ObjectsManager.get_object_by_name("MainMenu").show()

    def __register_user(self):

        Log.info("'self.__register_user' has been called!")

        if not DBManager.opened:
            DBManager.re_connect()

        Log.info("Getting the data user provided us...")
        player_1_name = self.__player1_fields["name"].text()
        player_1_pass = self.__player1_fields["password"].text()
        player_2_name = self.__player2_fields["name"].text()
        player_2_pass = self.__player2_fields["password"].text()

        if not all({player_1_name, player_1_pass, player_2_name, player_2_pass}):
            Log.info("Provided wrong information!")
            QMessageBox.critical(self, "Error", "Please provide valid info!")
            self.show()
            return

        registered_1 = DBManager.log_in(player_1_name, player_1_pass)
        if not self.__check_login_result(registered_1):
            return None

        registered_2 = DBManager.log_in(player_2_name, player_2_pass)
        if not self.__check_login_result(registered_2):
            return None

        ObjectsManager.create_object(Player, "Player1", player_1_name, custom_name="Player1")
        ObjectsManager.create_object(Player, "Player2", player_2_name, custom_name="Player2")

        for button in self.__disabled_buttons:
            button.setDisabled(False)

        self.__clean_things_up()

    def closeEvent(self, event):
        self.__clean_things_up()
