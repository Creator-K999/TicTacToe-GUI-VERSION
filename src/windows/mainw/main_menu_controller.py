"""
This is the file that contains the code which controls the main menu window.
"""

# 3rd party Libs
from PyQt6 import uic
from PyQt6.QtGui import QAction, QFont
from PyQt6.QtWidgets import QMainWindow, QPushButton

from processing.management.logger.logger import Log
from processing.management.objects.objects_manager import ObjectsManager
# Custom Libs
from src import connect_object
from src.windows import CURRENT_FONT, STYLE, WEIGHT
from src.windows.mainw.main_game_controller import MainGameWindow
from src.windows.subw.login_controller import LoginWindow
from src.windows.subw.settings_controller import Settings
from src.windows.subw.signup_controller import SignUp


class MainMenu(QMainWindow):
    """
    This is the MainMenu class, it controls the main menu attributes and variables.
    """

    def __init__(self):

        """
        This is the constructor of the MainMenu class, It calls the constructor of QMainWindow,
        Loads the main_menu_window.ui file, then displays it.
        """

        super().__init__()  # calls the constructor of QMainWindow

        # loads the .UI file and sets "self" as its base object.
        Log.debug("Loading The UI...")
        self.__window = uic.loadUi("..\\..\\..\\Dep\\ui\\main_menu_window.ui", self)
        Log.info("UI has been Loaded Successfully!")

        self.setStyleSheet(f"font-family: {CURRENT_FONT}; font-style: {STYLE}; font-weight: {WEIGHT};")
        ObjectsManager.get_object_by_name("QApplication").setFont(QFont(f"{CURRENT_FONT}", 13))

        # gets the object of the "Vs. Local Player" button.
        Log.debug("Looking for 'local_game_button'")
        self.__local_game_button = self.findChild(QPushButton, "local_game_button")
        connect_object(self.__local_game_button, self.__show_local_game_window)

        Log.debug("Looking for 'QAction's")
        self.__action_sign_up = self.findChild(QAction, "action_sign_up")
        self.__action_sign_in = self.findChild(QAction, "action_sign_in")
        self.__action_settings = self.findChild(QAction, "action_settings")

        connect_object(self.__action_sign_up, self.__show_sign_up_window, custom_connect="triggered")
        connect_object(self.__action_sign_in, self.__show_login_window, custom_connect="triggered")
        connect_object(self.__action_settings, self.__show_settings_window, custom_connect="triggered")

    #
    # PUBLIC SECTION
    #
    def get_menu_buttons(self):
        return [self.__local_game_button]

    #
    #   PRIVATE SECTION
    #

    def __show_settings_window(self):

        # Hiding the main menu
        Log.debug("Calling 'self.hide()'...")
        self.hide()
        Log.info("self.__window has been hidden Successfully!")

        settings_window = ObjectsManager.create_object(Settings)

        Log.debug("Calling 'sign_up.show()'...")
        settings_window.show()
        Log.info("'sign_up.show()' has been Called Successfully!")

    def __show_local_game_window(self):

        """
        This method gets called when the user presses "Vs. Local" option on main menu.
        It closes the main menu, and displays the game window.

        :return: None
        """

        # closing the main menu
        self.close()
        Log.info("MainMenu has been closed Successfully!")

        # ObjectsManager.delete_object("MainMenu")
        # creating a game window objects and displaying it

        if "MainGameWindow" not in ObjectsManager.get_objects():
            main_game_window = ObjectsManager.create_object(MainGameWindow)

        else:
            main_game_window = ObjectsManager.get_object_by_name("MainGameWindow")

        Log.debug("Calling 'MainGameWindow.show()'...")
        main_game_window.show()
        Log.info("'MainGameWindow.show()' has been Called Successfully!")

    def __show_sign_up_window(self):
        # Hiding the main menu
        Log.debug("Calling 'self.hide()'...")
        self.hide()
        Log.info("self.__window has been hidden Successfully!")

        # creating a game window objects and displaying it
        sign_up = ObjectsManager.create_object(SignUp)

        Log.debug("Calling 'sign_up.show()'...")
        sign_up.show()
        Log.info("'sign_up.show()' has been Called Successfully!")

    def __show_login_window(self):
        # Hiding the main menu
        Log.debug("Calling 'self.hide()'...")
        self.hide()
        Log.info("self.__window has been hidden Successfully!")

        # creating a game window objects and displaying it
        login_window = ObjectsManager.create_object(LoginWindow, self.get_menu_buttons())

        Log.debug("Calling 'login_window.show()'...")
        login_window.show()
        Log.info("'login_window.show()' has been Called Successfully!")

    def closeEvent(self, event):
        ...
