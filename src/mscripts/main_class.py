"""
This is the MainClass, it gets called by the main function.
The main menu gets called and displayed from here.
"""

# 3rd party Libs
from PyQt6.QtWidgets import QApplication

# Custom Libs
from processing.management.logger_threads_manager import LoggerThreadManager
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

        self.__logger = LoggerThreadManager()

        self.__logger.debug("Creating QApplication Object...")
        self.__app = QApplication([])  # main application
        self.__logger.info("QApplication Object has been created Successfully!")

        self.__logger.debug("Creating MainMenu object...")
        self.__window = MainMenu()  # main menu class
        self.__logger.info("MainMenu Object has been created Successfully!")

        self.__logger.debug("Calling 'self.__window.show()'...")
        self.__window.show()
        self.__logger.info("'self.__window.show()' has been called Successfully!")

#
#   PUBLIC SECTION
#
    def run(self) -> None:

        """
        This method gets called in the main function, it runs the application.
        :return: None
        """

        try:
            self.__logger.debug("Executing the Application...")
            exit_code = self.__app.exec()  # executes the application and waits for the window close.
            self.__logger.info("User Closed Window Successfully!")

            exit(exit_code)

        except SystemExit:
            self.__logger.info("Cleaning things up")

            for thread in self.__logger.threads_list:
                thread.join()

            self.__logger.info("Closing Application...")
