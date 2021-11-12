from PyQt5.QtWidgets import QMainWindow, QFileDialog


class OpenCSVManagerWindow:
    def __init__(self, parent: QMainWindow):
        self.parent = parent
        self.db = self.build()
        self.invoke()

    def build(self):
        fname = QFileDialog.getOpenFileName(self.parent, 'Выбрать базу данных', '')[0]
        return fname

    def invoke(self):
        self.parent.init_Cvs_Manager_window(self.db)
