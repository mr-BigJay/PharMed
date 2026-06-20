from PySide6.QtWidgets import (
    QMainWindow,
    QStackedWidget
)

from db import engine

from models.base import Base
from models.user import User
from models.center import Center
from models.health_house import HealthHouse
from models.category import Category
from models.item import Item

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
            900,
            700
        )

        self.setMinimumSize(
            850,
            650
        )

        Base.metadata.create_all(
            bind=engine
        )

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

        self.stack.setCurrentWidget(
            self.inventory_page
        )

    def show_equipment(self):

        self.stack.setCurrentWidget(
            self.equipment_page
        )

    def show_requests(self):

        self.stack.setCurrentWidget(
            self.requests_page
        )

    def show_users(self):

        self.stack.setCurrentWidget(
            self.users_page
        )

    def show_reports(self):

        self.stack.setCurrentWidget(
            self.reports_page
        )