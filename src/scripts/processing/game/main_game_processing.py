from random import randint

from PyQt6.QtWidgets import QMessageBox

from classes.player.player_class import Player
from processing.management.logger.logger import Log
from processing.management.objects.objects_manager import ObjectsManager


class MainGameProcessing:

    def __init__(self):

        self.__current_player = None

        self.__main_game_window_object = ObjectsManager.get_object_by_name("MainGameWindow")
        self.__buttons = self.__main_game_window_object.buttons
        self.__player_labels = self.__main_game_window_object.player_labels

        Log.debug("Getting players info through PLAYERS_INFO global dictionary...")

        __objects = ObjectsManager.get_objects()

        if "Player1" in __objects:
            self.__player1 = ObjectsManager.get_object_by_name("Player1")
        else:
            self.__player1 = ObjectsManager.create_object(Player, "Player1", "Player1", None, custom_name="Player1")

        if "Player2" in __objects:
            self.__player2 = ObjectsManager.get_object_by_name("Player2")
        else:
            self.__player2 = ObjectsManager.create_object(Player, "Player2", "Player2", None, custom_name="Player2")

        Log.info("Successfully got players info through PLAYERS_INFO global dictionary")

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
        if not isinstance(value, Player):
            Log.error(f"Expected a Player class, got '{type(value)}'")
            return

        elif self.__current_player is not None:
            Log.info(f"Changing color of {self.__current_player.object_name} label to black!")
            self.__player_labels[self.__current_player.object_name].setStyleSheet("color: black;")

        self.__current_player = value
        Log.info(f"Changing color of {self.__current_player.username} label to red!")
        self.__player_labels[self.__current_player.object_name].setStyleSheet("color: red;")

    @staticmethod
    def set_label_text(label, text):

        if None in {label, text}:
            Log.error("Either the object or the text is 'None'!")
            return

        Log.info("set_label_text has been called!")
        Log.info(f"Changing text of label {label.objectName()} to {text}")
        label.setText(text)

    def button_clicked_process(self, button):
        Log.debug(f"{button.objectName()} has been pressed, current player is "
                  f"{self.__current_player.username} playing as {self.__current_player.mark}!")
        button.setText(self.__current_player.mark)
        button.setDisabled(True)

        result = "None"
        Log.info(f"[TURN]: {self.__current_player.username}")

        if self.__win_check():
            QMessageBox.information(self.__main_game_window_object, "Win", f"{self.__current_player.username} has Won!")

            self.__current_player.increment_score()
            result = "Win"
            Log.debug("Calling 'self.__win_tie_process'...")
            self.__win_tie_process()
            Log.debug("'self.__win_tie_process' has been called Successfully!")

        elif self.__tie_check():
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

        self.__player1.mark = marks[0]
        self.__player2.mark = marks[1]
        self.current_player = self.__player1 if marks[0] == 'X' else self.__player2
        Log.info(f"The new current player is {self.__current_player.username}")

    #
    #   PRIVATE SECTION
    #
    def __win_tie_process(self):
        self.randomize_player()

        self.set_label_text(
            self.__player_labels[self.__player1.object_name],
            f"{self.__player1.username} ({self.__player1.mark}): {self.__player1.score}"
        )

        self.set_label_text(
            self.__player_labels[self.__player2.object_name],
            f"{self.__player2.username} ({self.__player2.mark}): {self.__player2.score}"
        )

    def __win_check(self):
        Log.debug("Checking for win...")
        buttons = [button.text() for button in self.__buttons.values()]
        current_player_mark = self.__current_player.mark

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
        return all(not button.isEnabled() for button in self.__buttons.values())
