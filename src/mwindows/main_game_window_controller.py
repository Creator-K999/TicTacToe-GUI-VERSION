from _thread import start_new_thread

from PyQt6 import uic, QtWidgets
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow

from src.gprocessing import main_game_processing
from src.subwindows.timer_window_controller import TimerWindow


class MainGameWindow(QMainWindow):

    __signal = pyqtSignal()

    def __init__(self, main_window):

        super().__init__()

        self.__main_window = main_window
        self.__window = uic.loadUi("..\\..\\Dep\\ui\\main_game_window.ui", self)

        self.__buttons = {
            (button_name := f"b{i}"): self.findChild(QtWidgets.QPushButton, button_name)
            for i in range(1, 10)
        }

        self.__player_labels = {
            (button_name := f"Player{i}"): self.findChild(QtWidgets.QLabel, button_name)
            for i in range(1, 3)
        }

        self.__timer_buttons = {
            "b10": self.findChild(QtWidgets.QPushButton, "b10"),
            "b11": self.findChild(QtWidgets.QPushButton, "b11")
        }

        self.__timer_label = self.findChild(QtWidgets.QLabel, "timer_label_object")

        if None in self.__buttons.values() or \
                None in self.__player_labels.values() or \
                None in self.__timer_buttons.values() or \
                None is self.__timer_label:
            print("One or more button's couldn't be found!")

        self.__game_processor = main_game_processing.MainGameProcessing(self)

        for button in self.__buttons.values():
            button.clicked.connect(self.__buttonPress)

        self.__timer_buttons["b10"].clicked.connect(lambda: start_new_thread(self.__game_processor.prepare_timer, ()))
        self.__timer_buttons["b11"].clicked.connect(lambda: TimerWindow(self.__game_processor))

    @property
    def game_processor(self):
        return self.__game_processor

    @property
    def signal(self):
        return self.__signal

    @property
    def buttons(self):
        return self.__buttons

    @property
    def player_labels(self):
        return self.__player_labels

    @property
    def timer_label(self):
        return self.__timer_label

    def __buttonPress(self):
        result = self.__game_processor.button_clicked_process(self.sender())

        if result == "Win":
            self.__reset_game()

        elif result == "Tie":
            self.__reset_game()

    def __reset_game(self):
        for button in self.__buttons.values():
            button.setText("")
            button.setDisabled(False)

    def closeEvent(self, event):
        self.__game_processor.timer_is_on = False
        self.__main_window().show()
