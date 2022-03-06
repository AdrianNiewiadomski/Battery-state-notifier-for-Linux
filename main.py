import sys

from PySide2.QtWidgets import QApplication

from main_window import MainWindow


if __name__ == '__main__':
    my_app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    my_app.exec_()
    sys.exit(0)
