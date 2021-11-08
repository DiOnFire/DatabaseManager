from PyQt5.QtWidgets import QMessageBox, QWidget


class MessageBoxBuilder:
    def __init__(self, message: str, title: str, parent: QWidget):
        self.message = message
        self.title = title
        self.parent = parent
        self.build()

    def build(self):
        message = QMessageBox(self.parent)
        message.setWindowTitle(self.title)
        message.setText(self.message)
        message.show()
