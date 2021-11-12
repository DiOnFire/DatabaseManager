from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

from screen.app.CSVManagerWindow import CSVManagerWindow
from screen.app.SQLManagerWindow import SQLManagerWindow
from screen.root.CreateCSVTable import CreateCSVTable
from screen.root.OpenCSVManagerWindow import OpenCSVManagerWindow
from screen.root.OpenSQLManagerWindow import OpenSQLManagerWindow


class MainMenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("layout/MainMenu.ui", self)
        self.init_handlers()
        self.initUI()

    def init_handlers(self):
        self.openSqlDatabaseButton.clicked.connect(self.open_sql)
        self.openCvsDatabaseButton.clicked.connect(self.open_csv)
        self.createCvsDatabaseButton.clicked.connect(self.init_Cvs_Creator_window)
        self.exitButton.clicked.connect(self.init_app_exit)

    def initUI(self):
        self.setFixedSize(484, 576)
        self.setWindowTitle("Database Manager - главное меню")

    def open_csv(self):
        OpenCSVManagerWindow(self)

    def open_sql(self):
        OpenSQLManagerWindow(self)

    def init_Sql_Manager_window(self, dir=""):
        self.close()
        self.sql_window = SQLManagerWindow(dir)
        self.sql_window.show()

    def init_Cvs_Manager_window(self, dir=""):
        self.close()
        self.csv_window = CSVManagerWindow(dir)
        self.csv_window.show()

    def init_Cvs_Creator_window(self):
        window = CreateCSVTable(self)

    def init_Tvs_Creator_window(self):
        pass

    def init_app_exit(self):
        self.close()
