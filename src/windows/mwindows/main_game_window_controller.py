from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QMainWindow

from scripts.processing.gprocessing.main_game_processing import MainGameProcessing
from scripts.processing.management.logger.logger_threads_manager import LoggerThreadManager
from scripts.processing.management.objects.objects_manager import ObjectsManager


class MainGameWindow(QMainWindow):

    def __init__(self, main_window):

        super().__init__()

        self.__game_processor = None

        LoggerThreadManager.debug("Storing 'MainMenu' instance in 'self.__main_window' attribute")
        self.__main_window = main_window

        LoggerThreadManager.debug("Loading The UI...")
        self.__window = uic.loadUi("..\\..\\Dep\\ui\\main_game_window.ui", self)
        LoggerThreadManager.info("UI has been loaded successfully!")

        LoggerThreadManager.debug("Looking for the 9 TicTacToe buttons (buttons are named from b1 to b9)")
        self.__buttons = {
            (button_name := f"b{i}"): self.findChild(QtWidgets.QPushButton, button_name)
            for i in range(1, 10)
        }
        LoggerThreadManager.info("Finished looking for 9 TicTacToe buttons and stored the result in self.__buttons attribute")

        LoggerThreadManager.debug("Initiating 'first_players_label_object_name' and 'second_players_label_object_name' ("
                            "Usage: finding players_labels on the UI)...")
        first_players_label_object_name = "Player1"
        second_players_label_object_name = "Player2"

        LoggerThreadManager.debug("Looking for the players labels objects...")
        self.__player_labels = {
            first_players_label_object_name: self.findChild(QtWidgets.QLabel, first_players_label_object_name),
            second_players_label_object_name: self.findChild(QtWidgets.QLabel, second_players_label_object_name)
        }
        LoggerThreadManager.info("Finished Looking for the players labels objects")

        if None in self.__buttons.values():
            LoggerThreadManager.warning("Couldn't find one or more of the 9 game buttons!")

        if None in self.__player_labels.values():
            LoggerThreadManager.warning("Couldn't find one or more players labels!")

        LoggerThreadManager.debug("Connecting all buttons to 'self.__button_press' method...")
        try:
            for button in self.__buttons.values():
                button.clicked.connect(self.__button_press)

        except AttributeError:
            LoggerThreadManager.exception("Probably couldn't find one or more buttons, hence we've tried to access "
                                    "'.clicked' attribute on a None object!")
        else:
            LoggerThreadManager.info("Connected all buttons to 'self.__button_press' Successfully!")

    def init(self):

        LoggerThreadManager.debug("Initiating a MainGameProcessing object!")
        self.__game_processor = ObjectsManager.create_object(MainGameProcessing)

#
#   PUBLIC SECTION
#

    @property
    def game_processor(self):
        LoggerThreadManager.info("'game_processor' getter has been called!")
        return self.__game_processor

    @property
    def buttons(self):
        LoggerThreadManager.info("'buttons' getter has been called!")
        return self.__buttons

    @property
    def player_labels(self):
        LoggerThreadManager.info("'player_labels' getter has been called!")
        return self.__player_labels

#
#   PRIVATE SECTION
#
    def __button_press(self):
        LoggerThreadManager.info("A button has been pressed!")

        LoggerThreadManager.debug("getting the sender and sending it to the 'self.__game_processor.button_clicked_process'")
        result = self.__game_processor.button_clicked_process(self.sender())

        LoggerThreadManager.debug("checking the returned value from 'self.__game_processor.button_clicked_process'...")
        if result in frozenset({"Win", "Tie"}):
            LoggerThreadManager.info(f"The game is a {result}!")

            LoggerThreadManager.debug("calling 'self.__reset_game' method...")
            self.__reset_game()
            LoggerThreadManager.info("Game has been reset Successfully!")

    def __reset_game(self):

        LoggerThreadManager.info("resetting the game...")
        try:
            for button in self.__buttons.values():
                button.setText("")
                button.setDisabled(False)

        except AttributeError:
            LoggerThreadManager.exception("Error while resetting the game!")

        else:
            LoggerThreadManager.info("Finished resetting the game!")

#
#   OverLoaded SECTION
#
    def closeEvent(self, event):
        LoggerThreadManager.debug("Closing MainGameWindow...")
        ObjectsManager.delete_object("Player1")
        ObjectsManager.delete_object("Player2")
        ObjectsManager.delete_object("MainGameProcessing")
        ObjectsManager.delete_object("MainGameWindow")
        self.close()

        LoggerThreadManager.debug("Creating and Re-Displaying the MainMenu")
        main_window = ObjectsManager.create_object(self.__main_window)
        main_window.show()
