import sys
from PyQt5.QtWidgets import QApplication
from screen.root.MainMenuWindow import MainMenuWindow


def main():
    app = QApplication(sys.argv)
    menu = MainMenuWindow()
    menu.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
