from random import randint

from src.pobject.player_class import Player
from src.subwindows.info_display_controller import InfoDisplay


class MainGameProcessing:

    def __init__(self, game_instance):

        marks = self.__get_marks()

        self.__game_window_instance = game_instance

        self.__buttons = game_instance.buttons
        self.__player_labels = game_instance.player_labels
        self.__player1 = Player("Player1", marks[0])
        self.__player2 = Player("Player2", marks[1])
        self.__current_player = self.__player1 if marks[0] == 'X' else self.__player2

        self.__player_labels["Player1"].setText(f"Player1 ({self.__player1.mark}): {self.__player1.score}")
        self.__player_labels["Player2"].setText(f"Player2 ({self.__player2.mark}): {self.__player2.score}")

        self.__change_object_color(self.__player_labels[self.__current_player.name], "foreground", "red")

#
#   PUBLIC SECTION
#

    @property
    def game_instance(self):
        return self.__game_window_instance

    def button_clicked_process(self, button):
        button.setText(self.__current_player.mark)
        button.setDisabled(True)

        result = "None"
        print(f"[TURN]: {self.__current_player.name}")
        current_player = self.__current_player

        if self.__win_check():
            InfoDisplay(self.__game_window_instance, f"{current_player.name} has Won!")
            current_player.increment_score()

            result = "Win"
            self.__win_tie_process()

        elif self.__tie_check():
            InfoDisplay(self.__game_window_instance, "Tie Game!")

            result = "Tie"
            self.__win_tie_process()

        else:
            self.__change_object_color(self.__player_labels[self.__current_player.name], "foreground", "black")
            self.__current_player = self.__player1 if self.__current_player is self.__player2 else self.__player2
            self.__change_object_color(self.__player_labels[self.__current_player.name], "foreground", "red")

        return result

#
#   PRIVATE SECTION
#
    @staticmethod
    def __get_marks():
        flip_coin = randint(0, 100)

        if flip_coin % 2:
            return 'X', 'O'

        return 'O', 'X'

    @staticmethod
    def __change_object_color(_object, object_part, color):
        if object_part == "foreground":
            _object.setStyleSheet(f"color: {color};")
        else:
            _object.setStyleSheet(f"background-color: {color};")

    def __win_tie_process(self):

        marks = self.__get_marks()

        self.__change_object_color(self.__player_labels[self.__current_player.name], "foreground", "black")

        self.__player1 = Player("Player1", marks[0], self.__player1.score)
        self.__player2 = Player("Player2", marks[1], self.__player2.score)
        self.__current_player = self.__player1 if marks[0] == 'X' else self.__player2

        self.__change_object_color(self.__player_labels[self.__current_player.name], "foreground", "red")

        self.__player_labels[self.__player1.name].setText(
            f"{self.__player1.name} ({self.__player1.mark}): {self.__player1.score}"
        )

        self.__player_labels[self.__player2.name].setText(
            f"{self.__player2.name} ({self.__player2.mark}): {self.__player2.score}"
        )

    def __win_check(self):
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
