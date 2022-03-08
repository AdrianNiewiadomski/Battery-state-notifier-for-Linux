from time import sleep
from threading import Thread

from PySide2.QtCore import Signal, QObject


class StateChecker(QObject):
    state_changed_signal = Signal(str, int)

    DIR_PATH = "/sys/class/power_supply/BAT1"

    def __init__(self, parent):
        super().__init__(parent)

        self.run_checker = True
        self.parent = parent

        self.thread = Thread(target=self._run_state_checker)

    def _run_state_checker(self) -> None:
        while self.run_checker:
            status = self._get_parameter("status").strip()
            capacity = int(self._get_parameter("capacity").strip())
            if self.parent.current_state != status or self.parent.current_capacity != capacity:
                self.state_changed_signal.emit(status, capacity)
            sleep(30)

    def _get_parameter(self, parameter_name: str) -> str:
        with open(self.DIR_PATH + "/" + parameter_name, "r") as capacity_file:
            parameter = capacity_file.read()
        return parameter

    def start_checker(self):
        self.thread.start()
