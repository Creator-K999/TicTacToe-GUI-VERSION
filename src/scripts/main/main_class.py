"""
This is the MainClass, it gets called by the main function.
The main menu gets called and displayed from here.
"""

# 3rd party Libs
from PyQt6.QtWidgets import QApplication

# Custom Libs
from src.windows.mwindows.main_menu_window_controller import MainMenu
from processing.management.objects.objects_manager import ObjectsManager
from processing.management.logger.logger_threads_manager import Log


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

        self.__app = ObjectsManager.create_object(QApplication, [])  # main application
        self.__window = ObjectsManager.create_object(MainMenu)  # main menu class

        Log.debug("Calling 'MainMenu.show()'...")
        self.__window.show()
        Log.info("'MainMenu.show()' has been called Successfully!")

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
        Log.debug("Executing the Application...")

        # executes the application and waits for the window close.
        exit_code = self.__app.exec()
        self.__app.quit()
        Log.debug("MainMenu has been closed!")
        ObjectsManager.delete_object("MainGameWindow")
        ObjectsManager.delete_object("MainMenu")
        ObjectsManager.delete_object("QApplication")

        Log.info("User Quit App Successfully!")
        return exit_code
