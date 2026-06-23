from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from services.format_utils import format_value
from services.inventory_service import get_report_data


class ReportsPage(QWidget):

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
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
            "گزارشات موجودی"
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

        actions_layout = QHBoxLayout()

        refresh_btn = QPushButton(
            "به‌روزرسانی گزارش"
        )
        refresh_btn.clicked.connect(
            self.refresh_data
        )

        actions_layout.addWidget(
            refresh_btn
        )
        actions_layout.addStretch()
        layout.addLayout(
            actions_layout
        )

        self.summary_label = QLabel()
        self.summary_label.setObjectName(
            "welcomeInfo"
        )
        self.summary_label.setAlignment(
            Qt.AlignCenter
        )
        self.summary_label.setWordWrap(
            True
        )
        layout.addWidget(
            self.summary_label
        )

        low_stock_title = QLabel(
            "کالاهای زیر حداقل موجودی"
        )
        low_stock_title.setObjectName(
            "welcomeTitle"
        )
        layout.addWidget(
            low_stock_title
        )

        self.low_stock_table = QTableWidget()
        self.low_stock_table.setColumnCount(
            7
        )
        self.low_stock_table.setHorizontalHeaderLabels([
            "نام کالا",
            "فرم",
            "دسته",
            "واحد",
            "حداقل",
            "موجودی فعلی",
            "کسری",
        ])
        self.low_stock_table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )
        layout.addWidget(
            self.low_stock_table
        )

        self.setLayout(
            layout
        )

        self.refresh_data()

    def refresh_data(self):
        report = get_report_data(
            self.main_window.current_user
        )

        self.summary_label.setText(
            " | ".join([
                f"تعداد اقلام: {report['total_items']}",
                f"جمع موجودی: {format_value(report['total_stock'])}",
                f"اقلام زیر حداقل: {report['low_stock_count']}",
            ])
        )

        rows = report["low_stock_rows"]
        self.low_stock_table.setRowCount(
            len(rows)
        )

        for row_index, row in enumerate(rows):
            shortage = (
                row["minimum_stock"]
                - row["current_stock"]
            )
            values = [
                row["item_name"],
                row["item_form"],
                row["category_name"],
                row["unit"],
                row["minimum_stock"],
                row["current_stock"],
                shortage,
            ]

            for column_index, value in enumerate(values):
                item = QTableWidgetItem(
                    format_value(value)
                )
                if column_index >= 4:
                    item.setTextAlignment(
                        Qt.AlignCenter
                    )
                self.low_stock_table.setItem(
                    row_index,
                    column_index,
                    item
                )

        self.low_stock_table.resizeColumnsToContents()

