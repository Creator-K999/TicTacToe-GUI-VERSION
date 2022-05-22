from _thread import start_new_thread
from time import sleep

from PyQt6 import uic, QtWidgets
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QDialog


class TimerWindow(QDialog):

    def __init__(self, main_instance):

        super().__init__()

        self.__sleep_period = 0

        self.__main_instance = main_instance
        self.__window = uic.loadUi("..\\..\\Dep\\ui\\timer_window.ui", self)

        self.__box_buttons = self.findChild(QtWidgets.QDialogButtonBox, "buttonBox")
        self.__timer_value_box = self.findChild(QtWidgets.QLineEdit, "timerValue")

        self.accepted.connect(self.__set_timer)

        self.show()

    def __set_timer(self):
        self.__main_instance.timer_sleep_period = float(self.__timer_value_box.text())
