from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout
)

from PySide6.QtCore import Qt


class InventoryPage(QWidget):

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        layout = QVBoxLayout()

        title = QLabel(
            "مدیریت موجودی دارو"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            title
        )

        self.setLayout(
            layout
        )