from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from services.update_service import (
    current_version_label,
    open_release_page,
)
from ui.widgets.update_worker import (
    UpdateApplyWorker,
    UpdateCheckWorker,
)
from version import APP_NAME


class SettingsPage(QWidget):

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.pending_update = None
        self.check_worker = None
        self.apply_worker = None

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
                APP_NAME,
            ),
            (
                "نسخه",
                current_version_label(),
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

        update_card = QFrame()
        update_card.setObjectName(
            "panelCard"
        )
        update_layout = QVBoxLayout(
            update_card
        )
        update_layout.setSpacing(
            10
        )

        update_title = QLabel(
            "به‌روزرسانی نرم‌افزار"
        )
        update_title.setObjectName(
            "panelTitle"
        )
        self.update_status_label = QLabel(
            "می‌توانید آخرین نسخه را مستقیماً از GitHub "
            "بررسی و دریافت کنید."
        )
        self.update_status_label.setObjectName(
            "pageSubtitle"
        )
        self.update_status_label.setWordWrap(
            True
        )

        buttons_layout = QHBoxLayout()
        self.check_update_btn = QPushButton(
            "بررسی به‌روزرسانی"
        )
        self.check_update_btn.clicked.connect(
            self.start_update_check
        )
        self.apply_update_btn = QPushButton(
            "دریافت و نصب نسخه جدید"
        )
        self.apply_update_btn.setObjectName(
            "quickGreen"
        )
        self.apply_update_btn.setVisible(
            False
        )
        self.apply_update_btn.clicked.connect(
            self.start_update_apply
        )
        self.open_release_btn = QPushButton(
            "مشاهده در GitHub"
        )
        self.open_release_btn.setObjectName(
            "sectionButton"
        )
        self.open_release_btn.clicked.connect(
            self.open_release_in_browser
        )

        buttons_layout.addWidget(
            self.check_update_btn
        )
        buttons_layout.addWidget(
            self.apply_update_btn
        )
        buttons_layout.addWidget(
            self.open_release_btn
        )
        buttons_layout.addStretch()

        update_layout.addWidget(
            update_title
        )
        update_layout.addWidget(
            self.update_status_label
        )
        update_layout.addLayout(
            buttons_layout
        )
        layout.addWidget(
            update_card
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

    def set_update_busy(
        self,
        busy
    ):
        self.check_update_btn.setEnabled(
            not busy
        )
        self.apply_update_btn.setEnabled(
            not busy
        )
        self.open_release_btn.setEnabled(
            not busy
        )

    def start_update_check(self):
        if self.check_worker and self.check_worker.isRunning():
            return

        self.pending_update = None
        self.apply_update_btn.setVisible(
            False
        )
        self.update_status_label.setText(
            "در حال بررسی آخرین نسخه در GitHub..."
        )
        self.set_update_busy(
            True
        )

        self.check_worker = UpdateCheckWorker()
        self.check_worker.finished.connect(
            self.on_update_checked
        )
        self.check_worker.start()

    def on_update_checked(
        self,
        success,
        message,
        update_info
    ):
        self.set_update_busy(
            False
        )
        self.pending_update = update_info
        self.update_status_label.setText(
            message
        )

        if update_info:
            self.apply_update_btn.setVisible(
                True
            )

            if update_info.release_notes:
                notes_preview = (
                    update_info.release_notes[:400]
                )
                if len(
                    update_info.release_notes
                ) > 400:
                    notes_preview += "..."

                self.update_status_label.setText(
                    f"{message}\n\n"
                    f"یادداشت نسخه:\n"
                    f"{notes_preview}"
                )

            QMessageBox.information(
                self,
                "به‌روزرسانی موجود است",
                message,
            )
            return

        if success:
            QMessageBox.information(
                self,
                "بررسی به‌روزرسانی",
                message,
            )
        else:
            QMessageBox.warning(
                self,
                "خطا در بررسی به‌روزرسانی",
                message,
            )

    def start_update_apply(self):
        if not self.pending_update:
            return

        if self.apply_worker and self.apply_worker.isRunning():
            return

        confirm = QMessageBox.question(
            self,
            "دریافت نسخه جدید",
            (
                "آیا مایلید آخرین نسخه از GitHub "
                "دریافت و نصب شود؟"
            ),
        )

        if confirm != QMessageBox.StandardButton.Yes:
            return

        self.update_status_label.setText(
            "در حال دریافت نسخه جدید..."
        )
        self.set_update_busy(
            True
        )

        self.apply_worker = UpdateApplyWorker(
            self.pending_update
        )
        self.apply_worker.finished.connect(
            self.on_update_applied
        )
        self.apply_worker.start()

    def on_update_applied(
        self,
        success,
        message
    ):
        self.set_update_busy(
            False
        )
        self.update_status_label.setText(
            message
        )

        if success:
            QMessageBox.information(
                self,
                "به‌روزرسانی",
                message,
            )

            if "نصب‌کننده" in message:
                self.main_window.close()
        else:
            QMessageBox.warning(
                self,
                "خطا در به‌روزرسانی",
                message,
            )

    def open_release_in_browser(self):
        success, message = open_release_page(
            self.pending_update
        )

        if not success:
            QMessageBox.warning(
                self,
                "خطا",
                message,
            )

    def logout(self):
        self.main_window.current_user = None
        self.main_window.show_login()
