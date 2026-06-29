from PySide6.QtCore import Qt
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
        self.setObjectName("loginPage")
        self.setLayoutDirection(Qt.RightToLeft)

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        form_panel = QFrame()
        form_panel.setObjectName("loginFormPanel")
        form_layout = QVBoxLayout(form_panel)
        form_layout.setContentsMargins(56, 48, 56, 36)
        form_layout.setSpacing(14)

        title = QLabel("PharMed")
        title.setObjectName("loginTitle")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel(
            "سامانه مدیریت دارو و تجهیزات پزشکی"
        )
        subtitle.setObjectName("loginSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)

        description = QLabel(
            "مدیریت موجودی، درخواست‌ها و توزیع دارو و تجهیزات پزشکی"
        )
        description.setObjectName("loginDescription")
        description.setAlignment(Qt.AlignCenter)
        description.setWordWrap(True)

        form_layout.addStretch(1)
        form_layout.addWidget(title)
        form_layout.addWidget(subtitle)
        form_layout.addWidget(description)
        form_layout.addSpacing(18)

        self.mobile = QLineEdit()
        self.mobile.setObjectName("loginInput")
        self.mobile.setPlaceholderText("شماره موبایل")
        form_layout.addWidget(self.mobile)

        self.password = QLineEdit()
        self.password.setObjectName("loginInput")
        self.password.setPlaceholderText("رمز عبور")
        self.password.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(self.password)

        form_layout.addSpacing(6)

        login_btn = QPushButton("ورود")
        login_btn.setObjectName("loginPrimaryButton")
        login_btn.clicked.connect(self.login)
        form_layout.addWidget(login_btn)

        register_btn = QPushButton("ثبت نام")
        register_btn.setObjectName("loginSecondaryButton")
        register_btn.clicked.connect(self.open_register)
        form_layout.addWidget(register_btn)

        form_layout.addStretch(2)

        footer = QLabel(
            "طراحی و توسعه توسط صادق جعفری با همکاری علیرضا محمدرضایی"
        )
        footer.setObjectName("loginFooter")
        footer.setAlignment(Qt.AlignCenter)
        footer.setWordWrap(True)
        form_layout.addWidget(footer)

        hero_panel = QFrame()
        hero_panel.setObjectName("loginHeroPanel")
        hero_layout = QVBoxLayout(hero_panel)
        hero_layout.setContentsMargins(48, 48, 48, 48)
        hero_layout.setSpacing(16)

        hero_title = QLabel("PharMed")
        hero_title.setObjectName("loginHeroTitle")
        hero_title.setAlignment(Qt.AlignCenter)

        hero_subtitle = QLabel(
            "شبکه بهداشت و درمان شهرستان"
        )
        hero_subtitle.setObjectName("loginHeroSubtitle")
        hero_subtitle.setAlignment(Qt.AlignCenter)

        icons_row = QHBoxLayout()
        icons_row.setSpacing(24)
        icons_row.addStretch(1)
        for icon in ("💊", "🏥", "📦", "🩺"):
            icon_label = QLabel(icon)
            icon_label.setObjectName("loginHeroIcon")
            icon_label.setAlignment(Qt.AlignCenter)
            icons_row.addWidget(icon_label)
        icons_row.addStretch(1)

        hero_tagline = QLabel(
            "مدیریت یکپارچه انبار دارو\n"
            "و تجهیزات پزشکی"
        )
        hero_tagline.setObjectName("loginHeroTagline")
        hero_tagline.setAlignment(Qt.AlignCenter)

        hero_layout.addStretch(1)
        hero_layout.addWidget(hero_title)
        hero_layout.addWidget(hero_subtitle)
        hero_layout.addSpacing(24)
        hero_layout.addLayout(icons_row)
        hero_layout.addSpacing(24)
        hero_layout.addWidget(hero_tagline)
        hero_layout.addStretch(2)

        root.addWidget(form_panel, stretch=5)
        root.addWidget(hero_panel, stretch=4)

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
