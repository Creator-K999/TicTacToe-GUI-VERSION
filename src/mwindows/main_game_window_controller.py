from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QMainWindow

from src.gprocessing import main_game_processing


class MainGameWindow(QMainWindow):

    def __init__(self, main_window):

        super().__init__()

        self.__main_window = main_window
        self.__window = uic.loadUi("..\\..\\Dep\\ui\\main_game_window.ui", self)

        self.__buttons = {
            (button_name := f"b{i}"): self.findChild(QtWidgets.QPushButton, button_name)
            for i in range(1, 10)
        }

        self.__player_labels = {
            "Player1": self.findChild(QtWidgets.QLabel, "Player1"),
            "Player2": self.findChild(QtWidgets.QLabel, "Player2")
        }

        if None in self.__buttons.values() or None in self.__player_labels.values():
            print("One or more button's couldn't be found!")

        self.__game_processor = main_game_processing.MainGameProcessing(self)

        for button in self.__buttons.values():
            button.clicked.connect(self.__buttonPress)

    @property
    def game_processor(self):
        return self.__game_processor

    @property
    def buttons(self):
        return self.__buttons

    @property
    def player_labels(self):
        return self.__player_labels

    def __buttonPress(self):
        result = self.__game_processor.button_clicked_process(self.sender())

        if result in {"Win", "Tie"}:
            self.__reset_game()

    def __reset_game(self):
        for button in self.__buttons.values():
            button.setText("")
            button.setDisabled(False)

    def closeEvent(self, event):
        self.__main_window().show()
