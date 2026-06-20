from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class PlaceholderPage(QWidget):

    def __init__(
        self,
        main_window,
        title,
        description
    ):
        super().__init__()

        self.main_window = main_window

        layout = QVBoxLayout()
        layout.setContentsMargins(
            40,
            40,
            40,
            40
        )
        layout.setSpacing(
            20
        )

        title_label = QLabel(
            title
        )
        title_label.setObjectName(
            "pageTitle"
        )
        title_label.setAlignment(
            Qt.AlignCenter
        )

        description_label = QLabel(
            description
        )
        description_label.setObjectName(
            "pageSubtitle"
        )
        description_label.setAlignment(
            Qt.AlignCenter
        )
        description_label.setWordWrap(
            True
        )

        back_btn = QPushButton(
            "بازگشت به داشبورد"
        )
        back_btn.setMaximumWidth(
            260
        )
        back_btn.clicked.connect(
            self.main_window.show_dashboard
        )

        layout.addStretch()
        layout.addWidget(
            title_label
        )
        layout.addWidget(
            description_label
        )
        layout.addWidget(
            back_btn,
            alignment=Qt.AlignCenter
        )
        layout.addStretch()

        self.setLayout(
            layout
        )
