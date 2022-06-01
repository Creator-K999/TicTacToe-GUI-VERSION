from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QMainWindow

from processing.gprocessing import main_game_processing
from processing.management.accessmgmt.objects_access_manager import MultiAccessManager
from processing.management.logger.logger_threads_manager import LoggerThreadManager


class MainGameWindow(QMainWindow):

    def __init__(self, main_window):

        super().__init__()

        self.__logger = LoggerThreadManager()

        self.__access_manager = MultiAccessManager()
        self.__access_manager.multi_access_objects["MainGameWindow"] = self

        self.__logger.debug("Storing 'MainMenu' instance in 'self.__main_window' attribute")
        self.__main_window = main_window
        self.__logger.info("'MainMenu' instance has been successfully stored in 'self.__main_window' attribute")

        self.__logger.debug("Loading The UI...")
        self.__window = uic.loadUi("..\\..\\Dep\\ui\\main_game_window.ui", self)
        self.__logger.info("UI has been loaded successfully!")

        self.__logger.debug("Looking for the 9 TicTacToe buttons (buttons are named from b1 to b9)")
        self.__buttons = {
            (button_name := f"b{i}"): self.findChild(QtWidgets.QPushButton, button_name)
            for i in range(1, 10)
        }
        self.__logger.info("Finished looking for 9 TicTacToe buttons and stored the result in self.__buttons attribute")

        self.__logger.debug("Initiating 'first_players_label_object_name' and 'second_players_label_object_name' ("
                            "Usage: finding players_labels on the UI)...")
        first_players_label_object_name = "Player1"
        second_players_label_object_name = "Player2"

        self.__logger.debug("Looking for the players labels objects...")
        self.__player_labels = {
            first_players_label_object_name: self.findChild(QtWidgets.QLabel, first_players_label_object_name),
            second_players_label_object_name: self.findChild(QtWidgets.QLabel, second_players_label_object_name)
        }
        self.__logger.info("Finished Looking for the players labels objects")

        if None in self.__buttons.values():
            self.__logger.warning("Couldn't find one or more of the 9 game buttons!")

        if None in self.__player_labels.values():
            self.__logger.warning("Couldn't find one or more players labels!")

        self.__logger.debug("Initiating a MainGameProcessing object!")
        self.__game_processor = main_game_processing.MainGameProcessing()
        self.__logger.info("Finished Initiating a MainGameProcessing object!")

        self.__logger.debug("Connecting all buttons to 'self.__button_press' method...")
        try:
            for button in self.__buttons.values():
                button.clicked.connect(self.__button_press)

        except AttributeError:
            self.__logger.exception("Probably couldn't find one or more buttons, hence we've tried to access "
                                    "'.clicked' attribute on a None object!")
        else:
            self.__logger.info("Connected all buttons to 'self.__button_press' Successfully!")

#
#   PUBLIC SECTION
#

    @property
    def game_processor(self):
        self.__logger.info("'game_processor' getter has been called!")
        return self.__game_processor

    @property
    def buttons(self):
        self.__logger.info("'buttons' getter has been called!")
        return self.__buttons

    @property
    def player_labels(self):
        self.__logger.info("'player_labels' getter has been called!")
        return self.__player_labels

#
#   PRIVATE SECTION
#
    def __button_press(self):
        self.__logger.info("A button has been pressed!")

        self.__logger.debug("getting the sender and sending it to the 'self.__game_processor.button_clicked_process'")
        result = self.__game_processor.button_clicked_process(self.sender())

        self.__logger.debug("checking the returned value from 'self.__game_processor.button_clicked_process'...")
        if result in frozenset({"Win", "Tie"}):
            self.__logger.info(f"The game is a {result}!")

            self.__logger.debug("calling 'self.__reset_game' method...")
            self.__reset_game()
            self.__logger.info("Game has been reset Successfully!")

    def __reset_game(self):

        self.__logger.info("resetting the game...")
        try:
            for button in self.__buttons.values():
                button.setText("")
                button.setDisabled(False)

        except AttributeError:
            self.__logger.exception("Error while resetting the game!")

        else:
            self.__logger.info("Finished resetting the game!")

#
#   OverLoaded SECTION
#
    def closeEvent(self, event):
        self.close()
        self.__main_window().show()
