from time import sleep
from threading import Thread

from PySide2.QtWidgets import QMainWindow, QLabel
from PySide2.QtGui import QCloseEvent

from battery_state_checker import get_parameter


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(0, 0, 200, 100)
        self.setFixedSize(200, 100)

        self.status_label = QLabel("Status: ", self)
        self.status_label.resize(170, 32)
        self.status_label.move(15, 10)

        self.capacity_label = QLabel("Capacity: ", self)
        self.capacity_label.resize(170, 32)
        self.capacity_label.move(15, 50)

        self.run_notifier = True
        thread = Thread(target=self._run_state_notifier)
        thread.start()

    def _run_state_notifier(self) -> None:
        while self.run_notifier:
            self._update_labels()
            sleep(30)

    def _update_labels(self) -> None:
        status = get_parameter("status").strip()
        self.status_label.setText(f"Status: {status}")

        capacity = get_parameter("capacity").strip()
        self.capacity_label.setText(f"Capacity: {capacity}")
        self.repaint()

    def closeEvent(self, event: QCloseEvent):
        self.run_notifier = False
