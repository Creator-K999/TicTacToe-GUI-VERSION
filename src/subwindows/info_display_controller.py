from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QDialog


class InfoDisplay(QDialog):

    def __init__(self, prev_window, message):

        super().__init__()
        self.__prev_window = prev_window
        self.__window = uic.loadUi("..\\..\\Dep\\ui\\info_display_window.ui", self)

        self.__infoLabel = self.findChild(QtWidgets.QLabel, "infoLabel")
        self.__infoLabel.setText(message)

        self.accepted.connect(self.__close_and_show_prev_window)

        self.__prev_window.hide()
        self.__window.show()

#
#   PRIVATE SECTION
#

    def __close_and_show_prev_window(self):

        self.close()
        self.__prev_window.show()

#
#   OverLoaded SECTION
#
    def closeEvent(self, event):
        self.close()
        self.__prev_window.show()
