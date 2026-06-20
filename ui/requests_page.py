from PySide6.QtWidgets import QWidget


class RequestsPage(QWidget):

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window