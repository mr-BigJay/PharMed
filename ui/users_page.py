from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from services.user_service import (
    list_unit_users,
    set_user_active,
)


class UsersPage(QWidget):

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.users = []
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
            Qt.AlignCenter
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

        back_btn = QPushButton(
            "بازگشت به داشبورد"
        )
        back_btn.clicked.connect(
            self.main_window.show_dashboard
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
        actions_layout.addWidget(
            back_btn
        )
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

    def refresh_data(self):
        user = self.main_window.current_user

        if not user or not user.is_manager:
            self.info_label.setText(
                "فقط مدیر واحد به مدیریت کاربران دسترسی دارد."
            )
            self.users = []
        else:
            self.users = list_unit_users(
                user
            )
            self.info_label.setText(
                f"{len(self.users)} کاربر در محدوده دسترسی شما"
            )

        self.fill_table()

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
