from PyQt6 import uic
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QDialog, QFontComboBox, QLabel, QPushButton, QComboBox

from processing.management.objects.objects_manager import ObjectsManager
from src import Log, connect_object
from src.windows import CURRENT_FONT, STYLE, WEIGHT


class FontChanger(QDialog):
    def __init__(self):
        super().__init__()

        # loads the .UI file and sets "self" as its base object.
        Log.debug("Loading The UI...")
        self.__window = uic.loadUi("..\\..\\..\\Dep\\ui\\font_changer_window.ui", self)
        Log.info("UI has been Loaded Successfully!")

        self.setStyleSheet(f"font-family: {CURRENT_FONT}; font-style: {STYLE}; font-weight: {WEIGHT};")

        self.__font_box: QFontComboBox = self.findChild(QFontComboBox, "font_box")
        self.__style_box: QFontComboBox = self.findChild(QComboBox, "style_box")
        self.__weight_box: QFontComboBox = self.findChild(QComboBox, "weight_box")

        self.__sample_label = self.findChild(QLabel, "sample_label")
        self.__x_label = self.findChild(QLabel, "x_label")
        self.__o_label = self.findChild(QLabel, "o_label")

        self.__ok_button = self.findChild(QPushButton, "ok_button")
        self.__ok_apply_button = self.findChild(QPushButton, "ok_apply_button")
        self.__upload_button = self.findChild(QPushButton, "upload_button")
        self.__save_button = self.findChild(QPushButton, "save_button")

        if not all({
            self.__font_box, self.__style_box, self.__weight_box, self.__sample_label, self.__x_label, self.__o_label,
            self.__ok_button, self.__ok_apply_button, self.__upload_button, self.__save_button}):
            Log.error("Couldn't find all objects!")

        else:
            connect_object(self.__ok_button, self.__change_sample_font)
            connect_object(self.__ok_apply_button, self.__change_app_font)

    def __change_sample_font(self):

        try:
            style = \
                f"font-family: {self.__font_box.currentText()}; font-style: {self.__style_box.currentText()};" \
                f"font-weight: {self.__weight_box.currentText()};"

            self.__sample_label.setStyleSheet(style)
            self.__x_label.setStyleSheet(style)
            self.__o_label.setStyleSheet(style)

        except Exception as E:
            Log.error(E)

    def __change_app_font(self):

        style = \
            f"font-family: {self.__font_box.currentText()}; font-style: {self.__style_box.currentText()};" \
            f"font-weight: {self.__weight_box.currentText()};"

        try:
            for _object in ObjectsManager.get_objects().values():
                if isinstance(_object, QObject):
                    _object.setStyleSheet(style)

        except Exception as E:
            print(E)

    def closeEvent(self, event) -> None:
        Log.debug("Deleting Font Changer Window...")
        ObjectsManager.delete_object("FontChanger")

        Log.debug("Re-Displaying a hidden Settings window...")
        ObjectsManager.get_object_by_name("Settings").show()
