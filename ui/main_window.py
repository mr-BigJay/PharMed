from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from db import init_db

from models.center import Center
from models.health_house import HealthHouse
from services.db_session import SessionLocal
from services.expiry_service import (
    get_expiring_medicines,
    get_expiry_alert_count,
)
from services.format_utils import format_value

from ui.dashboard_page import DashboardPage
from ui.equipment_page import EquipmentPage
from ui.inventory_page import InventoryPage
from ui.login_window import LoginWindow
from ui.register_window import RegisterWindow
from ui.reports_page import ReportsPage
from ui.requests_page import RequestsPage
from ui.settings_page import SettingsPage
from ui.users_page import UsersPage


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.current_user = None

        self.setWindowTitle(
            "PharMed"
        )
        self.setLayoutDirection(
            Qt.RightToLeft
        )
        self.resize(
            1366,
            820
        )
        self.setMinimumSize(
            1180,
            740
        )

        init_db()

        self.root_stack = QStackedWidget()
        self.login_page = LoginWindow(
            self
        )
        self.register_page = RegisterWindow(
            self
        )

        self.content_stack = QStackedWidget()
        self.dashboard_page = DashboardPage(
            self
        )
        self.inventory_page = InventoryPage(
            self
        )
        self.equipment_page = EquipmentPage(
            self
        )
        self.requests_page = RequestsPage(
            self
        )
        self.users_page = UsersPage(
            self
        )
        self.reports_page = ReportsPage(
            self
        )
        self.settings_page = SettingsPage(
            self
        )

        for page in (
            self.dashboard_page,
            self.inventory_page,
            self.equipment_page,
            self.requests_page,
            self.users_page,
            self.reports_page,
            self.settings_page,
        ):
            self.content_stack.addWidget(
                page
            )

        self.nav_buttons = {}
        self.user_name_label = QLabel()
        self.user_status_label = QLabel()
        self.user_location_label = QLabel()
        self.expiry_bell_button = QPushButton()
        self.db = SessionLocal()
        self.app_shell = self.build_app_shell()

        self.root_stack.addWidget(
            self.login_page
        )
        self.root_stack.addWidget(
            self.register_page
        )
        self.root_stack.addWidget(
            self.app_shell
        )

        self.setCentralWidget(
            self.root_stack
        )
        self.show_login()

    def build_app_shell(self):
        shell = QWidget()
        shell.setObjectName(
            "appShell"
        )
        layout = QHBoxLayout(shell)
        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )
        layout.setSpacing(
            0
        )

        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )
        content_layout.setSpacing(
            0
        )
        content_layout.addWidget(
            self.build_topbar()
        )
        content_layout.addWidget(
            self.content_stack,
            stretch=1
        )

        layout.addWidget(
            content_area,
            stretch=1
        )
        layout.addWidget(
            self.build_sidebar()
        )

        return shell

    def build_topbar(self):
        topbar = QFrame()
        topbar.setObjectName(
            "topBar"
        )
        topbar.setFixedHeight(
            72
        )
        layout = QHBoxLayout(topbar)
        layout.setContentsMargins(
            22,
            12,
            22,
            12
        )
        layout.setSpacing(
            16
        )

        self.expiry_bell_button.setObjectName(
            "expiryBellButton"
        )
        self.expiry_bell_button.setCursor(
            Qt.PointingHandCursor
        )
        self.expiry_bell_button.clicked.connect(
            self.show_expiry_alerts
        )

        user_box = QWidget()
        user_layout = QVBoxLayout(user_box)
        user_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )
        user_layout.setSpacing(
            2
        )
        self.user_name_label.setObjectName(
            "topUserName"
        )
        self.user_status_label.setObjectName(
            "topUserStatus"
        )
        self.user_location_label.setObjectName(
            "topUserLocation"
        )
        user_layout.addWidget(
            self.user_name_label
        )
        user_layout.addWidget(
            self.user_status_label
        )
        user_layout.addWidget(
            self.user_location_label
        )

        avatar = QLabel(
            "👤"
        )
        avatar.setObjectName(
            "avatar"
        )

        layout.addWidget(
            self.expiry_bell_button
        )
        layout.addStretch()
        layout.addWidget(
            user_box
        )
        layout.addWidget(
            avatar
        )

        return topbar

    def build_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName(
            "appSidebar"
        )
        sidebar.setFixedWidth(
            245
        )
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(
            14,
            18,
            14,
            18
        )
        layout.setSpacing(
            8
        )

        brand_icon = QLabel(
            "✚"
        )
        brand_icon.setObjectName(
            "brandIcon"
        )
        brand_title = QLabel(
            "مدیریت انبار دارو\nو اقلام پزشکی"
        )
        brand_title.setObjectName(
            "brandTitle"
        )
        brand_title.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            brand_icon,
            alignment=Qt.AlignCenter
        )
        layout.addWidget(
            brand_title
        )
        layout.addSpacing(
            10
        )

        nav_items = [
            ("dashboard", "🏠  داشبورد", self.show_dashboard),
            ("items", "📦  اقلام", self.show_items),
            ("stock_in", "⬇  ورود انبار", self.show_stock_in),
            ("stock_out", "⬆  خروج انبار", self.show_stock_out),
            ("requests", "🔁  درخواست", self.show_requests),
            ("stock", "🏬  موجودی انبار", self.show_stock_balance),
            ("equipment", "🏥  تجهیزات پزشکی", self.show_equipment),
            ("reports", "📊  گزارشات", self.show_reports),
            ("users", "👥  کاربران", self.show_users),
            ("settings", "⚙  تنظیمات", self.show_settings),
        ]

        for key, title, callback in nav_items:
            button = QPushButton(
                title
            )
            button.setObjectName(
                "navButton"
            )
            button.setProperty(
                "navKey",
                key
            )
            button.clicked.connect(
                callback
            )
            self.nav_buttons[key] = button
            layout.addWidget(
                button
            )

        layout.addStretch()

        footer = QLabel(
            "PharMed v0.1\nشبکه بهداشت و درمان شهرستان"
        )
        footer.setObjectName(
            "sidebarFooter"
        )
        footer.setAlignment(
            Qt.AlignCenter
        )
        layout.addWidget(
            footer
        )

        return sidebar

    def update_topbar(self):
        user = self.current_user

        if user:
            self.user_name_label.setText(
                user.full_name
            )
            self.user_status_label.setText(
                "مدیر واحد"
                if user.is_manager
                else "کاربر"
            )
            self.user_location_label.setText(
                self._get_user_location_text(user)
            )
        else:
            self.user_name_label.setText(
                "کاربر"
            )
            self.user_status_label.setText(
                ""
            )
            self.user_location_label.setText(
                ""
            )

        self._update_expiry_bell()

    def _get_user_location_text(self, user) -> str:
        if user.health_house_id:
            house = (
                self.db.query(HealthHouse)
                .filter(
                    HealthHouse.id == user.health_house_id
                )
                .first()
            )
            if house:
                return f"خانه بهداشت: {house.name}"

        if user.center_id:
            center = (
                self.db.query(Center)
                .filter(
                    Center.id == user.center_id
                )
                .first()
            )
            if center:
                return f"مرکز درمانی: {center.name}"

        return ""

    def _update_expiry_bell(self):
        count = get_expiry_alert_count(
            self.db,
            self.current_user
        )

        if count > 0:
            self.expiry_bell_button.setText(
                f"🔔 {format_value(count)}"
            )
            self.expiry_bell_button.setToolTip(
                f"{format_value(count)} داروی منقضی یا نزدیک به انقضا"
            )
        else:
            self.expiry_bell_button.setText(
                "🔔"
            )
            self.expiry_bell_button.setToolTip(
                "هیچ داروی منقضی یا نزدیک به انقضا وجود ندارد"
            )

    def show_expiry_alerts(self):
        medicines = get_expiring_medicines(
            self.db,
            self.current_user
        )

        if not medicines:
            QMessageBox.information(
                self,
                "هشدار انقضای دارو",
                "هیچ داروی منقضی شده یا نزدیک به انقضایی یافت نشد.",
            )
            return

        lines = []
        for medicine in medicines:
            lines.append(
                f"• {medicine['item_name']} "
                f"(بچ: {medicine['batch_number']}) — "
                f"{medicine['status_label']} — "
                f"انقضا: {format_value(medicine['expiry_date'])}"
            )

        QMessageBox.warning(
            self,
            "هشدار انقضای دارو",
            "\n".join(lines),
        )

    def show_login(self):
        self.root_stack.setCurrentWidget(
            self.login_page
        )

    def show_register(self):
        self.root_stack.setCurrentWidget(
            self.register_page
        )

    def show_app_page(
        self,
        page,
        nav_key=None
    ):
        self.update_topbar()
        self.set_active_nav(
            nav_key
        )
        self.root_stack.setCurrentWidget(
            self.app_shell
        )
        self.content_stack.setCurrentWidget(
            page
        )

    def show_dashboard(self):
        self.content_stack.removeWidget(
            self.dashboard_page
        )
        self.dashboard_page.deleteLater()
        self.dashboard_page = DashboardPage(
            self
        )
        self.content_stack.insertWidget(
            0,
            self.dashboard_page
        )
        self.show_app_page(
            self.dashboard_page,
            "dashboard"
        )

    def show_items(self):
        if hasattr(
            self.inventory_page,
            "set_mode"
        ):
            self.inventory_page.set_mode(
                "items"
            )

        self.show_inventory(
            "items"
        )

    def show_stock_in(self):
        if hasattr(
            self.inventory_page,
            "set_mode"
        ):
            self.inventory_page.set_mode(
                "stock_in"
            )

        self.show_inventory(
            "stock_in"
        )

    def show_stock_out(self):
        if hasattr(
            self.inventory_page,
            "set_mode"
        ):
            self.inventory_page.set_mode(
                "stock_out"
            )

        self.show_inventory(
            "stock_out"
        )

    def show_stock_balance(self):
        if hasattr(
            self.inventory_page,
            "set_mode"
        ):
            self.inventory_page.set_mode(
                "stock"
            )

        self.show_inventory(
            "stock"
        )

    def show_inventory(
        self,
        nav_key="items"
    ):
        if hasattr(
            self.inventory_page,
            "refresh_data"
        ):
            self.inventory_page.refresh_data()

        self.show_app_page(
            self.inventory_page,
            nav_key
        )

    def show_equipment(self):
        if hasattr(
            self.equipment_page,
            "refresh_data"
        ):
            self.equipment_page.refresh_data()

        self.show_app_page(
            self.equipment_page,
            "equipment"
        )

    def show_requests(self):
        if hasattr(
            self.requests_page,
            "refresh_data"
        ):
            self.requests_page.refresh_data()

        self.show_app_page(
            self.requests_page,
            "requests"
        )

    def show_users(self):
        if hasattr(
            self.users_page,
            "refresh_data"
        ):
            self.users_page.refresh_data()

        self.show_app_page(
            self.users_page,
            "users"
        )

    def show_reports(self):
        if hasattr(
            self.reports_page,
            "refresh_data"
        ):
            self.reports_page.refresh_data()

        self.show_app_page(
            self.reports_page,
            "reports"
        )

    def show_settings(self):
        self.show_app_page(
            self.settings_page,
            "settings"
        )

    def set_active_nav(
        self,
        active_key
    ):
        for key, button in self.nav_buttons.items():
            button.setProperty(
                "active",
                key == active_key
            )
            button.style().unpolish(
                button
            )
            button.style().polish(
                button
            )
