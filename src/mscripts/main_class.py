"""
This is the MainClass, it gets called by the main function.
The main menu gets called and displayed from here.
"""

# 3rd party Libs
from PyQt6.QtWidgets import QApplication

# Custom Libs
from processing.management.logger.logger_threads_manager import LoggerThreadManager
from processing.management.objects.objects_manager import ObjectsManager
from src.mwindows.main_menu_window_controller import MainMenu


class MainClass:
    """
    This is the MainClass class, It creates an application,
    initiate the main menu, then displays it.
    SystemExit error thrown on main menu close.
    """

    __instance = None

    def __init__(self):

        """
        This is the constructor of the MainClass.
        """

        self.__logger = LoggerThreadManager()
        self.__objects_manager = ObjectsManager()

        self.__logger.debug("Creating QApplication Object...")
        self.__app = self.__objects_manager.create_object(QApplication, [])  # main application

        self.__logger.debug("Creating MainMenu object...")
        self.__window = self.__objects_manager.create_object(MainMenu)  # main menu class

        self.__logger.debug("Calling 'self.__window.show()'...")
        self.__window.show()
        self.__logger.info("'self.__window.show()' has been called Successfully!")

    def __del__(self):
        self.__objects_manager.delete_object("MainMenu")
        self.__objects_manager.delete_object("QApplication")

    def __new__(cls):

        if cls.__instance is None:
            cls.__instance = super(MainClass, cls).__new__(cls)

        return cls.__instance

#
#   PUBLIC SECTION
#
    def run(self) -> int:

        """
        This method gets called in the main function, it runs the application.
        :return: None
        """
        self.__logger.debug("Executing the Application...")

        # executes the application and waits for the window close.
        exit_code = self.__app.exec()

        self.__logger.info("Cleaning things up")
        for thread in self.__logger.threads_list:
            thread.join()
        self.__logger.info("User Closed Window Successfully!")

        return exit_code
