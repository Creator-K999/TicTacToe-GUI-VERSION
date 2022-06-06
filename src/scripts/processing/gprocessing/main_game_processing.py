from random import randint
from PyQt6.QtWidgets import QMessageBox

from src import PLAYERS_INFO
from pobject.player1_class import Player1
from pobject.player2_class import Player2
from processing.management.objects.objects_manager import ObjectsManager
from processing.management.logger.logger_threads_manager import LoggerThreadManager


class MainGameProcessing:

    def __init__(self):

        LoggerThreadManager.debug("calling 'self.__get_marks()'...")
        marks = self.__get_marks()
        LoggerThreadManager.info(f"Marks are {marks[0]}, {marks[1]}")

        self.__main_game_window_object = ObjectsManager.get_object_by_name("MainGameWindow")
        self.__buttons = self.__main_game_window_object.buttons
        self.__player_labels = self.__main_game_window_object.player_labels

        LoggerThreadManager.debug("Getting players info through PLAYERS_INFO global dictionary...")
        self.__player_1_name = PLAYERS_INFO["player1"]["name"]
        self.__player_1_pass = PLAYERS_INFO["player1"]["password"]
        self.__player_2_name = PLAYERS_INFO["player2"]["name"]
        self.__player_2_pass = PLAYERS_INFO["player2"]["password"]
        LoggerThreadManager.info("Successfully got players info through PLAYERS_INFO global dictionary")

        self.__player1 = ObjectsManager.create_object(Player1, "Player1", self.__player_1_name, self.__player_1_pass, marks[0])
        self.__player2 = ObjectsManager.create_object(Player2, "Player2", self.__player_2_name, self.__player_2_pass, marks[1])

        self.__current_player = self.__player1 if marks[0] == 'X' else self.__player2
        LoggerThreadManager.info(f"{self.__current_player.name} will play first with mark of {self.__current_player.mark}!")

        LoggerThreadManager.debug("Changing Players Labels Info...")
        self.__player_labels["Player1"].setText(
            f"{self.__player1.name} ({self.__player1.mark}): {self.__player1.score}"
        )
        self.__player_labels["Player2"].setText(
            f"{self.__player2.name} ({self.__player2.mark}): {self.__player2.score}"
        )
        LoggerThreadManager.info("Successfully Changed Players Labels Info!")
        LoggerThreadManager.info(f"setting {self.__current_player.name} label color or red!")
        self.__player_labels[self.__current_player.game_name].setStyleSheet("color: red;")

#
#   PUBLIC SECTION
#

    @property
    def game_instance(self):
        LoggerThreadManager.info("'game_instance' getter has been called!")
        return self.__main_game_window_object

    def button_clicked_process(self, button):
        LoggerThreadManager.debug(f"{button.objectName()} has been pressed, current player is "
                                  f"{self.__current_player.name} playing as {self.__current_player.mark}!")
        button.setText(self.__current_player.mark)
        button.setDisabled(True)

        result = "None"
        LoggerThreadManager.info(f"[TURN]: {self.__current_player.name}")

        if self.__win_check():
            LoggerThreadManager.info(f"{self.__current_player.name} has Won, Displaying InfoDisplay to let the player "
                                     "know!")
            QMessageBox.information(self.__main_game_window_object, "Win", f"{self.__current_player.name} has Won!")

            self.__current_player.increment_score()
            result = "Win"
            LoggerThreadManager.debug("Calling 'self.__win_tie_process'...")
            self.__win_tie_process()
            LoggerThreadManager.debug("'self.__win_tie_process' has been called Successfully!")

        elif self.__tie_check():
            LoggerThreadManager.info("Tie game, Displaying InfoDisplay to let the player "
                                     "know!")
            QMessageBox.information(self.__main_game_window_object, "Tie", "Tie Game!")

            result = "Tie"
            LoggerThreadManager.debug("Calling 'self.__win_tie_process'...")
            self.__win_tie_process()
            LoggerThreadManager.debug("'self.__win_tie_process' has been called Successfully!")

        else:
            LoggerThreadManager.info(f"Changing color of {self.__current_player.name} label to black!")
            self.__player_labels[self.__current_player.game_name].setStyleSheet("color: black;")
            self.__current_player = self.__player1 if self.__current_player is self.__player2 else self.__player2
            LoggerThreadManager.info(f"The new current player is {self.__current_player.name}")
            self.__player_labels[self.__current_player.game_name].setStyleSheet("color: red;")
            LoggerThreadManager.info(f"Changing color of {self.__current_player.name} label to red!")

        return result

#
#   PRIVATE SECTION
#
    @staticmethod
    def __get_marks():
        return 'X', 'O' if randint(0, 100) % 2 else 'O', 'X'

    def __win_tie_process(self):

        LoggerThreadManager.debug("calling 'self.__get_marks()'...")
        marks = self.__get_marks()
        LoggerThreadManager.info(f"Marks are {marks[0]}, {marks[1]}")

        LoggerThreadManager.info("Distributing players marks")
        self.__player1.mark = marks[0]
        self.__player2.mark = marks[1]

        LoggerThreadManager.info(f"Changing color of {self.__current_player.name} label to black!")
        self.__player_labels[self.__current_player.game_name].setStyleSheet("color: black;")
        self.__current_player = self.__player1 if marks[0] == 'X' else self.__player2
        LoggerThreadManager.info(f"The new current player is {self.__current_player.name}")
        self.__player_labels[self.__current_player.game_name].setStyleSheet("color: red;")
        LoggerThreadManager.info(f"Changing color of {self.__current_player.name} label to red!")

        LoggerThreadManager.debug("Changing Players Labels Info...")
        self.__player_labels["Player1"].setText(
            f"{self.__player1.name} ({self.__player1.mark}): {self.__player1.score}"
        )
        self.__player_labels["Player2"].setText(
            f"{self.__player2.name} ({self.__player2.mark}): {self.__player2.score}"
        )
        LoggerThreadManager.info("Successfully Changed Players Labels Info!")

    def __win_check(self):
        LoggerThreadManager.debug("Checking for win...")

        LoggerThreadManager.debug("getting all the buttons text...")
        buttons = [button.text() for button in self.__buttons.values()]
        LoggerThreadManager.debug("all the buttons text has been retrieved Successfully!")

        current_player_mark = self.__current_player.mark
        LoggerThreadManager.debug(f"Checking if {self.__current_player.name} playing as {current_player_mark} has won!")
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
        LoggerThreadManager.info("Checking for a tie!")
        return all(not button.isEnabled() for button in self.__buttons.values())
