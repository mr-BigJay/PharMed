from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout
)


class PageHeader(QWidget):

    def __init__(
        self,
        title="PharMed",
        subtitle="سامانه مدیریت دارو و تجهیزات پزشکی"
    ):
        super().__init__()

        layout = QVBoxLayout()

        title_label = QLabel(title)

        title_label.setObjectName(
            "pageTitle"
        )

        title_label.setAlignment(
            Qt.AlignCenter
        )

        subtitle_label = QLabel(
            subtitle
        )

        subtitle_label.setObjectName(
            "pageSubtitle"
        )

        subtitle_label.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            title_label
        )

        layout.addWidget(
            subtitle_label
        )

        self.setLayout(layout)