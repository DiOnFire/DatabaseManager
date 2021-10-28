from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from api.SQLTableManager import SQLTableManager
from exception.DatabaseNotFoundException import DatabaseNotFoundException
from exception.InvalidSQLRequestException import InvalidSQLRequestException

statuses = {
    "warning": "<span style=\" color: #ff0000;\">%s</span>" % "Невозможно обработать запрос!",
    "success": "<span style=\" color: #17ff00;\">%s</span>" % "Запрос успешно обработан!",
    "info": "<span style=\" color: #00e7ff;\">%s</span>"
}


class SQLManagerWindow(QWidget):
    def __init__(self, database=None):
        super().__init__()
        uic.loadUi('layout/SqlViewer.ui', self)
        self.init_handlers()
        self.initUI()
        self.database = "films_db.sqlite"
        self.manager = SQLTableManager(self.database)
        try:
            self.manager.connect_to_database()
        except DatabaseNotFoundException:
            print("AAAAAAAAA")

    def init_handlers(self):
        self.executeRequestButton.clicked.connect(self.execute_request)
        self.stringSpinBox.valueChanged.connect(self.execute_settings)
        self.columnsSpinBox.valueChanged.connect(self.execute_settings)

    def execute_settings(self):
        self.tableWidget.setRowCount(self.stringSpinBox.value())
        self.tableWidget.setColumnCount(self.columnsSpinBox.value())

    def initUI(self):
        global statuses
        self.setFixedSize(1162, 733)
        self.stringSpinBox.setMaximum(1000000000)
        self.columnsSpinBox.setMaximum(1000000000)
        self.stringSpinBox.setMinimum(1)
        self.columnsSpinBox.setMinimum(1)
        self.setWindowTitle("Database Manager - SQL менеджер")
        self.statusTextBrowser.append(statuses["info"] % "SQL Менеджер запущен!")

    def execute_request(self):
        answer = self.manager.execute_request(self.requestEdit.text())
        if answer == InvalidSQLRequestException:
            self.statusTextBrowser.append(statuses["warning"])
        else:
            self.tableWidget.setColumnCount(self.columnsSpinBox.value())
            self.tableWidget.setRowCount(self.stringSpinBox.value())
            for i, row in enumerate(answer):
                self.tableWidget.setRowCount(
                    self.tableWidget.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(
                        i, j, QTableWidgetItem(str(elem)))
            self.statusTextBrowser.append(statuses["success"])
        self.execute_settings()
