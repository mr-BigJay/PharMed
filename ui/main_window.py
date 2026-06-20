from PySide6.QtWidgets import (
    QMainWindow,
    QStackedWidget
)

from db import init_db

from ui.login_window import LoginWindow
from ui.register_window import RegisterWindow
from ui.dashboard_page import DashboardPage

from ui.inventory_page import InventoryPage
from ui.equipment_page import EquipmentPage
from ui.requests_page import RequestsPage
from ui.users_page import UsersPage
from ui.reports_page import ReportsPage


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.current_user = None

        self.setWindowTitle(
            "PharMed"
        )

        self.resize(
            1180,
            760
        )

        self.setMinimumSize(
            1050,
            700
        )

        init_db()

        self.stack = QStackedWidget()

        self.login_page = LoginWindow(
            self
        )

        self.register_page = RegisterWindow(
            self
        )

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

        self.stack.addWidget(
            self.login_page
        )

        self.stack.addWidget(
            self.register_page
        )

        self.stack.addWidget(
            self.dashboard_page
        )

        self.stack.addWidget(
            self.inventory_page
        )

        self.stack.addWidget(
            self.equipment_page
        )

        self.stack.addWidget(
            self.requests_page
        )

        self.stack.addWidget(
            self.users_page
        )

        self.stack.addWidget(
            self.reports_page
        )

        self.setCentralWidget(
            self.stack
        )

        self.show_login()

    def show_login(self):

        self.stack.setCurrentWidget(
            self.login_page
        )

    def show_register(self):

        self.stack.setCurrentWidget(
            self.register_page
        )

    def show_dashboard(self):

        self.stack.removeWidget(
            self.dashboard_page
        )

        self.dashboard_page.deleteLater()

        self.dashboard_page = DashboardPage(
            self
        )

        self.stack.addWidget(
            self.dashboard_page
        )

        self.stack.setCurrentWidget(
            self.dashboard_page
        )

    def show_inventory(self):

        if hasattr(
            self.inventory_page,
            "refresh_data"
        ):
            self.inventory_page.refresh_data()

        self.stack.setCurrentWidget(
            self.inventory_page
        )

    def show_equipment(self):

        if hasattr(
            self.equipment_page,
            "refresh_data"
        ):
            self.equipment_page.refresh_data()

        self.stack.setCurrentWidget(
            self.equipment_page
        )

    def show_requests(self):

        if hasattr(
            self.requests_page,
            "refresh_data"
        ):
            self.requests_page.refresh_data()

        self.stack.setCurrentWidget(
            self.requests_page
        )

    def show_users(self):

        if hasattr(
            self.users_page,
            "refresh_data"
        ):
            self.users_page.refresh_data()

        self.stack.setCurrentWidget(
            self.users_page
        )

    def show_reports(self):

        if hasattr(
            self.reports_page,
            "refresh_data"
        ):
            self.reports_page.refresh_data()

        self.stack.setCurrentWidget(
            self.reports_page
        )
