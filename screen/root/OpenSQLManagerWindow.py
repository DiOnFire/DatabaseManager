from PyQt5.QtWidgets import QFileDialog, QMainWindow


class OpenSQLManagerWindow:
    def __init__(self, parent: QMainWindow):
        self.parent = parent
        self.db = self.build()
        self.invoke()

    def build(self):
        fname = QFileDialog.getOpenFileName(self.parent, 'Выбрать базу данных', '')[0]
        return fname

    def invoke(self):
        self.parent.init_Sql_Manager_window(self.db)
