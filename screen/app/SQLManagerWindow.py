from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QTreeWidgetItem
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
        self.database = "films_db.sqlite"
        self.manager = SQLTableManager(self.database)
        try:
            self.manager.connect_to_database()
        except DatabaseNotFoundException:
            print("A")
        self.init_handlers()
        self.initUI()
        self.latest_request = ""
        self.modified = []
        self.titles = None

    def init_handlers(self):
        self.executeRequestButton.clicked.connect(self.execute_request)
        self.tableWidget.itemChanged.connect(self.item_changed_handler)
        self.saveAction.triggered.connect(self.save_table)

        self.treeWidget.setHeaderLabels(["База данных", "Тип"])

        main_tab = QTreeWidgetItem(self.treeWidget, [self.database.split(".")[0] + f" ({self.database})", "База данных"])

        for table in self.manager.get_table_list():
            tab = QTreeWidgetItem(main_tab, [table, "Таблица"])
            for id_ in self.manager.get_columns(table):
                temp = QTreeWidgetItem(tab, [id_, "Столбец"])

    def save_table(self):
        print(self.modified)
        if len(self.modified) > 0:
            for modified in self.modified:
                data = modified.split(":")
                request = f"UPDATE {data[0]} SET {data[1]}={data[2]}"
                self.manager.execute_request(request)
            self.manager.connection.commit()
            self.modified.clear()
        else:
            pass

    def initUI(self):
        global statuses
        self.setFixedSize(1162, 733)
        self.setWindowTitle("Database Manager - SQL менеджер")
        self.statusTextBrowser.append(statuses["info"] % "SQL Менеджер запущен!")

    def execute_request(self):
        global statuses
        self.latest_request = self.requestEdit.text()
        answer = self.manager.execute_request(self.requestEdit.text())
        self.tableWidget.setColumnCount(1000)
        self.tableWidget.setRowCount(0)
        if answer == InvalidSQLRequestException:
            self.statusTextBrowser.append(statuses["warning"])
        else:
            for i, row in enumerate(answer):
                self.tableWidget.setRowCount(
                    self.tableWidget.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(
                        i, j, QTableWidgetItem(str(elem)))
            self.statusTextBrowser.append(statuses["success"])

    def item_changed_handler(self, item):
        print(item)
        data = self.latest_request.split()
        table = [word for word in data if self.manager.get_table_list().count(word) > 0]
        self.modified.append(f"{table[0]}:{item.column()}:{item.text()}")
