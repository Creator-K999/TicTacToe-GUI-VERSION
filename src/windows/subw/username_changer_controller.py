from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QPushButton, QLineEdit, QMessageBox

from processing.management.database.db_manager import DBManager
from processing.management.objects.objects_manager import ObjectsManager
from src import Log, connect_object, last_login_info
from src.windows import font_settings


class UserNameChanger(QDialog):

    def __init__(self, is_player_1):
        super().__init__()

        self.__is_player_1 = is_player_1

        Log.debug("Loading UI...")
        self.__window = uic.loadUi("..\\..\\..\\Dep\\ui\\username_changer_window.ui", self)
        Log.info("UI has been loaded Successfully!")

        try:
            self.setStyleSheet(
                f"font-family: {font_settings['font']}; font-style: {font_settings['style']};"
                f"font-weight: {font_settings['weight']};")

            self.__new_username_entry: QLineEdit = self.findChild(QLineEdit, "new_username_entry")
            self.__password_entry: QLineEdit = self.findChild(QLineEdit, "password_entry")
            self.__change_username_button: QPushButton = self.findChild(QPushButton, "change_username_button")

            if not all({self.__new_username_entry, self.__password_entry, self.__change_username_button}):
                Log.error("Couldn't manage to find all objects !")

            else:
                connect_object(self.__change_username_button, self.__change_username)

        except Exception as E:
            print(E)

    def __change_username(self):

        # stopped here !
        player_object = ObjectsManager.get_object_by_name("Player1") if self.__is_player_1\
                    else ObjectsManager.get_object_by_name("Player2")

        new_username = self.__new_username_entry.text()
        password = self.__password_entry.text()

        if player_object is None:
            username = last_login_info["Player1"]

        else:
            if password != player_object.password:
                QMessageBox.critical(self, "ERROR", "Password is invalid!")
                return

        if not DBManager.is_open():
            DBManager.re_connect()

        db = DBManager.db()
        db.execute("UPDATE Credentials SET Name=? WHERE Name=?", (new_username, player_object.username))
        db.execute("UPDATE Scoreboard SET Name=? WHERE Name=?", (new_username, player_object.username))

        db.commit()
        DBManager.close_db()

        player_object.username = new_username

        # Continue from here !

    def closeEvent(self, event) -> None:

        DBManager.close_db()
        ObjectsManager.delete_object("UserNameChanger")
        ObjectsManager.get_object_by_name("Settings").show()
