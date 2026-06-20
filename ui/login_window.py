from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox
)
from services.auth_service import (
    validate_mobile,
    login_user
)


class LoginWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()
        layout.setContentsMargins(
            40,
            30,
            40,
            30
        )
        layout.setSpacing(15)
        title = QLabel("PharMed")
        title.setAlignment(Qt.AlignCenter)
        font = title.font()
        font.setPointSize(36)
        font.setBold(True)
        title.setFont(font)
        layout.addWidget(title)
        subtitle = QLabel(
            "سامانه مدیریت دارو و تجهیزات پزشکی"
        )
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        description = QLabel(
            "مدیریت موجودی، درخواست‌ها و توزیع دارو و تجهیزات پزشکی"
        )
        description.setAlignment(Qt.AlignCenter)
        layout.addWidget(description)
        layout.addSpacing(20)
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText(
            "شماره موبایل"
        )
        layout.addWidget(self.mobile)
        self.password = QLineEdit()
        self.password.setPlaceholderText(
            "رمز عبور"
        )
        self.password.setEchoMode(
            QLineEdit.Password
        )
        layout.addWidget(self.password)
        login_btn = QPushButton(
            "ورود"
        )
        login_btn.clicked.connect(
            self.login
        )
        layout.addWidget(login_btn)
        register_btn = QPushButton(
            "ثبت نام"
        )
        register_btn.clicked.connect(
            self.open_register
        )
        layout.addWidget(register_btn)
        layout.addStretch()
        footer = QLabel(
            "طراحی و توسعه\nصادق جعفری با همکاری علیرضا محمدرضایی"
        )
        footer.setAlignment(
            Qt.AlignCenter
        )
        font = footer.font()
        font.setPointSize(11)
        footer.setFont(font)
        layout.addWidget(footer)
        self.setLayout(layout)

    def open_register(self):
        self.main_window.show_register()

    def login(self):
        mobile = self.mobile.text().strip()
        password = self.password.text()
        if not validate_mobile(mobile):
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