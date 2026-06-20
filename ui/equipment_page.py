from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from services.inventory_service import list_inventory


class EquipmentPage(QWidget):

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.rows = []
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
            "تجهیزات پزشکی"
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

        tools_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "جستجوی تجهیزات"
        )
        self.search_input.returnPressed.connect(
            self.refresh_data
        )

        refresh_btn = QPushButton(
            "به‌روزرسانی"
        )
        refresh_btn.clicked.connect(
            self.refresh_data
        )

        back_btn = QPushButton(
            "بازگشت به داشبورد"
        )
        back_btn.clicked.connect(
            self.main_window.show_dashboard
        )

        tools_layout.addWidget(
            self.search_input
        )
        tools_layout.addWidget(
            refresh_btn
        )
        tools_layout.addWidget(
            back_btn
        )
        layout.addLayout(
            tools_layout
        )

        self.table = QTableWidget()
        self.table.setColumnCount(
            7
        )
        self.table.setHorizontalHeaderLabels([
            "نام تجهیز",
            "فرم",
            "واحد",
            "حداقل",
            "موجودی اولیه",
            "موجودی فعلی",
            "وضعیت",
        ])
        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )
        layout.addWidget(
            self.table
        )

        self.setLayout(
            layout
        )
        self.refresh_data()

    def refresh_data(self):
        self.rows = [
            row
            for row in list_inventory(
                self.main_window.current_user,
                self.search_input.text()
            )
            if row["category_name"] == "تجهیزات پزشکی"
        ]
        self.table.setRowCount(
            len(self.rows)
        )

        for row_index, row in enumerate(self.rows):
            values = [
                row["item_name"],
                row["item_form"],
                row["unit"],
                row["minimum_stock"],
                row["opening_quantity"],
                row["current_stock"],
                row["status"],
            ]

            for column_index, value in enumerate(values):
                item = QTableWidgetItem(
                    _format_value(value)
                )
                if column_index >= 3:
                    item.setTextAlignment(
                        Qt.AlignCenter
                    )
                self.table.setItem(
                    row_index,
                    column_index,
                    item
                )

        self.table.resizeColumnsToContents()


def _format_value(value):
    if isinstance(value, float):
        if value.is_integer():
            return str(
                int(value)
            )
        return f"{value:.2f}"

    return str(
        value
    )
