from PyQt5.QtWidgets import QFileDialog, QMainWindow
from screen.app.CSVManagerWindow import CSVManagerWindow


class CreateCSVTable:
    def __init__(self, parent: QMainWindow):
        self.parent = parent
        self.dir = self.build()
        self.invoke_editor_window()

    def build(self):
        directory = QFileDialog.getExistingDirectory(self.parent, "Открыть папку", "/home", QFileDialog.ShowDirsOnly |
                                                     QFileDialog.DontResolveSymlinks)
        return directory

    def invoke_editor_window(self):
        self.parent.init_Cvs_Manager_window(self.dir + "/database.csv")
