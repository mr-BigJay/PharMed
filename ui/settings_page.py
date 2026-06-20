from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class SettingsPage(QWidget):

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(
            28,
            24,
            28,
            24
        )
        layout.setSpacing(
            18
        )

        title = QLabel(
            "تنظیمات سامانه"
        )
        title.setObjectName(
            "pageTitle"
        )
        title.setAlignment(
            Qt.AlignRight
        )

        subtitle = QLabel(
            "تنظیمات عمومی نرم‌افزار مدیریت انبار دارو و اقلام پزشکی"
        )
        subtitle.setObjectName(
            "pageSubtitle"
        )
        subtitle.setAlignment(
            Qt.AlignRight
        )

        layout.addWidget(
            title
        )
        layout.addWidget(
            subtitle
        )

        grid = QGridLayout()
        grid.setSpacing(
            14
        )
        cards = [
            (
                "نام نرم‌افزار",
                "PharMed",
            ),
            (
                "نسخه",
                "v0.1",
            ),
            (
                "دامنه استفاده",
                "شبکه بهداشت و درمان شهرستان",
            ),
            (
                "نوع گردش کالا",
                "گردش داخلی اقلام در شبکه بهداشت و درمان",
            ),
        ]

        for index, (label, value) in enumerate(cards):
            grid.addWidget(
                self.build_setting_card(
                    label,
                    value
                ),
                index // 2,
                index % 2
            )

        layout.addLayout(
            grid
        )
        layout.addStretch()

        logout_btn = QPushButton(
            "خروج از حساب کاربری"
        )
        logout_btn.setObjectName(
            "dangerButton"
        )
        logout_btn.clicked.connect(
            self.logout
        )
        layout.addWidget(
            logout_btn,
            alignment=Qt.AlignLeft
        )

        self.setLayout(
            layout
        )

    def build_setting_card(
        self,
        label,
        value
    ):
        card = QFrame()
        card.setObjectName(
            "panelCard"
        )
        card.setMinimumHeight(
            110
        )
        layout = QVBoxLayout(card)

        label_widget = QLabel(
            label
        )
        label_widget.setObjectName(
            "metricTitle"
        )
        value_widget = QLabel(
            value
        )
        value_widget.setObjectName(
            "summaryRow"
        )
        value_widget.setWordWrap(
            True
        )

        layout.addWidget(
            label_widget
        )
        layout.addWidget(
            value_widget
        )
        layout.addStretch()

        return card

    def logout(self):
        self.main_window.current_user = None
        self.main_window.show_login()
