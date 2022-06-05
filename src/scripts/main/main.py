"""
This is a GUI version of the famous TicTacToe game.
It contains 3 modes to play.

    //
        1- Vs. Local: 1v1 local gameplay.
        2- Vs. Local Network: 1v1 on a local network gameplay.
        3- Vs. AI: Play vs undefeatable AI made by python using minimax algorithm.
    //

Made by: Ahmed Zaki Marei.
Last Modified Date: 23/05/2022
Version: 0.3
"""

# Built-ins
from sys import exit
from threading import active_count, enumerate as threads_enumerate

# Custom Libs
from scripts.processing.management.logger.logger_threads_manager import LoggerThreadManager
from scripts.processing.management.objects.objects_manager import ObjectsManager
from scripts.main.main_class import MainClass


def main():

    """
    This is the main function, the program starts from here!
    """

    logger = LoggerThreadManager()
    logger.info("Started The Application!")

    logger.debug("Creating MainClass Object")
    main_class = ObjectsManager.create_object(MainClass)

    if main_class is None:
        logger.error("Failed to Create MainClass object")
        return 1

    exit_code = main_class.run()
    logger.info("Application Closed!")
    del main_class
    ObjectsManager.delete_object("MainClass")

    ObjectsManager.destruct_objects()
    print(f"Current working threads: {active_count()}")
    for thread in threads_enumerate():
        if thread.name != "MainThread":
            print(thread.name)
            thread.join()

    exit(exit_code)


if __name__ == "__main__":
    main()
