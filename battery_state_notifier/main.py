import sys

from PySide2.QtWidgets import QApplication

from battery_state_notifier.main_window import MainWindow


def main():
    my_app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    my_app.exec_()
    sys.exit(0)


if __name__ == '__main__':
    main()
