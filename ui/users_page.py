from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from services.auth_service import (
    validate_mobile,
    validate_persian,
)
from services.user_service import (
    create_unit_user,
    get_user_capacity,
    list_unit_users,
    set_user_active,
)


class UsersPage(QWidget):

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.users = []
        self.capacity = {
            "registered": 0,
            "max_users": 0,
            "remaining": 0,
        }
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(
            40,
            30,
            40,
            30
        )
        layout.setSpacing(
            18
        )

        title = QLabel(
            "مدیریت کاربران"
        )
        title.setObjectName(
            "pageTitle"
        )
        title.setAlignment(
            Qt.AlignRight
        )
        layout.addWidget(
            title
        )

        self.info_label = QLabel()
        self.info_label.setObjectName(
            "pageSubtitle"
        )
        self.info_label.setAlignment(
            Qt.AlignCenter
        )
        layout.addWidget(
            self.info_label
        )

        self.create_user_group = self.build_create_user_group()
        layout.addWidget(
            self.create_user_group
        )

        actions_layout = QHBoxLayout()

        refresh_btn = QPushButton(
            "به‌روزرسانی"
        )
        refresh_btn.clicked.connect(
            self.refresh_data
        )

        activate_btn = QPushButton(
            "فعال‌سازی کاربر"
        )
        activate_btn.clicked.connect(
            lambda: self.change_selected_user_status(True)
        )

        deactivate_btn = QPushButton(
            "غیرفعال‌سازی کاربر"
        )
        deactivate_btn.clicked.connect(
            lambda: self.change_selected_user_status(False)
        )

        actions_layout.addWidget(
            refresh_btn
        )
        actions_layout.addWidget(
            activate_btn
        )
        actions_layout.addWidget(
            deactivate_btn
        )
        actions_layout.addStretch()
        layout.addLayout(
            actions_layout
        )

        self.users_table = QTableWidget()
        self.users_table.setColumnCount(
            6
        )
        self.users_table.setHorizontalHeaderLabels([
            "شناسه",
            "نام کامل",
            "موبایل",
            "نقش",
            "مدیر",
            "وضعیت",
        ])
        self.users_table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )
        self.users_table.setSelectionBehavior(
            QTableWidget.SelectRows
        )
        layout.addWidget(
            self.users_table
        )

        self.setLayout(
            layout
        )

        self.refresh_data()

    def build_create_user_group(self):
        group = QGroupBox(
            "ایجاد کاربر جدید برای همین واحد"
        )
        form = QFormLayout(group)

        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText(
            "نام"
        )
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText(
            "نام خانوادگی"
        )
        self.mobile_input = QLineEdit()
        self.mobile_input.setPlaceholderText(
            "09xxxxxxxxx"
        )
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText(
            "رمز عبور"
        )
        self.password_input.setEchoMode(
            QLineEdit.Password
        )

        create_btn = QPushButton(
            "ایجاد کاربر"
        )
        create_btn.clicked.connect(
            self.create_user
        )

        form.addRow(
            "نام:",
            self.first_name_input
        )
        form.addRow(
            "نام خانوادگی:",
            self.last_name_input
        )
        form.addRow(
            "موبایل:",
            self.mobile_input
        )
        form.addRow(
            "رمز عبور:",
            self.password_input
        )
        form.addRow(
            create_btn
        )

        return group

    def refresh_data(self):
        user = self.main_window.current_user

        if not user or not user.is_manager:
            self.info_label.setText(
                "فقط مدیر واحد به مدیریت کاربران دسترسی دارد."
            )
            self.users = []
            self.capacity = {
                "registered": 0,
                "max_users": 0,
                "remaining": 0,
            }
            self.create_user_group.setEnabled(
                False
            )
        else:
            self.capacity = get_user_capacity(
                user
            )
            self.users = list_unit_users(
                user
            )
            self.info_label.setText(
                (
                    f"{self.capacity['registered']} از "
                    f"{self.capacity['max_users']} کاربر ثبت شده | "
                    f"ظرفیت باقی‌مانده: {self.capacity['remaining']}"
                )
            )
            self.create_user_group.setEnabled(
                self.capacity["remaining"] > 0
            )

        self.fill_table()

    def create_user(self):
        first_name = self.first_name_input.text().strip()
        last_name = self.last_name_input.text().strip()
        mobile = self.mobile_input.text().strip()
        password = self.password_input.text()

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

        success, message = create_unit_user(
            self.main_window.current_user,
            first_name,
            last_name,
            mobile,
            password
        )

        if success:
            QMessageBox.information(
                self,
                "موفق",
                message
            )
            self.first_name_input.clear()
            self.last_name_input.clear()
            self.mobile_input.clear()
            self.password_input.clear()
            self.refresh_data()
        else:
            QMessageBox.warning(
                self,
                "خطا",
                message
            )

    def fill_table(self):
        self.users_table.setRowCount(
            len(self.users)
        )

        for row_index, user in enumerate(self.users):
            values = [
                user["id"],
                user["full_name"],
                user["mobile"],
                user["role"],
                "بله" if user["is_manager"] else "خیر",
                "فعال" if user["is_active"] else "غیرفعال",
            ]

            for column_index, value in enumerate(values):
                item = QTableWidgetItem(
                    str(value)
                )
                if column_index in (0, 4, 5):
                    item.setTextAlignment(
                        Qt.AlignCenter
                    )
                self.users_table.setItem(
                    row_index,
                    column_index,
                    item
                )

        self.users_table.resizeColumnsToContents()

    def change_selected_user_status(
        self,
        is_active
    ):
        selected_items = self.users_table.selectedItems()

        if not selected_items:
            QMessageBox.warning(
                self,
                "خطا",
                "ابتدا یک کاربر را انتخاب کنید"
            )
            return

        selected_row = selected_items[0].row()
        user_id = self.users[selected_row]["id"]

        success, message = set_user_active(
            self.main_window.current_user,
            user_id,
            is_active
        )

        if success:
            QMessageBox.information(
                self,
                "موفق",
                message
            )
            self.refresh_data()
        else:
            QMessageBox.warning(
                self,
                "خطا",
                message
            )
