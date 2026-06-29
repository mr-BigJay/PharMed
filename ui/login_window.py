from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QMessageBox,
)

from services.auth_service import (
    validate_mobile,
    login_user,
)


class LoginWindow(QWidget):

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.password_visible = False

        self.setObjectName("loginPage")
        self.setLayoutDirection(Qt.RightToLeft)

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        form_panel = QFrame()
        form_panel.setObjectName("loginFormPanel")
        form_panel.setAutoFillBackground(True)
        form_outer = QVBoxLayout(form_panel)
        form_outer.setContentsMargins(64, 48, 64, 32)
        form_outer.setSpacing(0)

        form_column = QWidget()
        form_column.setObjectName("loginFormColumn")
        form_layout = QVBoxLayout(form_column)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(0)

        title = QLabel("PharMed")
        title.setObjectName("loginTitle")
        title.setAlignment(
            Qt.AlignRight | Qt.AlignVCenter
        )

        subtitle = QLabel(
            "سامانه مدیریت دارو و تجهیزات پزشکی"
        )
        subtitle.setObjectName("loginSubtitle")
        subtitle.setAlignment(
            Qt.AlignRight | Qt.AlignVCenter
        )

        form_layout.addWidget(title)
        form_layout.addSpacing(8)
        form_layout.addWidget(subtitle)
        form_layout.addSpacing(28)

        mobile_label = QLabel("شماره موبایل")
        mobile_label.setObjectName("loginFieldLabel")
        mobile_label.setAlignment(
            Qt.AlignRight | Qt.AlignVCenter
        )
        form_layout.addWidget(mobile_label)
        form_layout.addSpacing(8)

        self.mobile = QLineEdit()
        self.mobile.setObjectName("loginInput")
        self.mobile.setPlaceholderText("0912 123 4567")
        self.mobile.setAlignment(Qt.AlignRight)
        self.mobile.addAction(
            QAction("📱", self.mobile),
            QLineEdit.ActionPosition.LeadingPosition,
        )
        form_layout.addWidget(self.mobile)
        form_layout.addSpacing(18)

        password_label = QLabel("رمز عبور")
        password_label.setObjectName("loginFieldLabel")
        password_label.setAlignment(
            Qt.AlignRight | Qt.AlignVCenter
        )
        form_layout.addWidget(password_label)
        form_layout.addSpacing(8)

        self.password = QLineEdit()
        self.password.setObjectName("loginInput")
        self.password.setPlaceholderText(
            "رمز عبور خود را وارد کنید"
        )
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setAlignment(Qt.AlignRight)
        self.password.addAction(
            QAction("🔒", self.password),
            QLineEdit.ActionPosition.LeadingPosition,
        )
        self.toggle_password_action = QAction(
            "👁",
            self.password
        )
        self.toggle_password_action.triggered.connect(
            self.toggle_password_visibility
        )
        self.password.addAction(
            self.toggle_password_action,
            QLineEdit.ActionPosition.TrailingPosition,
        )
        form_layout.addWidget(self.password)
        form_layout.addSpacing(10)

        forgot_link = QLabel(
            "رمز عبور خود را فراموش کرده‌اید؟"
        )
        forgot_link.setObjectName("loginForgotLink")
        forgot_link.setAlignment(
            Qt.AlignRight | Qt.AlignVCenter
        )
        forgot_link.setCursor(Qt.PointingHandCursor)
        form_layout.addWidget(forgot_link)
        form_layout.addSpacing(22)

        login_btn = QPushButton("ورود")
        login_btn.setObjectName("loginPrimaryButton")
        login_btn.clicked.connect(self.login)
        form_layout.addWidget(login_btn)
        form_layout.addSpacing(12)

        register_btn = QPushButton("ثبت نام")
        register_btn.setObjectName("loginSecondaryButton")
        register_btn.clicked.connect(self.open_register)
        form_layout.addWidget(register_btn)
        form_layout.addSpacing(28)

        security_note = QLabel(
            "🛡️  اطلاعات شما نزد ما کاملاً امن و محرمانه است."
        )
        security_note.setObjectName("loginSecurityNote")
        security_note.setAlignment(
            Qt.AlignRight | Qt.AlignVCenter
        )
        security_note.setWordWrap(True)
        form_layout.addWidget(security_note)
        form_layout.addSpacing(8)

        developer_credit = QLabel(
            "طراحی و توسعه توسط صادق جعفری با همکاری علیرضا محمدرضایی"
        )
        developer_credit.setObjectName("loginDeveloperCredit")
        developer_credit.setAlignment(
            Qt.AlignRight | Qt.AlignVCenter
        )
        developer_credit.setWordWrap(True)
        form_layout.addWidget(developer_credit)

        form_outer.addStretch(1)
        form_outer.addWidget(
            form_column,
            alignment=Qt.AlignHCenter
        )
        form_outer.addStretch(1)

        hero_panel = QFrame()
        hero_panel.setObjectName("loginHeroPanel")
        hero_layout = QVBoxLayout(hero_panel)
        hero_layout.setContentsMargins(0, 0, 0, 0)
        hero_layout.setSpacing(0)

        hero_image = QLabel()
        hero_image.setObjectName("loginHeroImage")
        hero_image.setAlignment(Qt.AlignCenter)
        hero_image.setScaledContents(True)

        hero_path = Path(__file__).resolve().parent.parent / (
            "assets/login_hero.png"
        )
        if hero_path.exists():
            hero_image.setPixmap(
                QPixmap(str(hero_path))
            )

        hero_layout.addWidget(hero_image)

        root.addWidget(form_panel, stretch=1)
        root.addWidget(hero_panel, stretch=1)

    def toggle_password_visibility(self):
        self.password_visible = not self.password_visible
        self.password.setEchoMode(
            QLineEdit.Normal
            if self.password_visible
            else QLineEdit.Password
        )
        self.toggle_password_action.setText(
            "🙈" if self.password_visible else "👁"
        )

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
