"""
This is the MainClass, it gets called by the main function.
The main menu gets called and displayed from here.
"""

# 3rd party Libs
from PyQt6.QtWidgets import QApplication

# Custom Libs
from scripts.processing.management.logger.logger_threads_manager import LoggerThreadManager
from scripts.processing.management.objects.objects_manager import ObjectsManager
from windows.mwindows.main_menu_window_controller import MainMenu


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

        LoggerThreadManager.debug("Creating QApplication Object...")
        self.__app = ObjectsManager.create_object(QApplication, [])  # main application

        LoggerThreadManager.debug("Creating MainMenu object...")
        self.__window = ObjectsManager.create_object(MainMenu)  # main menu class

        LoggerThreadManager.debug("Calling 'self.__window.show()'...")
        self.__window.show()
        LoggerThreadManager.info("'self.__window.show()' has been called Successfully!")

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
        LoggerThreadManager.debug("Executing the Application...")

        # executes the application and waits for the window close.
        exit_code = self.__app.exec()

        LoggerThreadManager.info("Cleaning things up...")

        for thread in LoggerThreadManager.get_threads_list():
            thread.join()

        self.__app.quit()
        ObjectsManager.delete_object("MainMenu")
        ObjectsManager.delete_object("QApplication")

        LoggerThreadManager.info("User Closed Window Successfully!")
        return exit_code
