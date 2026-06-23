from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from services.auth_service import (
    login_user,
    validate_mobile,
)


class LoginWindow(QWidget):

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.setLayoutDirection(
            Qt.RightToLeft
        )

        root_layout = QVBoxLayout()
        root_layout.setContentsMargins(
            24,
            24,
            24,
            24
        )
        root_layout.setSpacing(
            0
        )

        root_layout.addStretch(
            1
        )

        login_card = QFrame()
        login_card.setObjectName(
            "loginCard"
        )
        login_card.setFixedWidth(
            420
        )
        login_card.setMinimumHeight(
            460
        )
        login_card.setMaximumHeight(
            520
        )

        card_layout = QVBoxLayout(
            login_card
        )
        card_layout.setContentsMargins(
            36,
            32,
            36,
            32
        )
        card_layout.setSpacing(
            14
        )

        card_layout.addStretch(
            1
        )

        title = QLabel(
            "PharMed"
        )
        title.setObjectName(
            "loginTitle"
        )
        title.setAlignment(
            Qt.AlignCenter
        )
        card_layout.addWidget(
            title
        )

        subtitle = QLabel(
            "سامانه مدیریت دارو و تجهیزات پزشکی"
        )
        subtitle.setObjectName(
            "loginSubtitle"
        )
        subtitle.setAlignment(
            Qt.AlignCenter
        )
        subtitle.setWordWrap(
            True
        )
        card_layout.addWidget(
            subtitle
        )

        description = QLabel(
            "مدیریت موجودی، درخواست‌ها و توزیع دارو و تجهیزات پزشکی"
        )
        description.setObjectName(
            "loginDescription"
        )
        description.setAlignment(
            Qt.AlignCenter
        )
        description.setWordWrap(
            True
        )
        card_layout.addWidget(
            description
        )

        card_layout.addSpacing(
            12
        )

        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText(
            "شماره موبایل"
        )
        self.mobile.setObjectName(
            "loginInput"
        )
        card_layout.addWidget(
            self.mobile
        )

        self.password = QLineEdit()
        self.password.setPlaceholderText(
            "رمز عبور"
        )
        self.password.setEchoMode(
            QLineEdit.Password
        )
        self.password.setObjectName(
            "loginInput"
        )
        card_layout.addWidget(
            self.password
        )

        login_btn = QPushButton(
            "ورود"
        )
        login_btn.setObjectName(
            "loginPrimaryButton"
        )
        login_btn.clicked.connect(
            self.login
        )
        card_layout.addWidget(
            login_btn
        )

        register_btn = QPushButton(
            "ثبت نام"
        )
        register_btn.setObjectName(
            "loginSecondaryButton"
        )
        register_btn.clicked.connect(
            self.open_register
        )
        card_layout.addWidget(
            register_btn
        )

        card_layout.addStretch(
            1
        )

        root_layout.addWidget(
            login_card,
            alignment=Qt.AlignHCenter
        )
        root_layout.addStretch(
            1
        )

        footer = QLabel(
            "طراحی و توسعه\n"
            "صادق جعفری با همکاری علیرضا محمدرضایی"
        )
        footer.setObjectName(
            "loginFooter"
        )
        footer.setAlignment(
            Qt.AlignCenter
        )
        root_layout.addWidget(
            footer
        )

        self.setLayout(
            root_layout
        )

    def open_register(self):
        self.main_window.show_register()

    def login(self):
        mobile = self.mobile.text().strip()
        password = self.password.text()

        if not validate_mobile(
            mobile
        ):
            QMessageBox.warning(
                self,
                "خطا",
                "شماره موبایل معتبر نیست"
            )
            return

        user = login_user(
            mobile,
            password
        )

        if not user:
            QMessageBox.warning(
                self,
                "خطا",
                "شماره موبایل یا رمز عبور اشتباه است"
            )
            return

        self.main_window.current_user = user
        self.main_window.show_dashboard()
