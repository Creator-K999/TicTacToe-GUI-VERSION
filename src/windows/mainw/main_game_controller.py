from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QMainWindow

from classes.player.player_class import Player
from processing.game.main_game_processing import MainGameProcessing
from processing.management.database.db_manager import DBManager
from processing.management.logger.logger import Log
from processing.management.objects.objects_manager import ObjectsManager
from src import connect_object, last_login_info
from src.windows import font_settings


class MainGameWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.__game_processor = None

        Log.debug("Storing 'MainMenu' class in 'self.__main_window' attribute")
        self.__main_window = ObjectsManager.get_object_by_name("MainMenu")

        Log.debug("Loading The UI...")
        self.__window = uic.loadUi("..\\..\\..\\Dep\\ui\\main_game_window.ui", self)
        Log.info("UI has been loaded successfully!")

        self.setStyleSheet(f"font-family: {font_settings['font']}; font-style: {font_settings['style']}; font-weight: {font_settings['weight']};")

        Log.debug("Looking for the 9 TicTacToe buttons (buttons are named from b1 to b9)")
        self.__buttons = {
            (button_name := f"b{i}"): self.findChild(QtWidgets.QPushButton, button_name)
            for i in range(1, 10)
        }

        for button in self.__buttons.values():
            connect_object(button, self.__button_press)

        Log.debug("Looking for the players labels objects...")
        self.__player_labels = {
            "Player1": self.findChild(QtWidgets.QLabel, "Player1"),
            "Player2": self.findChild(QtWidgets.QLabel, "Player2")
        }

        if None in self.__player_labels.values():
            Log.warning("Couldn't find one or more players labels!")

    def init(self):
        self.__game_processor = ObjectsManager.create_object(MainGameProcessing)

    #
    #   PUBLIC SECTION
    #

    @property
    def game_processor(self):
        Log.info("'game_processor' getter has been called!")
        return self.__game_processor

    @property
    def buttons(self):
        Log.info("'buttons' getter has been called!")
        return self.__buttons

    @property
    def player_labels(self):
        Log.info("'player_labels' getter has been called!")
        return self.__player_labels

    #
    #   PRIVATE SECTION
    #
    def __pick_first_player(self):
        self.__game_processor.randomize_player()

        player_1 = self.__game_processor.player_1
        player_2 = self.__game_processor.player_2
        current_player = self.__game_processor.current_player

        self.__game_processor.set_label_text(
            self.__player_labels[player_1.game_name],
            f"{player_1.name} ({player_1.mark}): {player_1.score}"
        )

        self.__game_processor.set_label_text(
            self.__player_labels[player_2.game_name],
            f"{player_2.name} ({player_2.mark}): {player_2.score}"
        )

        Log.info(f"setting {current_player.name} label color or red!")
        self.__player_labels[current_player.game_name].setStyleSheet("color: red;")

    def __button_press(self):
        Log.info("A button has been pressed!")

        Log.debug(
            "getting the sender and sending it to the 'self.__game_processor.button_clicked_process'")
        result = self.__game_processor.button_clicked_process(self.sender())

        Log.debug("checking the returned value from 'self.__game_processor.button_clicked_process'...")
        if result in frozenset({"Win", "Tie"}):
            Log.info(f"The game is a {result}!")

            Log.debug("calling 'self.__reset_game' method...")
            self.__reset_game()
            Log.info("Game has been reset Successfully!")

    def __reset_game(self):

        Log.info("resetting the game...")
        try:
            for button in self.__buttons.values():
                button.setText("")
                button.setDisabled(False)

        except AttributeError:
            Log.exception("Error while resetting the game!")

        else:
            Log.info("Finished resetting the game!")

    #
    #   OverLoaded SECTION
    #
    def showEvent(self, event):
        current_existing_objects = ObjectsManager.get_objects()

        if "Player1" not in current_existing_objects:
            ObjectsManager.create_object(Player, "Player1", last_login_info.get("Player1", "Player1"), custom_name="Player1")

        if "Player2" not in current_existing_objects:
            ObjectsManager.create_object(Player, "Player2", last_login_info.get("Player2", "Player2"), custom_name="Player2")

        self.init()

        for label in self.__player_labels.values():
            label.setStyleSheet("color: black;")

        self.__pick_first_player()

    def closeEvent(self, event):

        try:
            Log.info("Checking if DB is Opened")
            if not DBManager.is_open():
                Log.info("Reconnecting to DB")
                DBManager.re_connect()

            Log.info("Connected! Storing Players scores...")

            DBManager.update_players_scores(self.__game_processor.player_1, self.__game_processor.player_2)

            Log.debug("Closing MainGameWindow...")
            ObjectsManager.delete_object("Player2")
            ObjectsManager.delete_object("Player1")
            ObjectsManager.delete_object("MainGameProcessing")

            Log.debug("Re-Displaying a closed MainMenu window...")
            self.__main_window.show()

        except Exception as E:
            Log.exception(E)
