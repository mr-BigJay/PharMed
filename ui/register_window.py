from services.db_session import SessionLocal
from services.user_service import create_user

from models.center import Center
from models.health_house import HealthHouse

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QComboBox,
    QMessageBox
)

from services.auth_service import (
    validate_mobile,
    validate_persian
)


class RegisterWindow(QWidget):

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.db = SessionLocal()

        layout = QVBoxLayout()
        layout.setContentsMargins(
            60,
            30,
            60,
            30
        )

        layout.setSpacing(12)

        title = QLabel("ثبت نام کاربر جدید")
        layout.addWidget(title)

        self.first_name = QLineEdit()
        self.first_name.setPlaceholderText("نام")
        layout.addWidget(self.first_name)

        self.last_name = QLineEdit()
        self.last_name.setPlaceholderText("نام خانوادگی")
        layout.addWidget(self.last_name)

        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("09xxxxxxxxx")
        layout.addWidget(self.mobile)

        self.password = QLineEdit()
        self.password.setPlaceholderText("رمز عبور")
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)

        self.confirm_password = QLineEdit()
        self.confirm_password.setPlaceholderText("تکرار رمز عبور")
        self.confirm_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.confirm_password)

        self.unit_type = QComboBox()
        self.unit_type.addItems([
            "مرکز درمانی",
            "خانه بهداشت"
        ])

        self.unit_type.currentTextChanged.connect(
            self.unit_changed
        )

        layout.addWidget(self.unit_type)

        self.center_combo = QComboBox()
        layout.addWidget(self.center_combo)

        self.house_combo = QComboBox()
        layout.addWidget(self.house_combo)

        register_btn = QPushButton("ثبت نام")
        register_btn.clicked.connect(
            self.validate_form
        )

        layout.addWidget(register_btn)

        back_btn = QPushButton("بازگشت به ورود")

        back_btn.clicked.connect(
            self.go_back
        )

        layout.addWidget(back_btn)

        self.setLayout(layout)

        self.load_centers()

        self.center_combo.currentIndexChanged.connect(
            self.load_health_houses
        )

        self.unit_changed(
            self.unit_type.currentText()
        )

    def go_back(self):

        self.main_window.show_login()

    def unit_changed(self, value):

        if value == "مرکز درمانی":

            self.house_combo.hide()

        else:

            self.house_combo.show()

    def load_centers(self):

        self.center_combo.clear()

        self.center_combo.addItem(
            "انتخاب مرکز",
            None
        )

        centers = (
            self.db.query(Center)
            .order_by(Center.name)
            .all()
        )

        for center in centers:

            self.center_combo.addItem(
                center.name,
                center.id
            )

    def load_health_houses(self):

        self.house_combo.clear()

        self.house_combo.addItem(
            "انتخاب خانه بهداشت",
            None
        )

        center_id = self.center_combo.currentData()

        if center_id is None:
            return

        houses = (
            self.db.query(HealthHouse)
            .filter(
                HealthHouse.center_id == center_id
            )
            .order_by(HealthHouse.name)
            .all()
        )

        for house in houses:

            self.house_combo.addItem(
                house.name,
                house.id
            )

    def validate_form(self):

        first_name = self.first_name.text().strip()
        last_name = self.last_name.text().strip()
        mobile = self.mobile.text().strip()

        password = self.password.text()
        confirm_password = self.confirm_password.text()

        if not validate_persian(first_name):

            QMessageBox.warning(
                self,
                "خطا",
                "نام باید فارسی باشد"
            )
            return

        if not validate_persian(last_name):

            QMessageBox.warning(
                self,
                "خطا",
                "نام خانوادگی باید فارسی باشد"
            )
            return

        if not validate_mobile(mobile):

            QMessageBox.warning(
                self,
                "خطا",
                "شماره موبایل معتبر نیست"
            )
            return

        if len(password) < 6:

            QMessageBox.warning(
                self,
                "خطا",
                "رمز عبور حداقل 6 کاراکتر باشد"
            )
            return

        if password != confirm_password:

            QMessageBox.warning(
                self,
                "خطا",
                "تکرار رمز عبور صحیح نیست"
            )
            return

        center_id = self.center_combo.currentData()

        if center_id is None:

            QMessageBox.warning(
                self,
                "خطا",
                "لطفاً مرکز را انتخاب کنید"
            )
            return

        role = "پرستار"
        health_house_id = None

        if self.unit_type.currentText() == "خانه بهداشت":

            role = "بهورز"

            health_house_id = (
                self.house_combo.currentData()
            )

            if health_house_id is None:

                QMessageBox.warning(
                    self,
                    "خطا",
                    "لطفاً خانه بهداشت را انتخاب کنید"
                )
                return

        success, message = create_user(
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
            password=password,
            role=role,
            center_id=center_id,
            health_house_id=health_house_id,
            require_manager=True
        )

        if success:

            QMessageBox.information(
                self,
                "موفق",
                message
            )

            self.first_name.clear()
            self.last_name.clear()
            self.mobile.clear()
            self.password.clear()
            self.confirm_password.clear()

            self.main_window.show_login()

        else:

            QMessageBox.warning(
                self,
                "خطا",
                message
            )
