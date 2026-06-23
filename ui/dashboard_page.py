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
from services.format_utils import format_value
from services.user_service import get_user_capacity


class DashboardPage(QWidget):

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.db = SessionLocal()

        self.setup_ui()

    def setup_ui(self):
        scroll = QScrollArea()
        scroll.setObjectName(
            "pageScroll"
        )
        scroll.setWidgetResizable(
            True
        )
        scroll.setFrameShape(
            QFrame.NoFrame
        )

        content = QWidget()
        content.setObjectName(
            "pageCanvas"
        )
        layout = QVBoxLayout(content)
        layout.setContentsMargins(
            22,
            18,
            22,
            22
        )
        layout.setSpacing(
            16
        )

        layout.addWidget(
            self.build_welcome_bar()
        )
        layout.addLayout(
            self.build_metrics_grid()
        )
        layout.addLayout(
            self.build_middle_grid()
        )
        layout.addLayout(
            self.build_bottom_grid()
        )

        scroll.setWidget(
            content
        )

        root_layout = QVBoxLayout()
        root_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )
        root_layout.addWidget(
            scroll
        )
        self.setLayout(
            root_layout
        )

    def build_welcome_bar(self):
        user = self.main_window.current_user
        name = (
            user.full_name
            if user
            else "کاربر"
        )
        title = QLabel(
            f"👋 خوش آمدید، {name}"
        )
        title.setObjectName(
            "heroTitle"
        )
        subtitle = QLabel(
            "نمای کلی وضعیت انبار، موجودی‌ها و درخواست‌های واحد شما"
        )
        subtitle.setObjectName(
            "heroSubtitle"
        )

        date_card = QFrame()
        date_card.setObjectName(
            "dateCard"
        )
        date_layout = QVBoxLayout(date_card)
        date_layout.setSpacing(
            2
        )
        date_layout.addWidget(
            QLabel(
                "امروز"
            )
        )
        date_value = QLabel(
            format_value(
                datetime.now().date()
            )
        )
        date_value.setObjectName(
            "dateValue"
        )
        date_layout.addWidget(
            date_value
        )

        hero = QFrame()
        hero.setObjectName(
            "heroCard"
        )
        hero_layout = QHBoxLayout(hero)
        text_layout = QVBoxLayout()
        text_layout.addWidget(
            title
        )
        text_layout.addWidget(
            subtitle
        )
        hero_layout.addLayout(
            text_layout,
            stretch=1
        )
        hero_layout.addWidget(
            date_card
        )

        return hero

    def build_metrics_grid(self):
        report = get_report_data(
            self.main_window.current_user
        )
        pending_requests = self.count_pending_requests()

        cards = [
            (
                "کل اقلام موجود",
                format_value(report["total_items"]),
                "قلم",
                "metricBlue",
                "📦",
            ),
            (
                "موجودی کل انبار",
                format_value(report["total_stock"]),
                "عدد/واحد",
                "metricGreen",
                "🟢",
            ),
            (
                "ورود این ماه",
                format_value(self.sum_month_transactions("in")),
                "قلم",
                "metricPurple",
                "⬇",
            ),
            (
                "خروج این ماه",
                format_value(self.sum_month_transactions("out")),
                "قلم",
                "metricOrange",
                "⬆",
            ),
            (
                "اقلام کم موجودی",
                format_value(report["low_stock_count"]),
                "نیاز به پیگیری",
                "metricRed",
                "⚠",
            ),
            (
                "درخواست‌های باز",
                format_value(pending_requests),
                "در انتظار بررسی",
                "metricSky",
                "✉",
            ),
        ]

        grid = QGridLayout()
        grid.setHorizontalSpacing(
            12
        )
        grid.setVerticalSpacing(
            12
        )

        for index, card in enumerate(cards):
            grid.addWidget(
                self.build_metric_card(*card),
                index // 3,
                index % 3
            )

        return grid

    def build_metric_card(
        self,
        title,
        value,
        subtitle,
        object_name,
        icon
    ):
        card = QFrame()
        card.setObjectName(
            object_name
        )
        card.setMinimumHeight(
            116
        )
        layout = QHBoxLayout(card)

        icon_label = QLabel(
            icon
        )
        icon_label.setObjectName(
            "metricIcon"
        )
        text_layout = QVBoxLayout()

        title_label = QLabel(
            title
        )
        title_label.setObjectName(
            "metricTitle"
        )
        value_label = QLabel(
            value
        )
        value_label.setObjectName(
            "metricValue"
        )
        subtitle_label = QLabel(
            subtitle
        )
        subtitle_label.setObjectName(
            "metricSubtitle"
        )

        text_layout.addWidget(
            title_label
        )
        text_layout.addWidget(
            value_label
        )
        text_layout.addWidget(
            subtitle_label
        )

        layout.addWidget(
            icon_label
        )
        layout.addLayout(
            text_layout,
            stretch=1
        )

        return card

    def build_middle_grid(self):
        report = get_report_data(
            self.main_window.current_user
        )

        grid = QHBoxLayout()
        grid.setSpacing(
            14
        )
        grid.addWidget(
            self.build_low_stock_panel(
                report["low_stock_rows"]
            ),
            stretch=1
        )
        grid.addWidget(
            self.build_quick_actions_panel(),
            stretch=1
        )

        return grid

    def build_low_stock_panel(
        self,
        rows
    ):
        panel = QFrame()
        panel.setObjectName(
            "panelCard"
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
                5
            )
        )

        for row_index, row in enumerate(rows[:5]):
            values = [
                row["item_name"],
                row["minimum_stock"],
                row["current_stock"],
                row["minimum_stock"] - row["current_stock"],
            ]
            for column_index, value in enumerate(values):
                item = QTableWidgetItem(
                    format_value(value)
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

    def build_quick_actions_panel(self):
        panel = QFrame()
        panel.setObjectName(
            "panelCard"
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

        grid = QGridLayout()
        actions = [
            ("⬇ ورود کالا", self.main_window.show_stock_in, "quickGreen"),
            ("⬆ خروج کالا", self.main_window.show_stock_out, "quickRed"),
            ("🔁 ثبت درخواست", self.main_window.show_requests, "quickBlue"),
            ("📊 گزارشات", self.main_window.show_reports, "quickOrange"),
            ("⚙ مدیریت اقلام", self.main_window.show_items, "quickPurple"),
            ("👥 کاربران", self.main_window.show_users, "quickGray"),
        ]

        for index, (title, callback, object_name) in enumerate(actions):
            button = QPushButton(
                title
            )
            button.setObjectName(
                object_name
            )
            button.clicked.connect(
                callback
            )
            grid.addWidget(
                button,
                index // 3,
                index % 3
            )

        capacity = get_user_capacity(
            self.main_window.current_user
        )
        info = QLabel(
            f"کاربران واحد: {format_value(capacity['registered'])} از {format_value(capacity['max_users'])}"
        )
        info.setObjectName(
            "panelInfo"
        )
        info.setAlignment(
            Qt.AlignCenter
        )

        layout.addLayout(
            grid
        )
        layout.addWidget(
            info
        )

        return panel

    def build_bottom_grid(self):
        grid = QHBoxLayout()
        grid.setSpacing(
            14
        )
        grid.addWidget(
            self.build_transactions_panel(),
            stretch=2
        )
        grid.addWidget(
            self.build_summary_panel(),
            stretch=1
        )

        return grid

    def build_transactions_panel(self):
        transactions = list_recent_transactions(
            self.main_window.current_user,
            limit=7
        )

        panel = QFrame()
        panel.setObjectName(
            "panelCard"
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
                        format_value(value)
                    )
                )

        table.resizeColumnsToContents()
        layout.addWidget(
            table
        )

        return panel

    def build_summary_panel(self):
        panel = QFrame()
        panel.setObjectName(
            "panelCard"
        )
        layout = QVBoxLayout(panel)

        title = QLabel(
            "خلاصه وضعیت"
        )
        title.setObjectName(
            "panelTitle"
        )
        layout.addWidget(
            title
        )

        rows = [
            ("درخواست‌های باز", self.count_pending_requests()),
            ("ورود این ماه", self.sum_month_transactions("in")),
            ("خروج این ماه", self.sum_month_transactions("out")),
        ]

        for label, value in rows:
            row = QLabel(
                f"{label}: {format_value(value)}"
            )
            row.setObjectName(
                "summaryRow"
            )
            layout.addWidget(
                row
            )

        layout.addStretch()

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

    def sum_month_transactions(
        self,
        transaction_type
    ):
        today = datetime.now().date()
        total = 0

        for transaction in list_recent_transactions(
            self.main_window.current_user,
            limit=500
        ):
            transaction_date = transaction["date"]

            if (
                transaction["transaction_type"] == transaction_type
                and transaction_date.year == today.year
                and transaction_date.month == today.month
            ):
                total += transaction["quantity"]

        return total
