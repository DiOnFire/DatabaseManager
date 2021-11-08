from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox

from api.MessageBoxBuilder import MessageBoxBuilder
from api.SQLTableManager import SQLTableManager
from exception.InvalidSQLRequestException import InvalidSQLRequestException


class EditTableWindow(QWidget):
    def __init__(self, manager: SQLTableManager, database: str):
        super().__init__()
        uic.loadUi("layout/EditTable.ui", self)
        self.manager = manager
        self.database = database
        self.selected = []
        self.modified = {}
        self.latest_request = ""
        self.init_handlers()
        self.initUI()

    def initUI(self):
        self.setFixedSize(767, 574)
        self.setWindowTitle("Database Manager - изменение таблицы (SQL Менеджер)")

    def init_handlers(self):
        def init_column_combo_box():
            self.columnBox.clear()
            for column in self.manager.get_columns(self.tableBox.currentText()):
                self.columnBox.addItem(column)
        for table in self.manager.get_table_list():
            self.tableBox.addItem(table)
        self.tableBox.activated.connect(init_column_combo_box)
        self.tableWidget.itemChanged.connect(self.item_changed_handler)
        self.findButton.clicked.connect(self.execute_request)
        self.saveButton.clicked.connect(self.save_table)
        self.deleteButton.clicked.connect(self.delete_items)

    def item_changed_handler(self, item):
        self.modified[self.selected[item.column()]] = item.text()

    def save_table(self):
        if self.modified:
            que = f"UPDATE {self.tableBox.currentText()} SET\n"
            que += ", ".join([f"{key}='{self.modified.get(key)}'"
                              for key in self.modified.keys()])
            que += f"WHERE {self.columnBox.currentText()} {self.valueEdit.text()}"
            self.manager.cursor.execute(que)
            self.manager.connection.commit()
            self.modified.clear()

    def delete_items(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        valid = QMessageBox.question(
            self, '', f"Действительно удалить элементы с {self.columnBox.currentText()} " + ", ".join(ids) + "?",
            QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            self.manager.cursor.execute(f"DELETE FROM {self.tableBox.currentText()} WHERE {self.columnBox.currentText()} IN (" + ", ".join(
                '?' * len(ids)) + ")", ids)
            self.manager.connection.commit()
            self.execute_request()
        else:
            pass

    def execute_request(self):
        if self.valueEdit.text() != "":
            answer = self.manager.execute_request(f"SELECT * FROM {self.tableBox.currentText()} WHERE {self.columnBox.currentText()} {self.valueEdit.text()}")
            self.tableWidget.setColumnCount(1000)
            self.tableWidget.setRowCount(0)
            self.selected = [description[0] for description in self.manager.cursor.description]
            if answer == InvalidSQLRequestException:
                MessageBoxBuilder("Вы ввели неверное значение в поле", "Ошибка! - Database Manager", self)
            elif not answer:
                MessageBoxBuilder("По вашему запросу ничего не найдено", "Инфо - Database Manager", self)
            else:
                for i, row in enumerate(answer):
                    self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
                    for j, elem in enumerate(row):
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
            self.modified = {}
        else:
            MessageBoxBuilder("Введите запрос", "Ошибка! - Database Manager", self)
