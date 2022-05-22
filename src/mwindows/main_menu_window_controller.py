"""
This is the file that contains the code which controls the main menu window.
"""

# Built-ins
from logging import DEBUG, ERROR, Logger

# 3rd party Libs
from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QMainWindow

# Custom Libs
from src.mwindows.main_game_window_controller import MainGameWindow


class MainMenu(QMainWindow):
    """
    This is the MainMenu class, it controls the main menu attributes and variables.
    """

    def __init__(self):

        """
        This is the constructor of the MainMenu class, It calls the constructor of QMainWindow,
        Loads the main_menu_window.ui file, then displays it.
        """

        self.__logger = Logger("MainMenu Logger", DEBUG)

        super().__init__()  # calls the constructor of QMainWindow

        # loads the .UI file and sets "self" as its base object.
        self.__window = uic.loadUi("..\\..\\Dep\\ui\\main_menu_window.ui", self)

        # gets the object of the "Vs. Local Player" button.
        self.__local_game_button = self.findChild(QtWidgets.QPushButton, "local_game_button")

        # checks if we succeeded getting the button object
        if self.__local_game_button is None:
            self.__logger.log(ERROR, "Couldn't Find the button!")

        else:
            self.__logger.log(DEBUG, "successfully connected 'local_game_button' object with "
                                     "'self.__show_local_game_window'")
            self.__local_game_button.clicked.connect(self.__show_local_game_window)

        # displays the window
        self.__window.show()

    def __show_local_game_window(self):

        """
        This method gets called when the user presses "Vs. Local" option on main menu.
        It closes the main menu, and displays the game window.

        :return: None
        """

        # closing the main menu
        self.__window.close()

        # creating a game window objects and displaying it
        main_game_window = MainGameWindow(MainMenu)
        main_game_window.show()
