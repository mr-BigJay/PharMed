from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)

from services.datetime_service import (
    format_tehran_jalali_label,
    format_tehran_time,
)


class DateTimeCard(QFrame):

    def __init__(
        self,
        parent=None
    ):
        super().__init__(
            parent
        )

        self.setObjectName(
            "topDateTimeCard"
        )

        layout = QVBoxLayout(
            self
        )
        layout.setContentsMargins(
            16,
            4,
            16,
            4
        )
        layout.setSpacing(
            2
        )

        self.time_label = QLabel()
        self.time_label.setObjectName(
            "topClockValue"
        )
        self.time_label.setAlignment(
            Qt.AlignCenter
        )

        self.date_label = QLabel()
        self.date_label.setObjectName(
            "topDateValue"
        )
        self.date_label.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            self.time_label
        )
        layout.addWidget(
            self.date_label
        )

        self.refresh()

    def refresh(self):
        self.time_label.setText(
            format_tehran_time()
        )
        self.date_label.setText(
            format_tehran_jalali_label()
        )
