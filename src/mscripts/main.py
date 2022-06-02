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

# Custom Libs
from processing.management.logger.logger_threads_manager import LoggerThreadManager
from processing.management.objects.objects_manager import ObjectsManager
from src.mscripts.main_class import MainClass


def main():

    """
    This is the main function, the program starts from here!
    """

    logger = LoggerThreadManager()
    logger.info("Started The Application!")

    objects_manager = ObjectsManager()

    logger.debug("Creating MainClass Object")
    main_class = objects_manager.create_object(MainClass)

    if main_class is None:
        logger.error("Failed to Create MainClass object")
        return 1

    main_class.run()
    logger.info("Application Closed!")
    objects_manager.delete_object("MainClass")


if __name__ == "__main__":
    main()
