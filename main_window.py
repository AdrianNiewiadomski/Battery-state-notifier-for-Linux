from PySide2.QtWidgets import QMainWindow, QLabel, QMessageBox
from PySide2.QtGui import QCloseEvent

from battery_state_checker import StateChecker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Battery notifier")
        self.setGeometry(0, 0, 240, 100)
        self.setFixedSize(240, 100)

        self.status_label = self._setup_label("Status: ", 15, 10, 170, 32)
        self.capacity_label = self._setup_label("Capacity: ", 15, 50, 170, 32)

        self.current_state: str = ""
        self.current_capacity: int = 0

        self.minimum_capacity_level = 90

        self.state_checker = StateChecker(self)
        self.state_checker.state_changed_signal.connect(self._update_labels)
        self.state_checker.start_checker()

    def _setup_label(self, text: str, x: int, y: int, width: int, height: int) -> QLabel:
        label = QLabel(text, self)
        label.resize(width, height)
        label.move(x, y)
        return label

    def _update_labels(self, status, capacity) -> None:
        self.status_label.setText(f"Status: {status}")

        self._check_the_minimum_level(status, capacity)
        self.capacity_label.setText(f"Capacity: {capacity}%")

    def _check_the_minimum_level(self, status: str, capacity: int) -> None:
        if status == "Discharging" and capacity < self.minimum_capacity_level:
            self._display_warning()

    @staticmethod
    def _display_warning() -> None:
        QMessageBox(QMessageBox.Warning, "The battery is low!", "Please connect the power supply", QMessageBox.Ok)\
            .exec_()

    def closeEvent(self, event: QCloseEvent):
        self.state_checker.run_checker = False
