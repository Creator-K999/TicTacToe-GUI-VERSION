"""
This is the file that contains the code which controls the main menu window.
"""

# 3rd party Libs
from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QMainWindow

# Custom Libs
from src import OBJECTS_MANAGER
from src.mwindows.main_game_window_controller import MainGameWindow
from processing.management.logger.logger_threads_manager import LoggerThreadManager


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

        self.__logger = LoggerThreadManager()

        self.__logger.debug("Adding MainMenu Object to OBJECTS_MANAGER!")
        OBJECTS_MANAGER["MainMenu"] = self

        # loads the .UI file and sets "self" as its base object.
        self.__logger.debug("Loading The UI...")
        self.__window = uic.loadUi("..\\..\\Dep\\ui\\main_menu_window.ui", self)
        self.__logger.info("UI has been Loaded Successfully!")

        # gets the object of the "Vs. Local Player" button.
        self.__logger.debug("Looking for 'local_game_button'")
        self.__local_game_button = self.findChild(QtWidgets.QPushButton, "local_game_button")
        self.__logger.info("Finished Looking for 'local_game_button'!")

        # checks if we succeeded getting the button object
        if self.__local_game_button is None:
            self.__logger.warning("Couldn't Find 'local_game_button'!")

        else:
            self.__logger.info("Found 'local_game_button'")

            self.__logger.debug("Connecting 'self.__local_game_button' with 'self.__show_local_game_window'")
            try:
                self.__local_game_button.clicked.connect(self.__show_local_game_window)

            except AttributeError:
                self.__logger.exception("Couldn't connect 'self.__local_game_button' with "
                                        "'self.__show_local_game_window'")

            else:
                self.__logger.info("Successfully connected 'self.__local_game_button' with "
                                   "'self.__show_local_game_window'")

    def show(self):

        self.__logger.debug("Trying to delete MainGameWindow from Object Life Extender!")
        try:
            del OBJECTS_MANAGER["MainGameWindow"]

        except KeyError:
            self.__logger.exception("Didn't find a MainGameWindow Object in OBJECTS_MANAGER")

        else:
            self.__logger.info("Successfully deleted MainGameWindow object from Object Life Extender!")

        super().show()

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
        self.__logger.debug("Calling 'self.__window.close()'...")
        self.__window.close()
        self.__logger.info("self.__window has been closed Successfully!")

        # creating a game window objects and displaying it
        self.__logger.debug("Creating 'MainGameWindow' Object...")
        main_game_window = MainGameWindow(MainMenu)
        self.__logger.info("'MainGameWindow' Object has been created Successfully!")

        self.__logger.info("Adding MainGameWindow to Object Life Extender!")
        OBJECTS_MANAGER["MainGameWindow"] = main_game_window

        self.__logger.debug("Calling 'main_game_window.show()'...")
        main_game_window.show()
        self.__logger.info("'main_game_window.show()' has been Called Successfully!")
