from PyQt6 import uic
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QDialog, QLineEdit, QListView, QPushButton

from processing.management.database.db_manager import DBManager
from processing.management.objects.objects_manager import ObjectsManager
from src import Log


class AccountDeletion(QDialog):

    __account_names = None

    # move the condition into re_connect method.
    if not DBManager.is_open():
        DBManager.re_connect()

    db = DBManager.db()

    data = db.execute("SELECT Name FROM Credentials").fetchall()

    if data:
        __account_names = {name[0] for name in data}

    def __init__(self):
        super().__init__()

        # loads the .UI file and sets "self" as its base object.
        Log.debug("Loading The UI...")
        self.__window = uic.loadUi("..\\..\\..\\Dep\\ui\\account_delete_window.ui", self)
        Log.info("UI has been Loaded Successfully!")

        self.__search_entry = self.findChild(QLineEdit, "search_entry")
        self.__password_entry = self.findChild(QLineEdit, "password_entry")

        self.__accounts_list_view: QListView = self.findChild(QListView, "accounts_list_view")

        self.__account_delete_button = self.findChild(QPushButton, "account_delete_button")

        model = QStandardItemModel()
        self.__accounts_list_view.setModel(model)

        for name in AccountDeletion.__account_names:
            model.appendRow(QStandardItem(name))

    def closeEvent(self, event) -> None:
        Log.debug("Closing Settings Window...")
        ObjectsManager.delete_object("AccountDeletion")

        Log.debug("Re-Displaying a hidden Settings window...")
        ObjectsManager.get_object_by_name("Settings").show()
