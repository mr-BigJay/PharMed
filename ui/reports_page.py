from PySide6.QtWidgets import QWidget


class ReportsPage(QWidget):

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window