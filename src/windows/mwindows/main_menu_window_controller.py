"""
This is the file that contains the code which controls the main menu window.
"""

# 3rd party Libs
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QPushButton

# Custom Libs
from scripts.processing.management.objects.objects_manager import ObjectsManager
from windows.mwindows.main_game_window_controller import MainGameWindow
from scripts.processing.management.logger.logger_threads_manager import LoggerThreadManager
from windows.subwindows.login_window_controller import LoginWindow


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
        LoggerThreadManager.debug("Loading The UI...")
        self.__window = uic.loadUi("..\\..\\Dep\\ui\\main_menu_window.ui", self)
        LoggerThreadManager.info("UI has been Loaded Successfully!")

        # gets the object of the "Vs. Local Player" button.
        LoggerThreadManager.debug("Looking for 'local_game_button'")
        self.__local_game_button = self.findChild(QPushButton, "local_game_button")
        LoggerThreadManager.info("Finished Looking for 'local_game_button'!")

        LoggerThreadManager.debug("Looking for 'login_button'...")
        self.__login_button = self.findChild(QPushButton, "login_button")
        LoggerThreadManager.info("Finished Looking for 'login_button'...")

        # checks if we succeeded getting the button object
        if self.__local_game_button is None:
            LoggerThreadManager.warning("Couldn't Find 'local_game_button'!")

        else:
            LoggerThreadManager.info("Found 'local_game_button'")

            LoggerThreadManager.debug("Connecting 'self.__local_game_button' with 'self.__show_local_game_window'")
            try:
                self.__local_game_button.clicked.connect(self.__show_local_game_window)

            except AttributeError:
                LoggerThreadManager.exception("Couldn't connect 'self.__local_game_button' with "
                                              "'self.__show_local_game_window'")

            else:
                LoggerThreadManager.info("Successfully connected 'self.__local_game_button' with "
                                         "'self.__show_local_game_window'")

        # checks if we succeeded getting the button object
        if self.__login_button is None:
            LoggerThreadManager.warning("Couldn't Find 'login_button'!")

        else:
            LoggerThreadManager.info("Found 'login_button'")

            LoggerThreadManager.debug("Connecting 'self.__login_button' with 'self.__show_login_window'")
            try:
                self.__login_button.clicked.connect(self.__show_login_window)

            except AttributeError:
                LoggerThreadManager.exception("Couldn't connect 'self.__login_button' with "
                                              "'self.__show_login_window'")

            else:
                LoggerThreadManager.info("Successfully connected 'self.__login_button' with "
                                         "'self.__show_login_window'")

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
        LoggerThreadManager.debug("Calling 'self.__window.close()'...")
        self.__window.close()
        LoggerThreadManager.info("self.__window has been closed Successfully!")

        LoggerThreadManager.debug("Deleting MainMenu...")
        ObjectsManager.delete_object("MainMenu")
        LoggerThreadManager.info("MainMenu has been Deleted Successfully!")

        # creating a game window objects and displaying it
        LoggerThreadManager.debug("Creating 'MainGameWindow' Object...")
        main_game_window = ObjectsManager.create_object(MainGameWindow, MainMenu)
        main_game_window.init()

        LoggerThreadManager.debug("Calling 'main_game_window.show()'...")
        main_game_window.show()
        LoggerThreadManager.info("'main_game_window.show()' has been Called Successfully!")

    def __show_login_window(self):
        # closing the main menu
        LoggerThreadManager.debug("Calling 'self.__window.hide()'...")
        self.__window.hide()
        LoggerThreadManager.info("self.__window has been hidden Successfully!")

        # creating a game window objects and displaying it
        LoggerThreadManager.debug("Creating 'LoginWindow' Object...")
        login_window = ObjectsManager.create_object(LoginWindow)

        LoggerThreadManager.debug("Calling 'login_window.show()'...")
        login_window.show()
        LoggerThreadManager.info("'login_window.show()' has been Called Successfully!")

    def closeEvent(self, event):
        self.close()
