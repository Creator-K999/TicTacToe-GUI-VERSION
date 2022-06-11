"""
This is the file that contains the code which controls the main menu window.
"""

# 3rd party Libs
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QPushButton

# Custom Libs
from src import PLAYERS_INFO, connect_object
from src.windows.subwindows.login_window_controller import LoginWindow
from src.windows.mwindows.main_game_window_controller import MainGameWindow
from processing.management.objects.objects_manager import ObjectsManager
from processing.management.logger.logger import Log


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

        # gets the object of the "Vs. Local Player" button.
        Log.debug("Looking for 'local_game_button'")
        self.__local_game_button = self.findChild(QPushButton, "local_game_button")
        connect_object(self.__local_game_button, self.__show_local_game_window)

        if PLAYERS_INFO:
            for button in self.get_menu_buttons():
                button.setDisabled(False)

        Log.debug("Looking for 'login_button'...")
        self.__login_button = self.findChild(QPushButton, "login_button")
        connect_object(self.__login_button, self.__show_login_window)

    #
    # PUBLIC SECTION
    #
    def get_menu_buttons(self):
        return [self.__local_game_button]

    #
    #   PRIVATE SECTION
    #

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
        main_game_window = ObjectsManager.create_object(MainGameWindow)
        Log.debug("Calling MainGameWindow.init() to create a game processor!")
        main_game_window.init()

        Log.debug("Calling 'MainGameWindow.show()'...")
        main_game_window.show()
        Log.info("'MainGameWindow.show()' has been Called Successfully!")

    def __show_login_window(self):
        # closing the main menu
        Log.debug("Calling 'self.__window.hide()'...")
        self.__window.hide()
        Log.info("self.__window has been hidden Successfully!")

        # creating a game window objects and displaying it
        login_window = ObjectsManager.create_object(LoginWindow, self.get_menu_buttons())

        Log.debug("Calling 'login_window.show()'...")
        login_window.show()
        Log.info("'login_window.show()' has been Called Successfully!")

    def closeEvent(self, event):
        ...
