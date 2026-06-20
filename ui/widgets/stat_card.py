from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout
)


class StatCard(QFrame):

    def __init__(
        self,
        title,
        value
    ):
        super().__init__()
        self.setMaximumWidth(220)
        self.setMinimumHeight(80)
        self.setMaximumHeight(95)

        self.setObjectName(
            "statCard"
        )

        layout = QVBoxLayout()

        value_label = QLabel(
            str(value)
        )

        value_label.setAlignment(
            Qt.AlignCenter
        )

        font = value_label.font()

        font.setPointSize(20)
        font.setBold(True)

        value_label.setFont(font)

        title_label = QLabel(title)

        title_label.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            value_label
        )

        layout.addWidget(
            title_label
        )

        self.setLayout(layout)