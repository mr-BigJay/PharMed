from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from models.stock_request import StockRequest
from services.db_session import SessionLocal
from services.inventory_service import (
    get_report_data,
    list_recent_transactions,
)
from services.user_service import get_user_capacity


class DashboardPage(QWidget):

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.db = SessionLocal()

        self.setup_ui()

    def setup_ui(self):
        root_layout = QHBoxLayout()
        root_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )
        root_layout.setSpacing(
            0
        )

        root_layout.addWidget(
            self.build_sidebar()
        )
        root_layout.addWidget(
            self.build_content(),
            stretch=1
        )

        self.setLayout(
            root_layout
        )

    def build_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName(
            "sidebar"
        )
        sidebar.setFixedWidth(
            230
        )

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(
            18,
            24,
            18,
            24
        )
        layout.setSpacing(
            12
        )

        title = QLabel(
            "مدیریت انبار دارو\nو اقلام پزشکی"
        )
        title.setObjectName(
            "sidebarTitle"
        )
        title.setAlignment(
            Qt.AlignCenter
        )
        layout.addWidget(
            title
        )

        nav_items = [
            ("داشبورد", self.main_window.show_dashboard),
            ("مدیریت اقلام", self.main_window.show_inventory),
            ("ورود کالا", self.main_window.show_inventory),
            ("خروج کالا", self.main_window.show_inventory),
            ("انتقال / درخواست کالا", self.main_window.show_requests),
            ("تجهیزات پزشکی", self.main_window.show_equipment),
            ("گزارشات", self.main_window.show_reports),
        ]

        if self.main_window.current_user and self.main_window.current_user.is_manager:
            nav_items.append(
                ("کاربران", self.main_window.show_users)
            )

        for title, callback in nav_items:
            button = QPushButton(
                title
            )
            button.setObjectName(
                "sidebarButton"
            )
            button.clicked.connect(
                callback
            )
            layout.addWidget(
                button
            )

        layout.addStretch()

        logout_btn = QPushButton(
            "خروج"
        )
        logout_btn.setObjectName(
            "logoutButton"
        )
        logout_btn.clicked.connect(
            self.logout
        )
        layout.addWidget(
            logout_btn
        )

        return sidebar

    def build_content(self):
        user = self.main_window.current_user
        report = get_report_data(
            user
        )
        transactions = list_recent_transactions(
            user,
            limit=6
        )
        pending_requests = self.count_pending_requests()
        capacity = get_user_capacity(
            user
        )

        content = QWidget()
        main_layout = QVBoxLayout(content)
        main_layout.setContentsMargins(
            28,
            24,
            28,
            24
        )
        main_layout.setSpacing(
            18
        )

        main_layout.addWidget(
            self.build_header()
        )

        stats_grid = QGridLayout()
        stats_grid.setHorizontalSpacing(
            12
        )
        stats_grid.setVerticalSpacing(
            12
        )
        stat_cards = [
            (
                "کل اقلام موجود",
                _format_value(report["total_items"]),
                "قلم",
                "blueStat",
            ),
            (
                "موجودی کل",
                _format_value(report["total_stock"]),
                "عدد/واحد",
                "greenStat",
            ),
            (
                "ورود امروز",
                _format_value(self.sum_today_transactions("in")),
                "قلم",
                "purpleStat",
            ),
            (
                "خروج امروز",
                _format_value(self.sum_today_transactions("out")),
                "قلم",
                "orangeStat",
            ),
            (
                "اقلام کم موجودی",
                _format_value(report["low_stock_count"]),
                "نیاز به پیگیری",
                "redStat",
            ),
        ]

        for index, (title, value, subtitle, object_name) in enumerate(stat_cards):
            stats_grid.addWidget(
                self.build_stat_card(
                    title,
                    value,
                    subtitle,
                    object_name
                ),
                index // 5,
                index % 5
            )

        main_layout.addLayout(
            stats_grid
        )

        middle_layout = QHBoxLayout()
        middle_layout.setSpacing(
            12
        )
        middle_layout.addWidget(
            self.build_low_stock_panel(
                report["low_stock_rows"]
            ),
            stretch=1
        )
        middle_layout.addWidget(
            self.build_quick_actions(
                pending_requests,
                capacity
            ),
            stretch=1
        )
        main_layout.addLayout(
            middle_layout
        )

        main_layout.addWidget(
            self.build_transactions_panel(
                transactions
            )
        )

        scroll = QScrollArea()
        scroll.setWidgetResizable(
            True
        )
        scroll.setFrameShape(
            QFrame.NoFrame
        )
        scroll.setWidget(
            content
        )

        return scroll

    def build_header(self):
        user = self.main_window.current_user
        full_name = (
            user.full_name
            if user
            else "کاربر"
        )
        role_text = (
            "مدیر واحد"
            if user and user.is_manager
            else "کاربر واحد"
        )

        header = QFrame()
        header.setObjectName(
            "dashboardHeader"
        )
        layout = QHBoxLayout(header)

        welcome = QLabel(
            f"خوش آمدید، {full_name}"
        )
        welcome.setObjectName(
            "dashboardWelcome"
        )

        role_label = QLabel(
            role_text
        )
        role_label.setObjectName(
            "dashboardRole"
        )

        today = datetime.now().strftime(
            "%Y/%m/%d - %H:%M"
        )
        date_label = QLabel(
            today
        )
        date_label.setObjectName(
            "dashboardDate"
        )

        layout.addWidget(
            welcome
        )
        layout.addWidget(
            role_label
        )
        layout.addStretch()
        layout.addWidget(
            date_label
        )

        return header

    def build_stat_card(
        self,
        title,
        value,
        subtitle,
        object_name
    ):
        card = QFrame()
        card.setObjectName(
            object_name
        )
        card.setMinimumHeight(
            110
        )

        layout = QVBoxLayout(card)
        layout.setSpacing(
            6
        )

        title_label = QLabel(
            title
        )
        title_label.setObjectName(
            "statTitle"
        )
        value_label = QLabel(
            value
        )
        value_label.setObjectName(
            "statValue"
        )
        subtitle_label = QLabel(
            subtitle
        )
        subtitle_label.setObjectName(
            "statSubtitle"
        )

        layout.addWidget(
            title_label
        )
        layout.addWidget(
            value_label
        )
        layout.addWidget(
            subtitle_label
        )

        return card

    def build_low_stock_panel(
        self,
        rows
    ):
        panel = QFrame()
        panel.setObjectName(
            "dashboardPanel"
        )
        layout = QVBoxLayout(panel)

        title = QLabel(
            "اقلام کم موجودی"
        )
        title.setObjectName(
            "panelTitle"
        )
        layout.addWidget(
            title
        )

        table = QTableWidget()
        table.setColumnCount(
            4
        )
        table.setHorizontalHeaderLabels([
            "قلم",
            "حداقل",
            "موجودی",
            "کسری",
        ])
        table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )
        table.setRowCount(
            min(
                len(rows),
                6
            )
        )

        for row_index, row in enumerate(rows[:6]):
            shortage = row["minimum_stock"] - row["current_stock"]
            values = [
                row["item_name"],
                row["minimum_stock"],
                row["current_stock"],
                shortage,
            ]
            for column_index, value in enumerate(values):
                item = QTableWidgetItem(
                    _format_value(value)
                )
                item.setTextAlignment(
                    Qt.AlignCenter
                )
                table.setItem(
                    row_index,
                    column_index,
                    item
                )

        table.resizeColumnsToContents()
        layout.addWidget(
            table
        )

        return panel

    def build_quick_actions(
        self,
        pending_requests,
        capacity
    ):
        panel = QFrame()
        panel.setObjectName(
            "dashboardPanel"
        )
        layout = QVBoxLayout(panel)

        title = QLabel(
            "عملیات سریع"
        )
        title.setObjectName(
            "panelTitle"
        )
        layout.addWidget(
            title
        )

        actions_grid = QGridLayout()
        actions = [
            ("ورود کالا", self.main_window.show_inventory),
            ("خروج کالا", self.main_window.show_inventory),
            ("ثبت درخواست", self.main_window.show_requests),
            ("گزارشات", self.main_window.show_reports),
        ]

        if self.main_window.current_user and self.main_window.current_user.is_manager:
            actions.append(
                ("ایجاد کاربر", self.main_window.show_users)
            )

        for index, (title, callback) in enumerate(actions):
            button = QPushButton(
                title
            )
            button.setObjectName(
                "quickActionButton"
            )
            button.clicked.connect(
                callback
            )
            actions_grid.addWidget(
                button,
                index // 2,
                index % 2
            )

        layout.addLayout(
            actions_grid
        )

        info = QLabel(
            (
                f"درخواست‌های در انتظار: {pending_requests}\n"
                f"کاربران واحد: {capacity['registered']} از {capacity['max_users']}"
            )
        )
        info.setObjectName(
            "panelInfo"
        )
        info.setAlignment(
            Qt.AlignCenter
        )
        layout.addWidget(
            info
        )

        return panel

    def build_transactions_panel(
        self,
        transactions
    ):
        panel = QFrame()
        panel.setObjectName(
            "dashboardPanel"
        )
        layout = QVBoxLayout(panel)

        title = QLabel(
            "آخرین ورود و خروج کالا"
        )
        title.setObjectName(
            "panelTitle"
        )
        layout.addWidget(
            title
        )

        table = QTableWidget()
        table.setColumnCount(
            5
        )
        table.setHorizontalHeaderLabels([
            "تاریخ",
            "قلم",
            "نوع",
            "تعداد",
            "توضیحات",
        ])
        table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )
        table.setRowCount(
            len(transactions)
        )

        for row_index, transaction in enumerate(transactions):
            values = [
                transaction["date"],
                transaction["item_name"],
                transaction["transaction_label"],
                transaction["quantity"],
                transaction["description"],
            ]
            for column_index, value in enumerate(values):
                table.setItem(
                    row_index,
                    column_index,
                    QTableWidgetItem(
                        _format_value(value)
                    )
                )

        table.resizeColumnsToContents()
        layout.addWidget(
            table
        )

        return panel

    def count_pending_requests(self):
        user = self.main_window.current_user

        if not user:
            return 0

        query = self.db.query(StockRequest).filter(
            StockRequest.status == "pending"
        )

        if user.health_house_id:
            query = query.filter(
                StockRequest.health_house_id == user.health_house_id
            )
        elif user.center_id:
            query = query.filter(
                StockRequest.center_id == user.center_id,
                StockRequest.health_house_id.is_(None)
            )
        else:
            query = query.filter(
                StockRequest.user_id == user.id
            )

        return query.count()

    def sum_today_transactions(
        self,
        transaction_type
    ):
        today = datetime.now().date()
        total = 0

        for transaction in list_recent_transactions(
            self.main_window.current_user,
            limit=200
        ):
            if (
                transaction["transaction_type"] == transaction_type
                and transaction["date"] == today
            ):
                total += transaction["quantity"]

        return total

    def logout(self):
        self.main_window.current_user = None
        self.main_window.show_login()


def _format_value(value):
    if value is None:
        return ""

    if isinstance(value, float):
        if value.is_integer():
            return str(
                int(value)
            )
        return f"{value:.2f}"

    return str(
        value
    )
