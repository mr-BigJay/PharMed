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
    QScrollArea,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from services import inventory_service


class InventoryPage(QWidget):

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.inventory_rows = []

        self.setup_ui()

    def setup_ui(self):
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(
            30,
            25,
            30,
            25
        )
        layout.setSpacing(
            18
        )

        title = QLabel(
            "مدیریت موجودی دارو و تجهیزات"
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
            "جستجوی نام کالا"
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

        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(
            9
        )
        self.inventory_table.setHorizontalHeaderLabels([
            "شناسه",
            "نام کالا",
            "فرم",
            "دسته",
            "واحد",
            "حداقل",
            "موجودی اولیه",
            "موجودی فعلی",
            "وضعیت",
        ])
        self.inventory_table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )
        self.inventory_table.setSelectionBehavior(
            QTableWidget.SelectRows
        )
        self.inventory_table.itemSelectionChanged.connect(
            self.select_current_table_item
        )
        layout.addWidget(
            self.inventory_table
        )

        forms_layout = QHBoxLayout()
        forms_layout.addWidget(
            self.build_item_group()
        )
        forms_layout.addWidget(
            self.build_stock_group()
        )
        forms_layout.addWidget(
            self.build_transaction_group()
        )
        layout.addLayout(
            forms_layout
        )

        transactions_title = QLabel(
            "آخرین تراکنش‌ها"
        )
        transactions_title.setObjectName(
            "welcomeTitle"
        )
        layout.addWidget(
            transactions_title
        )

        self.transactions_table = QTableWidget()
        self.transactions_table.setColumnCount(
            7
        )
        self.transactions_table.setHorizontalHeaderLabels([
            "تاریخ",
            "کالا",
            "نوع",
            "تعداد",
            "سری ساخت",
            "انقضا",
            "توضیحات",
        ])
        self.transactions_table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )
        layout.addWidget(
            self.transactions_table
        )

        scroll = QScrollArea()
        scroll.setWidgetResizable(
            True
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

        self.load_categories()
        self.refresh_data()

    def build_item_group(self):
        group = QGroupBox(
            "ثبت کالای جدید"
        )
        form = QFormLayout(group)

        self.category_combo = QComboBox()
        self.item_name_input = QLineEdit()
        self.item_name_input.setPlaceholderText(
            "نام کالا"
        )
        self.item_form_input = QLineEdit()
        self.item_form_input.setPlaceholderText(
            "مثلاً قرص، آمپول، عدد"
        )
        self.unit_input = QLineEdit()
        self.unit_input.setPlaceholderText(
            "عدد"
        )
        self.minimum_stock_input = QSpinBox()
        self.minimum_stock_input.setMaximum(
            1000000
        )

        add_btn = QPushButton(
            "ثبت کالا"
        )
        add_btn.clicked.connect(
            self.add_item
        )

        form.addRow(
            "دسته:",
            self.category_combo
        )
        form.addRow(
            "نام:",
            self.item_name_input
        )
        form.addRow(
            "فرم:",
            self.item_form_input
        )
        form.addRow(
            "واحد:",
            self.unit_input
        )
        form.addRow(
            "حداقل:",
            self.minimum_stock_input
        )
        form.addRow(
            add_btn
        )

        return group

    def build_stock_group(self):
        group = QGroupBox(
            "موجودی اولیه"
        )
        form = QFormLayout(group)

        self.opening_item_combo = QComboBox()
        self.opening_quantity_input = QDoubleSpinBox()
        self.opening_quantity_input.setMaximum(
            100000000
        )
        self.opening_quantity_input.setDecimals(
            2
        )

        save_btn = QPushButton(
            "ثبت موجودی اولیه"
        )
        save_btn.clicked.connect(
            self.save_opening_stock
        )

        form.addRow(
            "کالا:",
            self.opening_item_combo
        )
        form.addRow(
            "تعداد:",
            self.opening_quantity_input
        )
        form.addRow(
            save_btn
        )

        return group

    def build_transaction_group(self):
        group = QGroupBox(
            "ثبت ورود / خروج"
        )
        form = QFormLayout(group)

        self.transaction_item_combo = QComboBox()
        self.transaction_type_combo = QComboBox()
        self.transaction_type_combo.addItem(
            "ورود",
            inventory_service.TRANSACTION_IN
        )
        self.transaction_type_combo.addItem(
            "خروج",
            inventory_service.TRANSACTION_OUT
        )
        self.transaction_quantity_input = QDoubleSpinBox()
        self.transaction_quantity_input.setMaximum(
            100000000
        )
        self.transaction_quantity_input.setDecimals(
            2
        )
        self.batch_input = QLineEdit()
        self.batch_input.setPlaceholderText(
            "اختیاری"
        )
        self.expiry_input = QLineEdit()
        self.expiry_input.setPlaceholderText(
            "مثلاً 1405/12/29"
        )
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText(
            "اختیاری"
        )

        save_btn = QPushButton(
            "ثبت تراکنش"
        )
        save_btn.clicked.connect(
            self.save_transaction
        )

        form.addRow(
            "کالا:",
            self.transaction_item_combo
        )
        form.addRow(
            "نوع:",
            self.transaction_type_combo
        )
        form.addRow(
            "تعداد:",
            self.transaction_quantity_input
        )
        form.addRow(
            "سری ساخت:",
            self.batch_input
        )
        form.addRow(
            "تاریخ انقضا:",
            self.expiry_input
        )
        form.addRow(
            "توضیحات:",
            self.description_input
        )
        form.addRow(
            save_btn
        )

        return group

    def load_categories(self):
        self.category_combo.clear()

        for category in inventory_service.get_categories():
            self.category_combo.addItem(
                category.name,
                category.id
            )

    def refresh_data(self):
        user = self.main_window.current_user
        self.inventory_rows = inventory_service.list_inventory(
            user,
            self.search_input.text()
        )

        self.fill_inventory_table()
        self.fill_item_combos()
        self.fill_transactions_table()

    def fill_inventory_table(self):
        self.inventory_table.setRowCount(
            len(self.inventory_rows)
        )

        for row_index, row in enumerate(self.inventory_rows):
            values = [
                row["item_id"],
                row["item_name"],
                row["item_form"],
                row["category_name"],
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
                if column_index in (0, 5, 6, 7):
                    item.setTextAlignment(
                        Qt.AlignCenter
                    )
                self.inventory_table.setItem(
                    row_index,
                    column_index,
                    item
                )

        self.inventory_table.resizeColumnsToContents()

    def fill_item_combos(self):
        current_item_id = self.transaction_item_combo.currentData()

        self.opening_item_combo.clear()
        self.transaction_item_combo.clear()

        for row in self.inventory_rows:
            label = (
                f"{row['item_name']} "
                f"{row['item_form']}"
            ).strip()
            self.opening_item_combo.addItem(
                label,
                row["item_id"]
            )
            self.transaction_item_combo.addItem(
                label,
                row["item_id"]
            )

        if current_item_id:
            index = self.transaction_item_combo.findData(
                current_item_id
            )
            if index >= 0:
                self.transaction_item_combo.setCurrentIndex(
                    index
                )
                self.opening_item_combo.setCurrentIndex(
                    index
                )

    def fill_transactions_table(self):
        transactions = inventory_service.list_recent_transactions(
            self.main_window.current_user
        )
        self.transactions_table.setRowCount(
            len(transactions)
        )

        for row_index, transaction in enumerate(transactions):
            values = [
                transaction["date"],
                (
                    f"{transaction['item_name']} "
                    f"{transaction['item_form']}"
                ).strip(),
                transaction["transaction_label"],
                transaction["quantity"],
                transaction["batch_number"],
                transaction["expiry_date"],
                transaction["description"],
            ]

            for column_index, value in enumerate(values):
                self.transactions_table.setItem(
                    row_index,
                    column_index,
                    QTableWidgetItem(
                        _format_value(value)
                    )
                )

        self.transactions_table.resizeColumnsToContents()

    def select_current_table_item(self):
        selected_items = self.inventory_table.selectedItems()

        if not selected_items:
            return

        selected_row = selected_items[0].row()
        item_id = self.inventory_rows[selected_row]["item_id"]

        for combo in (
            self.opening_item_combo,
            self.transaction_item_combo
        ):
            index = combo.findData(
                item_id
            )
            if index >= 0:
                combo.setCurrentIndex(
                    index
                )

    def add_item(self):
        success, message = inventory_service.add_item(
            category_id=self.category_combo.currentData(),
            item_name=self.item_name_input.text(),
            item_form=self.item_form_input.text(),
            unit=self.unit_input.text(),
            minimum_stock=self.minimum_stock_input.value()
        )

        self.show_result(
            success,
            message
        )

        if success:
            self.item_name_input.clear()
            self.item_form_input.clear()
            self.unit_input.clear()
            self.minimum_stock_input.setValue(
                0
            )
            self.refresh_data()

    def save_opening_stock(self):
        success, message = inventory_service.set_opening_stock(
            user=self.main_window.current_user,
            item_id=self.opening_item_combo.currentData(),
            quantity=self.opening_quantity_input.value()
        )

        self.show_result(
            success,
            message
        )

        if success:
            self.refresh_data()

    def save_transaction(self):
        success, message = inventory_service.create_transaction(
            user=self.main_window.current_user,
            item_id=self.transaction_item_combo.currentData(),
            transaction_type=self.transaction_type_combo.currentData(),
            quantity=self.transaction_quantity_input.value(),
            batch_number=self.batch_input.text(),
            expiry_date=self.expiry_input.text(),
            description=self.description_input.text()
        )

        self.show_result(
            success,
            message
        )

        if success:
            self.transaction_quantity_input.setValue(
                0
            )
            self.batch_input.clear()
            self.expiry_input.clear()
            self.description_input.clear()
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
