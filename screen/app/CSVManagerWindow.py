from PyQt5.QtWidgets import QMainWindow
from api.CSVManager import CSVManager


class CSVManagerWindow(QMainWindow):
    def __init__(self, database: str):
        super().__init__()
        self.database = database
        self.manager = CSVManager(self.database)
