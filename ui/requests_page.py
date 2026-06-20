from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
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

from services.inventory_service import list_inventory
from services.request_service import (
    STATUS_APPROVED,
    STATUS_REJECTED,
    create_request,
    list_requests,
    update_request_status,
)


class RequestsPage(QWidget):

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.requests = []
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
            "درخواست‌های کالا"
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

        form_group = QGroupBox(
            "ثبت درخواست جدید"
        )
        form = QFormLayout(form_group)

        self.item_combo = QComboBox()
        self.quantity_input = QDoubleSpinBox()
        self.quantity_input.setMaximum(
            100000000
        )
        self.quantity_input.setDecimals(
            2
        )
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText(
            "توضیحات اختیاری"
        )

        submit_btn = QPushButton(
            "ثبت درخواست"
        )
        submit_btn.clicked.connect(
            self.submit_request
        )

        form.addRow(
            "کالا:",
            self.item_combo
        )
        form.addRow(
            "تعداد:",
            self.quantity_input
        )
        form.addRow(
            "توضیحات:",
            self.description_input
        )
        form.addRow(
            submit_btn
        )
        layout.addWidget(
            form_group
        )

        actions_layout = QHBoxLayout()
        refresh_btn = QPushButton(
            "به‌روزرسانی"
        )
        refresh_btn.clicked.connect(
            self.refresh_data
        )
        approve_btn = QPushButton(
            "تأیید درخواست"
        )
        approve_btn.clicked.connect(
            lambda: self.change_request_status(STATUS_APPROVED)
        )
        reject_btn = QPushButton(
            "رد درخواست"
        )
        reject_btn.clicked.connect(
            lambda: self.change_request_status(STATUS_REJECTED)
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
            approve_btn
        )
        actions_layout.addWidget(
            reject_btn
        )
        actions_layout.addWidget(
            back_btn
        )
        layout.addLayout(
            actions_layout
        )

        self.table = QTableWidget()
        self.table.setColumnCount(
            8
        )
        self.table.setHorizontalHeaderLabels([
            "شناسه",
            "تاریخ",
            "درخواست‌دهنده",
            "کالا",
            "فرم",
            "تعداد",
            "وضعیت",
            "توضیحات",
        ])
        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )
        self.table.setSelectionBehavior(
            QTableWidget.SelectRows
        )
        layout.addWidget(
            self.table
        )

        self.setLayout(
            layout
        )
        self.refresh_data()

    def refresh_data(self):
        self.load_items()
        self.requests = list_requests(
            self.main_window.current_user
        )
        self.fill_table()

    def load_items(self):
        current_item_id = self.item_combo.currentData()
        self.item_combo.clear()

        for row in list_inventory(
            self.main_window.current_user
        ):
            label = (
                f"{row['item_name']} "
                f"{row['item_form']}"
            ).strip()
            self.item_combo.addItem(
                label,
                row["item_id"]
            )

        if current_item_id:
            index = self.item_combo.findData(
                current_item_id
            )
            if index >= 0:
                self.item_combo.setCurrentIndex(
                    index
                )

    def fill_table(self):
        self.table.setRowCount(
            len(self.requests)
        )

        for row_index, request in enumerate(self.requests):
            values = [
                request["id"],
                request["request_date"],
                request["requester"],
                request["item_name"],
                request["item_form"],
                request["quantity"],
                request["status_label"],
                request["description"],
            ]

            for column_index, value in enumerate(values):
                item = QTableWidgetItem(
                    _format_value(value)
                )
                if column_index in (0, 5, 6):
                    item.setTextAlignment(
                        Qt.AlignCenter
                    )
                self.table.setItem(
                    row_index,
                    column_index,
                    item
                )

        self.table.resizeColumnsToContents()

    def submit_request(self):
        success, message = create_request(
            user=self.main_window.current_user,
            item_id=self.item_combo.currentData(),
            quantity=self.quantity_input.value(),
            description=self.description_input.text()
        )

        self.show_result(
            success,
            message
        )

        if success:
            self.quantity_input.setValue(
                0
            )
            self.description_input.clear()
            self.refresh_data()

    def change_request_status(
        self,
        status
    ):
        selected_items = self.table.selectedItems()

        if not selected_items:
            QMessageBox.warning(
                self,
                "خطا",
                "ابتدا یک درخواست را انتخاب کنید"
            )
            return

        selected_row = selected_items[0].row()
        request_id = self.requests[selected_row]["id"]

        success, message = update_request_status(
            self.main_window.current_user,
            request_id,
            status
        )

        self.show_result(
            success,
            message
        )

        if success:
            self.refresh_data()

    def show_result(
        self,
        success,
        message
    ):
        if success:
            QMessageBox.information(
                self,
                "موفق",
                message
            )
        else:
            QMessageBox.warning(
                self,
                "خطا",
                message
            )


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
