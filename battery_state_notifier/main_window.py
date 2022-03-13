import pathlib
import sys

from PySide2.QtWidgets import QMainWindow, QLabel, QMessageBox, QSystemTrayIcon, QMenu
from PySide2.QtGui import QCloseEvent, QHideEvent, QIcon

from battery_state_notifier.battery_state_checker import StateChecker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Battery notifier")
        self.setGeometry(0, 0, 240, 100)
        self.setFixedSize(240, 100)

        self.status_label = self._setup_label("Status: ", 15, 10, 170, 32)
        self.capacity_label = self._setup_label("Capacity: ", 15, 50, 170, 32)

        self._setup_tray_icon()

        self.current_state: str = ""
        self.current_capacity: int = 0

        self.minimum_capacity_level = 20

        self.state_checker = StateChecker(self)
        self.state_checker.state_changed_signal.connect(self._update_state)
        self.state_checker.start_checker()

    def _setup_label(self, text: str, x: int, y: int, width: int, height: int) -> QLabel:
        label = QLabel(text, self)
        label.resize(width, height)
        label.move(x, y)
        return label

    def _setup_tray_icon(self):
        self.tray_icon = QSystemTrayIcon()
        self.tray_icon.setIcon(self._get_icon("medium"))
        self.tray_icon.setContextMenu(self._get_try_icon_menu())
        self.tray_icon.show()

    @staticmethod
    def _get_icon(icon_name: str) -> QIcon:
        icon_folder_path = pathlib.Path(__file__).parent.resolve() / "icons"

        icon_names = {
            "charging": "battery_charging_icon.png",
            "empty": "battery_empty_icon.png",
            "low": "battery_low_icon.png",
            "medium": "battery_medium_icon.png",
            "full": "battery_full_icon.png"
        }

        return QIcon(str(icon_folder_path / icon_names[icon_name]))

    def _get_try_icon_menu(self):
        menu = QMenu()

        toggle_visibility_action = menu.addAction("show/hide")
        toggle_visibility_action.triggered.connect(self._toggle_visibility)

        exit_action = menu.addAction("exit")
        exit_action.triggered.connect(self.close)

        return menu

    def _toggle_visibility(self) -> None:
        if self.isVisible():
            self.hide()
        else:
            self.showNormal()

    def _update_state(self, status, capacity) -> None:
        self.status_label.setText(f"Status: {status}")
        self.capacity_label.setText(f"Capacity: {capacity}%")

        self._update_icon(status, capacity)
        self._check_the_minimum_level(status, capacity)

    def _update_icon(self, status, capacity):
        if capacity >= 90:
            icon_name = "full"
        elif status == "Charging" and capacity < 90:
            icon_name = "charging"
        else:
            if 90 > capacity >= 50:
                icon_name = "medium"
            elif 50 > capacity >= self.minimum_capacity_level:
                icon_name = "low"
            else:
                icon_name = "empty"

        self.tray_icon.setIcon(self._get_icon(icon_name))

    def _check_the_minimum_level(self, status: str, capacity: int) -> None:
        if status == "Discharging" and capacity < self.minimum_capacity_level:
            self._display_warning()

    @staticmethod
    def _display_warning() -> None:
        QMessageBox(QMessageBox.Warning, "The battery is low!", "Please connect the power supply", QMessageBox.Ok)\
            .exec_()

    def hideEvent(self, event: QHideEvent) -> None:
        self.hide()

    def closeEvent(self, event: QCloseEvent):
        self.hide()
        self.state_checker.run_checker = False
        sys.exit()
