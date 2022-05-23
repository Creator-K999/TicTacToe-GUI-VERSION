"""
This is the MainClass, it gets called by the main function.
The main menu gets called and displayed from here.
"""

# 3rd party Libs
from PyQt6.QtWidgets import QApplication

# Custom Libs
from src.mwindows.main_menu_window_controller import MainMenu


class MainClass:
    """
    This is the MainClass class, It creates an application, initiate the main menu, then displays it.
    SystemExit error thrown on main menu close.
    """

    def __init__(self):

        """
        This is the constructor of the MainClass.
        """

        self.__app = QApplication([])  # main application
        self.__window = MainMenu()  # main menu class

#
#   PUBLIC SECTION
#
    def run(self) -> None:

        """
        This method gets called in the main function, it runs the application.
        :return: None
        """

        try:
            exit(self.__app.exec())  # executes the application and waits for the window close.

        except SystemExit:
            print("Exiting System")
