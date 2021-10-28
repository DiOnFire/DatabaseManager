from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from screen.app.SQLManagerWindow import SQLManagerWindow


class MainMenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("layout/MainMenu.ui", self)
        self.init_handlers()
        self.initUI()

    def init_handlers(self):
        self.openSqlDatabaseButton.clicked.connect(self.init_Sql_Manager_window)
        self.openCvsDatabaseButton.clicked.connect(self.init_Cvs_Manager_window)
        self.openTvsDatabaseButton.clicked.connect(self.init_Tvs_Manager_window)
        self.createSqlDatabaseButton.clicked.connect(self.init_Sql_Creator_window)
        self.createCvsDatabaseButton.clicked.connect(self.init_Cvs_Creator_window)
        self.createTvsDatabaseButton.clicked.connect(self.init_Tvs_Creator_window)
        self.continueButton.clicked.connect(self.init_empty_window)
        self.exitButton.clicked.connect(self.init_app_exit)

    def initUI(self):
        self.setFixedSize(484, 576)
        self.setWindowTitle("Database Manager - главное меню")

    def init_Sql_Manager_window(self):
        self.close()
        self.sql_window = SQLManagerWindow()
        self.sql_window.show()

    def init_Cvs_Manager_window(self):
        pass

    def init_Tvs_Manager_window(self):
        pass

    def init_Sql_Creator_window(self):
        pass

    def init_Cvs_Creator_window(self):
        pass

    def init_Tvs_Creator_window(self):
        pass

    def init_app_exit(self):
        self.close()

    def init_empty_window(self):
        pass
