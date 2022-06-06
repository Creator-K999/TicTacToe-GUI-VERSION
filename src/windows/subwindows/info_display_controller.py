from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QDialog

from src import LoggerThreadManager


class InfoDisplay(QDialog):

    def __init__(self, prev_window, message):

        super().__init__()
        self.__prev_window = prev_window

        LoggerThreadManager.debug("Loading The UI...")
        self.__window = uic.loadUi("..\\..\\..\\Dep\\ui\\info_display_window.ui", self)
        LoggerThreadManager.info("UI has been loaded Successfully!")

        LoggerThreadManager.debug("Trying to find 'infoLabel'...")
        self.__info_label = self.findChild(QtWidgets.QLabel, "infoLabel")

        if self.__info_label is None:
            LoggerThreadManager.error(f"Couldn't find infoLabel'")

        else:
            LoggerThreadManager.info(f"Successfully found 'infoLabel', setting the message: {message}")
            self.__info_label.setText(message)

        self.accepted.connect(self.close)
        LoggerThreadManager.info("Connected ok button with 'self.close'")

        LoggerThreadManager.info("Hiding the previous window and displaying InfoDisplay window")
        self.__prev_window.hide()
        self.__window.show()

#
#   PRIVATE SECTION
#

#
#   OverLoaded SECTION
#
    def closeEvent(self, event):
        LoggerThreadManager.info("InfoDisplay window has been closed, Showing back our previous window...")
        self.__prev_window.show()
