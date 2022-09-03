from PyQt6 import uic
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QDialog, QLineEdit, QListView, QPushButton

from processing.management.database.db_manager import DBManager
from processing.management.objects.objects_manager import ObjectsManager
from src import Log


class AccountDeletion(QDialog):

    def __init__(self):
        super().__init__()

        # loads the .UI file and sets "self" as its base object.
        Log.debug("Loading The UI...")
        self.__window = uic.loadUi("..\\..\\..\\Dep\\ui\\account_delete_window.ui", self)
        Log.info("UI has been Loaded Successfully!")

        self.__search_entry = self.findChild(QLineEdit, "search_entry")
        self.__password_entry = self.findChild(QLineEdit, "password_entry")

        self.__accounts_list_view: QListView = self.findChild(QListView, "accounts_list_view")

        self.__accounts_list_view.clicked.connect(self.__item_selected)

        self.__account_delete_button = self.findChild(QPushButton, "account_delete_button")

        # move the condition into re_connect method.
        if not DBManager.is_open():
            DBManager.re_connect()

        self.__db = DBManager.db()
        data = self.__db.execute("SELECT Name FROM Credentials").fetchall()
        self.__accounts_names = {name[0] for name in data}

        model = QStandardItemModel()
        self.__accounts_list_view.setModel(model)

        for name in self.__accounts_names:
            model.appendRow(QStandardItem(name))

        self.__old_key_press_event = self.__search_entry.keyPressEvent
        self.__search_entry.keyPressEvent = self.__on_search

    def __item_selected(self):
        print(self.__accounts_list_view.model().data(self.__accounts_list_view.currentIndex()))

    def __on_search(self, event):
        self.__old_key_press_event(event)
        text = self.__search_entry.text().lower()

        model = QStandardItemModel()
        self.__accounts_list_view.setModel(model)

        for name in self.__accounts_names:
            if name.lower().startswith(text):
                model.appendRow(QStandardItem(name))

    def closeEvent(self, event) -> None:
        Log.debug("Closing Settings Window...")
        ObjectsManager.delete_object("AccountDeletion")

        Log.debug("Re-Displaying a hidden Settings window...")
        ObjectsManager.get_object_by_name("Settings").show()
