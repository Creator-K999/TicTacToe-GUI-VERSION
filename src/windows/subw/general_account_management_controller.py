from PyQt6 import uic
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QDialog, QLineEdit, QListView, QPushButton, QMessageBox

from processing.cryptography.cryptomanager import CryptoManager
from processing.management.database.db_manager import DBManager
from processing.management.objects.objects_manager import ObjectsManager
from src import Log, connect_object


class AccountDeletion(QDialog):

    def __init__(self):
        super().__init__()

        # loads the .UI file and sets "self" as its base object.
        Log.debug("Loading The UI...")
        self.__window = uic.loadUi("..\\..\\..\\Dep\\ui\\general_account_management_window.ui", self)
        Log.info("UI has been Loaded Successfully!")

        self.__search_entry = self.findChild(QLineEdit, "search_entry")
        self.__password_entry = self.findChild(QLineEdit, "password_entry")

        self.__accounts_list_view: QListView = self.findChild(QListView, "accounts_list_view")

        self.__account_delete_button = self.findChild(QPushButton, "account_delete_button")
        self.__score_reset_button = self.findChild(QPushButton, "reset_score_button")

        connect_object(self.__account_delete_button, self.__on_delete)
        connect_object(self.__score_reset_button, self.__on_reset)

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

    def __refresh(self):

        self.__accounts_names.remove(self.__accounts_list_view.model().data(self.__accounts_list_view.currentIndex()))
        self.__accounts_list_view.model().removeRow(self.__accounts_list_view.currentIndex().row())
        self.__password_entry.setText("")

    def __on_search(self, event):
        self.__old_key_press_event(event)
        text = self.__search_entry.text().lower()

        model = QStandardItemModel()
        self.__accounts_list_view.setModel(model)

        for name in self.__accounts_names:
            if name.lower().startswith(text):
                model.appendRow(QStandardItem(name))

    def __on_delete(self):
        account_name = self.__accounts_list_view.model().data(self.__accounts_list_view.currentIndex())
        password = self.__password_entry.text()

        if account_name is None or password == "":
            QMessageBox.critical(self, "Error", "Wrong Info provided !")
            return

        encrypted_password = \
            self.__db.execute("SELECT Password FROM Credentials WHERE Name = ?", (account_name,)).fetchall()[0][0]

        *_encrypted_pass_as_list, key = \
            (int(x) for x in encrypted_password[1:-1].split(', '))

        if password == CryptoManager.decrypt(_encrypted_pass_as_list, key):
            self.__db.execute("DELETE FROM Credentials WHERE Name = ?", (account_name,))
            self.__db.execute("DELETE FROM Scoreboard WHERE Name = ?", (account_name,))
            self.__db.commit()

            self.__refresh()

        else:
            QMessageBox.critical(self, "Error", "Wrong password provided!")

    def __on_reset(self):
        account_name = self.__accounts_list_view.model().data(self.__accounts_list_view.currentIndex())
        password = self.__password_entry.text()

        if account_name is None or password == "":
            QMessageBox.critical(self, "Error", "Wrong Info provided !")
            return

        encrypted_password = \
            self.__db.execute("SELECT Password FROM Credentials WHERE Name = ?", (account_name,)).fetchall()[0][0]

        *_encrypted_pass_as_list, key = \
            (int(x) for x in encrypted_password[1:-1].split(', '))

        if password == CryptoManager.decrypt(_encrypted_pass_as_list, key):

            respond = QMessageBox.information(self, "Info", f"reset score for {account_name} ?",
                                              QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Cancel)

            # check bookmarks
            if respond.value:
                self.__db.execute("UPDATE Scoreboard SET Score = ? WHERE Name = ?", (0, account_name))
                self.__db.commit()

                self.__password_entry.setText("")

        else:
            QMessageBox.critical(self, "Error", "Wrong password provided!")

    def closeEvent(self, event) -> None:
        Log.debug("Closing Settings Window...")
        ObjectsManager.delete_object("AccountDeletion")

        Log.debug("Re-Displaying a hidden Settings window...")
        ObjectsManager.get_object_by_name("Settings").show()
