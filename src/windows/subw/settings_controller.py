from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QPushButton

from processing.management.objects.objects_manager import ObjectsManager
from src import Log, connect_object
from src.windows import font_settings
from src.windows.subw.font_changer_controller import FontChanger
from src.windows.subw.general_account_management_controller import AccountDeletion


class Settings(QDialog):

    def __init__(self):
        super().__init__()

        # loads the .UI file and sets "self" as its base object.
        Log.debug("Loading The UI...")
        self.__window = uic.loadUi("..\\..\\..\\Dep\\ui\\settings_window.ui", self)
        Log.info("UI has been Loaded Successfully!")

        self.setStyleSheet(f"font-family: {font_settings['font']}; font-style: {font_settings['style']}; font-weight: {font_settings['weight']};")

        # General Tab
        self.__delete_account_button = self.findChild(QPushButton, "delete_account_button")
        self.__change_font_button = self.findChild(QPushButton, "change_font_button")
        self.__change_username_button_1: QPushButton = self.findChild(QPushButton, "change_username_button_1")
        self.__change_username_button_2: QPushButton = self.findChild(QPushButton, "change_username_button_2")

        connect_object(self.__delete_account_button, self.__show_account_deletion_window)
        connect_object(self.__change_font_button, self.__show_font_changer_window)
        connect_object(self.__change_username_button, self.__show_username_changer_window)

    def __show_account_deletion_window(self):

        # Closing the main menu
        Log.debug("Calling 'self.close()'...")
        self.hide()
        Log.info("self has been hidden Successfully!")

        # creating a account deletion window objects and displaying it
        account_deletion = ObjectsManager.create_object(AccountDeletion)

        Log.debug("Calling 'account_deletion.show()'...")
        account_deletion.show()
        Log.info("'account_deletion.show()' has been Called Successfully!")

    def __show_font_changer_window(self):
        # Closing the main menu
        Log.debug("Calling 'self.close()'...")
        self.hide()
        Log.info("self has been hidden Successfully!")

        # creating a account deletion window objects and displaying it
        font_changer = ObjectsManager.create_object(FontChanger)

        Log.debug("Calling 'font_changer.show()'...")
        font_changer.show()
        Log.info("'font_changer.show()' has been Called Successfully!")

    def __show_username_changer_window(self):
        # Closing the main menu
        Log.debug("Calling 'self.close()'...")
        self.hide()
        Log.info("self has been hidden Successfully!")

        # creating a account deletion window objects and displaying it
        username_changer = ObjectsManager.create_object(FontChanger)

        Log.debug("Calling 'username_changer.show()'...")
        username_changer.show()
        Log.info("'username_changer.show()' has been Called Successfully!")

    def closeEvent(self, event) -> None:
        Log.debug("Deleting Settings Window...")
        ObjectsManager.delete_object("Settings")

        Log.debug("Re-Displaying a hidden MainMenu window...")
        ObjectsManager.get_object_by_name("MainMenu").show()
