from PySide6.QtWidgets import QWidget


class EquipmentPage(QWidget):

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window