from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from api.CSVManager import CSVManager
from api.MessageBoxBuilder import MessageBoxBuilder


class CSVManagerWindow(QMainWindow):
    def __init__(self, database: str = ""):
        super().__init__()
        uic.loadUi("layout/CSVViewer.ui", self)
        self.database = database
        self.manager = CSVManager(self.database)
        self.init_handlers()
        self.initUI()

    def initUI(self):
        self.setFixedSize(986, 623)
        self.setWindowTitle("Database Manager - CSV менеджер")

    def init_handlers(self):
        self.searchButton.clicked.connect(self.search)
        self.saveAction.triggered.connect(self.save)
        self.deleteAction.triggered.connect(self.delete)
        self.addColumnButton.clicked.connect(self.create_empty_line)
        self.delEmptyAction.triggered.connect(self.delete_empty_lines)

    def delete_empty_lines(self):
        dump = self.manager.data
        if dump:
            for line in dump:
                if line == "":
                    dump.remove(line)
        self.manager.save(dump)

    def create_empty_line(self):
        string = ""
        data = self.manager.data
        for i in range(self.spinBox.value()):
            string += ", "
        data.append(string)
        self.manager.save(data)

    def save(self):
        dump = []
        for row in range(self.tableWidget.rowCount()):
            string = ""
            for column in range(self.tableWidget.columnCount()):
                string += self.tableWidget.item(row, column).text() + ","
            string.strip(",")
            dump.append(string)
        self.manager.save(dump)

    def delete(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        if rows:
            valid = QMessageBox.question(
                self, '', f"Действительно удалить элементы?",
                QMessageBox.Yes, QMessageBox.No)
            if valid == QMessageBox.Yes:
                dump = self.manager.data
                for row in rows:
                    dump.remove(dump[row])
                self.manager.save(dump)
        else:
            MessageBoxBuilder("Выберите хотя бы один элемент", "Инфо - Database Manager", self)

    def search(self):
        answer = self.manager.find(self.lineEdit.text())
        if answer:
            self.tableWidget.setColumnCount(len(answer[0].split(",")))
            self.tableWidget.setRowCount(len(answer))
            for i, line in enumerate(answer):
                for j, data in enumerate(line.split(",")):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(data))
        else:
            MessageBoxBuilder("По вашему запросу ничего не найдено", "Инфо - Database Manager", self)
