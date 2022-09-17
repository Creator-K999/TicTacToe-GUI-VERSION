from PyQt6 import uic
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QDialog, QFontComboBox, QLineEdit, QCheckBox, QLabel, QPushButton

from processing.management.objects.objects_manager import ObjectsManager
from src import Log, connect_object
from src.windows import CURRENT_FONT


class FontChanger(QDialog):
    def __init__(self):
        super().__init__()

        # loads the .UI file and sets "self" as its base object.
        Log.debug("Loading The UI...")
        self.__window = uic.loadUi("..\\..\\..\\Dep\\ui\\font_changer_window.ui", self)
        Log.info("UI has been Loaded Successfully!")

        self.setStyleSheet(f"font-family: {CURRENT_FONT};")

        self.__font_box: QFontComboBox = self.findChild(QFontComboBox, "font_box")
        self.__font_size: QLineEdit = self.findChild(QLineEdit, "font_size_entry")
        self.__is_italic: QCheckBox = self.findChild(QCheckBox, "is_italic_check_box")
        self.__is_bold: QCheckBox = self.findChild(QCheckBox, "is_bold_check_box")

        self.__sample_label = self.findChild(QLabel, "sample_label")
        self.__x_label = self.findChild(QLabel, "x_label")
        self.__o_label = self.findChild(QLabel, "o_label")

        self.__ok_button = self.findChild(QPushButton, "ok_button")
        self.__ok_apply_button = self.findChild(QPushButton, "ok_apply_button")
        self.__upload_button = self.findChild(QPushButton, "upload_button")
        self.__save_button = self.findChild(QPushButton, "save_button")

        if not all({
            self.__font_box, self.__font_size, self.__is_italic, self.__sample_label, self.__x_label, self.__o_label,
                self.__ok_button, self.__ok_apply_button, self.__upload_button, self.__save_button}):
            Log.error("Couldn't find all objects!")

        else:
            connect_object(self.__ok_button, self.__change_sample_font)

    def __change_sample_font(self):

        try:
            font_name = self.__font_box.currentText()
            font: QFont = QFont(font_name, int(self.__font_size.text()), italic=self.__is_italic.isChecked())
            font.setBold(self.__is_bold.isChecked())

            self.__sample_label.setFont(font)
            self.__x_label.setFont(font)
            self.__o_label.setFont(font)

            self.__sample_label.setStyleSheet(f"font-family: {font_name};")
            self.__x_label.setStyleSheet(f"font-family: {font_name};")
            self.__o_label.setStyleSheet(f"font-family: {font_name};")

        except Exception as E:
            Log.error(E)

    def closeEvent(self, event) -> None:
        Log.debug("Deleting Font Changer Window...")
        ObjectsManager.delete_object("FontChanger")

        Log.debug("Re-Displaying a hidden Settings window...")
        ObjectsManager.get_object_by_name("Settings").show()
