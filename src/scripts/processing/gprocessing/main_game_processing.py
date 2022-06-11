from random import randint
from PyQt6.QtWidgets import QMessageBox

from src import PLAYERS_INFO
from pobject.player1_class import Player1
from pobject.player2_class import Player2
from processing.management.objects.objects_manager import ObjectsManager
from processing.management.logger.logger import Log


class MainGameProcessing:

    def __init__(self):

        self.__current_player = None

        self.__main_game_window_object = ObjectsManager.get_object_by_name("MainGameWindow")
        self.__buttons = self.__main_game_window_object.buttons
        self.__player_labels = self.__main_game_window_object.player_labels

        Log.debug("Getting players info through PLAYERS_INFO global dictionary...")
        self.__player_1_name = PLAYERS_INFO["player1"]["name"]
        self.__player_1_pass = PLAYERS_INFO["player1"]["password"]
        self.__player_2_name = PLAYERS_INFO["player2"]["name"]
        self.__player_2_pass = PLAYERS_INFO["player2"]["password"]
        Log.info("Successfully got players info through PLAYERS_INFO global dictionary")

        self.__player1 = ObjectsManager.create_object(Player1, "Player1", self.__player_1_name, self.__player_1_pass)
        self.__player2 = ObjectsManager.create_object(Player2, "Player2", self.__player_2_name, self.__player_2_pass)

    #
    #   PUBLIC SECTION
    #
    @property
    def player_1(self):
        return self.__player1

    @property
    def player_2(self):
        return self.__player2

    @property
    def current_player(self):
        return self.__current_player

    @current_player.setter
    def current_player(self, value):
        if not isinstance(value, Player1) and not isinstance(value, Player2):
            Log.error(f"Expected a Player class, got '{type(value)}'")
        elif self.__current_player is not None:
            Log.info(f"Changing color of {self.__current_player.game_name} label to black!")
            self.__player_labels[self.__current_player.game_name].setStyleSheet("color: black;")

        self.__current_player = value
        Log.info(f"Changing color of {self.__current_player.name} label to red!")
        self.__player_labels[self.__current_player.game_name].setStyleSheet("color: red;")

    def button_clicked_process(self, button):
        Log.debug(f"{button.objectName()} has been pressed, current player is "
                  f"{self.__current_player.name} playing as {self.__current_player.mark}!")
        button.setText(self.__current_player.mark)
        button.setDisabled(True)

        result = "None"
        Log.info(f"[TURN]: {self.__current_player.name}")

        if self.__win_check():
            Log.info(f"{self.__current_player.name} has Won, Displaying MessageBox to let the player "
                     "know!")
            QMessageBox.information(self.__main_game_window_object, "Win", f"{self.__current_player.name} has Won!")

            self.__current_player.increment_score()
            result = "Win"
            Log.debug("Calling 'self.__win_tie_process'...")
            self.__win_tie_process()
            Log.debug("'self.__win_tie_process' has been called Successfully!")

        elif self.__tie_check():
            Log.info("Tie game, Displaying InfoDisplay to let the player "
                     "know!")
            QMessageBox.information(self.__main_game_window_object, "Tie", "Tie Game!")

            result = "Tie"
            Log.debug("Calling 'self.__win_tie_process'...")
            self.__win_tie_process()
            Log.debug("'self.__win_tie_process' has been called Successfully!")

        else:
            self.current_player = self.__player1 if self.__current_player is self.__player2 else self.__player2

        return result

    def randomize_player(self):
        marks = ('X', 'O') if randint(0, 100) & 1 else ('O', 'X')
        Log.info(f"Marks are {marks[0]}, {marks[1]}")

        Log.info("Distributing players marks")
        self.__player1.mark = marks[0]
        self.__player2.mark = marks[1]
        self.current_player = self.__player1 if marks[0] == 'X' else self.__player2
        Log.info(f"The new current player is {self.__current_player.name}")

    #
    #   PRIVATE SECTION
    #
    def __win_tie_process(self):
        self.randomize_player()

        Log.debug("Changing Players Labels Info...")
        self.__player_labels["Player1"].setText(
            f"{self.__player1.name} ({self.__player1.mark}): {self.__player1.score}"
        )
        self.__player_labels["Player2"].setText(
            f"{self.__player2.name} ({self.__player2.mark}): {self.__player2.score}"
        )
        Log.info("Successfully Changed Players Labels Info!")

    def __win_check(self):
        Log.debug("Checking for win...")

        Log.debug("getting all the buttons text...")
        buttons = [button.text() for button in self.__buttons.values()]
        Log.debug("all the buttons text has been retrieved Successfully!")

        current_player_mark = self.__current_player.mark
        Log.debug(f"Checking if {self.__current_player.name} playing as {current_player_mark} has won!")
        return (
                (buttons[0] == buttons[1] == buttons[2] == current_player_mark) or
                (buttons[3] == buttons[4] == buttons[5] == current_player_mark) or
                (buttons[6] == buttons[7] == buttons[8] == current_player_mark) or
                (buttons[0] == buttons[3] == buttons[6] == current_player_mark) or
                (buttons[1] == buttons[4] == buttons[7] == current_player_mark) or
                (buttons[2] == buttons[5] == buttons[8] == current_player_mark) or
                (buttons[0] == buttons[4] == buttons[8] == current_player_mark) or
                (buttons[2] == buttons[4] == buttons[6] == current_player_mark)
        )

    def __tie_check(self):
        Log.info("Checking for a tie!")
        return all(not button.isEnabled() for button in self.__buttons.values())
