from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from services.format_utils import format_value
from services.inventory_service import list_inventory
from services.request_service import (
    create_request,
    list_requests,
)
from ui.widgets.compact_form import wrap_centered_form
from ui.widgets.form_fields import (
    combo_value_by_text,
    create_quantity_input,
    create_searchable_combo,
    reset_combo_selection,
)


class RequestsPage(QWidget):

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.requests = []
        self.inventory_rows = []
        self.current_section = "form"
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
            Qt.AlignRight
        )
        layout.addWidget(
            title
        )

        sections_layout = QHBoxLayout()
        self.form_section_btn = QPushButton(
            "فرم درخواست"
        )
        self.form_section_btn.setObjectName(
            "sectionButton"
        )
        self.form_section_btn.clicked.connect(
            lambda: self.set_section("form")
        )
        self.list_section_btn = QPushButton(
            "لیست درخواست‌های تأمین کالا"
        )
        self.list_section_btn.setObjectName(
            "sectionButton"
        )
        self.list_section_btn.clicked.connect(
            lambda: self.set_section("list")
        )
        sections_layout.addWidget(
            self.form_section_btn
        )
        sections_layout.addWidget(
            self.list_section_btn
        )
        sections_layout.addStretch()
        layout.addLayout(
            sections_layout
        )

        self.form_group = QGroupBox(
            "فرم درخواست"
        )
        form = QFormLayout(self.form_group)

        self.item_combo = create_searchable_combo(
            "جستجو یا انتخاب از لیست..."
        )
        self.item_combo.currentIndexChanged.connect(
            self.update_item_details
        )
        self.item_combo.lineEdit().textEdited.connect(
            lambda _text: self.update_item_details()
        )
        self.form_value_label = QLabel(
            "-"
        )
        self.form_value_label.setObjectName(
            "summaryRow"
        )
        self.unit_value_label = QLabel(
            "-"
        )
        self.unit_value_label.setObjectName(
            "summaryRow"
        )
        self.quantity_input = create_quantity_input(
            decimals=2
        )

        submit_btn = QPushButton(
            "ثبت درخواست و بازگشت"
        )
        submit_btn.clicked.connect(
            self.submit_request
        )

        form.addRow(
            "کالا:",
            self.item_combo
        )
        form.addRow(
            "فرم:",
            self.form_value_label
        )
        form.addRow(
            "واحد:",
            self.unit_value_label
        )
        form.addRow(
            "تعداد:",
            self.quantity_input
        )
        form.addRow(
            submit_btn
        )
        layout.addWidget(
            wrap_centered_form(
                self.form_group
            )
        )

        self.list_group = QGroupBox(
            "لیست درخواست‌های تأمین کالا"
        )
        list_layout = QVBoxLayout(self.list_group)
        actions_layout = QHBoxLayout()
        refresh_btn = QPushButton(
            "به‌روزرسانی"
        )
        refresh_btn.clicked.connect(
            self.refresh_data
        )
        actions_layout.addWidget(
            refresh_btn
        )
        actions_layout.addStretch()
        list_layout.addLayout(
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
        list_layout.addWidget(
            self.table
        )
        layout.addWidget(
            self.list_group
        )

        self.setLayout(
            layout
        )
        self.refresh_data()
        self.set_section(
            "form"
        )

    def set_section(
        self,
        section
    ):
        self.current_section = section
        self.form_group.setVisible(
            section == "form"
        )
        self.list_group.setVisible(
            section == "list"
        )
        self.form_section_btn.setProperty(
            "active",
            section == "form"
        )
        self.list_section_btn.setProperty(
            "active",
            section == "list"
        )
        for button in (
            self.form_section_btn,
            self.list_section_btn
        ):
            button.style().unpolish(
                button
            )
            button.style().polish(
                button
            )

    def refresh_data(self):
        self.load_items()
        self.requests = list_requests(
            self.main_window.current_user
        )
        self.fill_table()

    def load_items(self):
        self.item_combo.clear()
        self.inventory_rows = list_inventory(
            self.main_window.current_user
        )

        for row in self.inventory_rows:
            label = (
                f"{row['item_name']} "
                f"{row['item_form']}"
            ).strip()
            self.item_combo.addItem(
                label,
                row["item_id"]
            )

        reset_combo_selection(
            self.item_combo
        )
        self.update_item_details()

    def update_item_details(self):
        item_id = combo_value_by_text(
            self.item_combo
        )
        selected_row = next(
            (
                row
                for row in self.inventory_rows
                if row["item_id"] == item_id
            ),
            None
        )

        if not selected_row:
            self.form_value_label.setText(
                "-"
            )
            self.unit_value_label.setText(
                "-"
            )
            return

        self.form_value_label.setText(
            selected_row["item_form"] or "-"
        )
        self.unit_value_label.setText(
            selected_row["unit"] or "-"
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
                    format_value(value)
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
        item_id = combo_value_by_text(
            self.item_combo
        )
        if item_id is None:
            self.show_result(
                False,
                "کالای انتخاب‌شده معتبر نیست"
            )
            return

        success, message = create_request(
            user=self.main_window.current_user,
            item_id=item_id,
            quantity=self.quantity_input.value(),
            description=""
        )

        self.show_result(
            success,
            message
        )

        if success:
            self.quantity_input.setValue(
                0
            )
            self.refresh_data()
            self.main_window.show_dashboard()

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


