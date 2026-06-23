from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
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
    QGraphicsBlurEffect,
)

from services.bootstrap_service import (
    DRUG_CATEGORY_NAME,
    MEDICAL_CATEGORY_NAME,
)
from services.format_utils import format_value
from services import inventory_service
from ui.widgets.form_fields import (
    combo_value_by_text,
    configure_plain_combo,
    configure_quantity_input,
    create_quantity_input,
    create_searchable_combo,
    reset_combo_selection,
)


class InventoryPage(QWidget):

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.inventory_rows = []
        self.current_mode = "items"
        self.current_stock_in_section = "register"
        self.current_stock_out_section = "register"

        self.summary_value_labels = {}

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

        self.title_label = QLabel(
            "مدیریت موجودی دارو و تجهیزات"
        )
        self.title_label.setObjectName(
            "pageTitle"
        )
        self.title_label.setAlignment(
            Qt.AlignCenter
        )
        layout.addWidget(
            self.title_label,
            alignment=Qt.AlignHCenter
        )

        self.items_summary_widget = self.build_items_summary()
        layout.addWidget(
            self.items_summary_widget
        )

        self.items_toolbar = self.build_items_toolbar()
        layout.addWidget(
            self.items_toolbar
        )

        self.stock_in_section_layout = QHBoxLayout()
        self.register_stock_in_btn = QPushButton(
            "ثبت ورود به انبار"
        )
        self.register_stock_in_btn.setObjectName(
            "sectionButton"
        )
        self.register_stock_in_btn.clicked.connect(
            lambda: self.set_stock_in_section("register")
        )
        self.list_stock_in_btn = QPushButton(
            "لیست ورودهای ثبت‌شده"
        )
        self.list_stock_in_btn.setObjectName(
            "sectionButton"
        )
        self.list_stock_in_btn.clicked.connect(
            lambda: self.set_stock_in_section("list")
        )
        self.stock_in_section_layout.addStretch()
        self.stock_in_section_layout.addWidget(
            self.register_stock_in_btn
        )
        self.stock_in_section_layout.addWidget(
            self.list_stock_in_btn
        )
        self.stock_in_section_layout.addStretch()

        self.stock_in_section_widget = QWidget()
        self.stock_in_section_widget.setLayout(
            self.stock_in_section_layout
        )
        layout.addWidget(
            self.stock_in_section_widget
        )

        self.stock_out_section_layout = QHBoxLayout()
        self.register_stock_out_btn = QPushButton(
            "ثبت خروج از انبار"
        )
        self.register_stock_out_btn.setObjectName(
            "sectionButton"
        )
        self.register_stock_out_btn.clicked.connect(
            lambda: self.set_stock_out_section("register")
        )
        self.list_stock_out_btn = QPushButton(
            "لیست خروج‌های ثبت‌شده"
        )
        self.list_stock_out_btn.setObjectName(
            "sectionButton"
        )
        self.list_stock_out_btn.clicked.connect(
            lambda: self.set_stock_out_section("list")
        )
        self.stock_out_section_layout.addStretch()
        self.stock_out_section_layout.addWidget(
            self.register_stock_out_btn
        )
        self.stock_out_section_layout.addWidget(
            self.list_stock_out_btn
        )
        self.stock_out_section_layout.addStretch()

        self.stock_out_section_widget = QWidget()
        self.stock_out_section_widget.setLayout(
            self.stock_out_section_layout
        )
        layout.addWidget(
            self.stock_out_section_widget
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
        self._configure_inventory_table(
            self.inventory_table
        )
        layout.addWidget(
            self.inventory_table
        )

        self.item_form_group = self.build_item_group()
        self.stock_group = self.build_stock_group()
        self.transaction_group = self.build_transaction_group()

        layout.addWidget(
            self.stock_group
        )
        layout.addWidget(
            self.transaction_group
        )

        self.transactions_title = QLabel(
            "آخرین تراکنش‌ها"
        )
        self.transactions_title.setObjectName(
            "welcomeTitle"
        )
        layout.addWidget(
            self.transactions_title
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

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(
            True
        )
        self.scroll.setFrameShape(
            QFrame.NoFrame
        )
        self.scroll.setWidget(
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
            self.scroll
        )
        self.setLayout(
            root_layout
        )

        self.build_item_modal()

        self.load_categories()
        self.refresh_data()
        self.set_mode(
            "items"
        )

    def build_items_summary(self):
        widget = QWidget()
        grid = QGridLayout(widget)
        grid.setHorizontalSpacing(
            12
        )
        grid.setVerticalSpacing(
            0
        )
        grid.setContentsMargins(
            0,
            0,
            0,
            0
        )

        cards = [
            (
                "total",
                "کل اقلام",
                "قلم",
                "metricBlue",
                "📦",
            ),
            (
                "drug",
                "اقلام دارویی",
                "مورد",
                "metricGreen",
                "💊",
            ),
            (
                "equipment",
                "تجهیزات پزشکی",
                "مورد",
                "metricPurple",
                "🏥",
            ),
        ]

        for column_index in range(3):
            grid.setColumnStretch(
                column_index,
                1
            )

        for index, (key, title, unit, style, icon) in enumerate(cards):
            card = self.build_summary_card(
                title,
                unit,
                style,
                icon
            )
            self.summary_value_labels[key] = (
                card.findChild(
                    QLabel,
                    "metricValue"
                )
            )
            grid.addWidget(
                card,
                0,
                index
            )

        return widget

    def build_summary_card(
        self,
        title,
        unit,
        object_name,
        icon
    ):
        card = QFrame()
        card.setObjectName(
            object_name
        )
        card.setMinimumHeight(
            96
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
            format_value(0)
        )
        value_label.setObjectName(
            "metricValue"
        )
        unit_label = QLabel(
            unit
        )
        unit_label.setObjectName(
            "metricSubtitle"
        )

        text_layout.addWidget(
            title_label
        )
        text_layout.addWidget(
            value_label
        )
        text_layout.addWidget(
            unit_label
        )

        layout.addWidget(
            icon_label
        )
        layout.addLayout(
            text_layout,
            stretch=1
        )
        return card

    def build_items_toolbar(self):
        widget = QWidget()
        row = QHBoxLayout(widget)
        row.setContentsMargins(
            0,
            0,
            0,
            0
        )
        row.setSpacing(
            12
        )

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "جستجو در لیست اقلام..."
        )
        self.search_input.textChanged.connect(
            self.refresh_data
        )

        self.new_item_btn = QPushButton(
            "ثبت مورد جدید"
        )
        self.new_item_btn.setObjectName(
            "loginPrimaryButton"
        )
        self.new_item_btn.setMinimumWidth(
            160
        )
        self.new_item_btn.clicked.connect(
            self.open_item_modal
        )

        row.addWidget(
            self.search_input,
            stretch=1
        )
        row.addWidget(
            self.new_item_btn
        )
        return widget

    def build_item_modal(self):
        self.modal_overlay = QFrame(
            self
        )
        self.modal_overlay.setObjectName(
            "modalOverlay"
        )
        self.modal_overlay.hide()

        overlay_layout = QVBoxLayout(
            self.modal_overlay
        )
        overlay_layout.setContentsMargins(
            24,
            24,
            24,
            24
        )
        overlay_layout.addStretch(
            1
        )

        center_row = QHBoxLayout()
        center_row.addStretch(
            1
        )

        modal_card = QFrame()
        modal_card.setObjectName(
            "modalCard"
        )
        card_layout = QVBoxLayout(
            modal_card
        )
        card_layout.setContentsMargins(
            24,
            24,
            24,
            24
        )
        card_layout.setSpacing(
            16
        )

        modal_title = QLabel(
            "ثبت اقلام دارویی و تجهیزات پزشکی"
        )
        modal_title.setObjectName(
            "panelTitle"
        )
        modal_title.setAlignment(
            Qt.AlignCenter
        )
        card_layout.addWidget(
            modal_title
        )
        card_layout.addWidget(
            self.item_form_group
        )

        buttons_row = QHBoxLayout()
        buttons_row.setSpacing(
            12
        )
        cancel_btn = QPushButton(
            "بازگشت"
        )
        cancel_btn.setObjectName(
            "sectionButton"
        )
        cancel_btn.clicked.connect(
            self.close_item_modal
        )
        submit_btn = QPushButton(
            "ثبت"
        )
        submit_btn.setObjectName(
            "loginPrimaryButton"
        )
        submit_btn.clicked.connect(
            self.add_item
        )
        buttons_row.addWidget(
            cancel_btn
        )
        buttons_row.addWidget(
            submit_btn
        )
        card_layout.addLayout(
            buttons_row
        )

        center_row.addWidget(
            modal_card
        )
        center_row.addStretch(
            1
        )
        overlay_layout.addLayout(
            center_row
        )
        overlay_layout.addStretch(
            1
        )

    def resizeEvent(
        self,
        event
    ):
        super().resizeEvent(
            event
        )
        if hasattr(
            self,
            "modal_overlay"
        ):
            self.modal_overlay.setGeometry(
                self.rect()
            )

    def open_item_modal(self):
        blur = QGraphicsBlurEffect()
        blur.setBlurRadius(
            10
        )
        self.scroll.setGraphicsEffect(
            blur
        )
        self.modal_overlay.setGeometry(
            self.rect()
        )
        self.modal_overlay.show()
        self.modal_overlay.raise_()

    def close_item_modal(self):
        self.scroll.setGraphicsEffect(
            None
        )
        self.modal_overlay.hide()

    def update_items_summary(self):
        all_rows = inventory_service.list_inventory(
            self.main_window.current_user,
            ""
        )
        total = len(
            all_rows
        )
        drug_count = sum(
            1
            for row in all_rows
            if row["category_name"] == DRUG_CATEGORY_NAME
        )
        equipment_count = sum(
            1
            for row in all_rows
            if row["category_name"] == MEDICAL_CATEGORY_NAME
        )

        values = {
            "total": total,
            "drug": drug_count,
            "equipment": equipment_count,
        }

        for key, label in self.summary_value_labels.items():
            if label:
                label.setText(
                    format_value(
                        values.get(
                            key,
                            0
                        )
                    )
                )

    def set_mode(
        self,
        mode
    ):
        self.current_mode = mode
        titles = {
            "items": "اقلام دارویی و تجهیزات پزشکی",
            "stock": "موجودی انبار",
            "stock_in": "ورود انبار",
            "stock_out": "خروج انبار",
        }
        self.title_label.setText(
            titles.get(
                mode,
                "مدیریت موجودی دارو و تجهیزات"
            )
        )

        if mode == "stock_in":
            self.current_stock_in_section = "register"
            index = self.transaction_type_combo.findData(
                inventory_service.TRANSACTION_IN
            )
            if index >= 0:
                self.transaction_type_combo.setCurrentIndex(
                    index
                )

        if mode == "stock_out":
            self.current_stock_out_section = "register"
            index = self.transaction_type_combo.findData(
                inventory_service.TRANSACTION_OUT
            )
            if index >= 0:
                self.transaction_type_combo.setCurrentIndex(
                    index
                )

        self.transaction_type_combo.setEnabled(
            mode not in ("stock_in", "stock_out")
        )
        if mode == "stock_in":
            self.transaction_group.setTitle(
                "ثبت ورود به انبار"
            )
            self.transactions_title.setText(
                "لیست ورودهای ثبت‌شده"
            )
        elif mode == "stock_out":
            self.transaction_group.setTitle(
                "ثبت خروج از انبار"
            )
            self.transactions_title.setText(
                "لیست خروج‌های ثبت‌شده"
            )
        else:
            self.transaction_group.setTitle(
                "ثبت ورود / خروج"
            )
            self.transactions_title.setText(
                "آخرین تراکنش‌ها"
            )

        self.update_mode_visibility()

    def set_stock_in_section(
        self,
        section
    ):
        self.current_stock_in_section = section
        self.update_mode_visibility()

    def set_stock_out_section(
        self,
        section
    ):
        self.current_stock_out_section = section
        self.update_mode_visibility()

    def update_mode_visibility(self):
        is_items_mode = self.current_mode == "items"
        is_stock_in_mode = self.current_mode == "stock_in"
        is_stock_out_mode = self.current_mode == "stock_out"

        self.items_summary_widget.setVisible(
            is_items_mode
        )
        self.items_toolbar.setVisible(
            is_items_mode
        )
        self.stock_in_section_widget.setVisible(
            is_stock_in_mode
        )
        self.stock_out_section_widget.setVisible(
            is_stock_out_mode
        )
        self.inventory_table.setVisible(
            is_items_mode
            or self.current_mode == "stock"
        )
        self.stock_group.setVisible(
            self.current_mode == "stock"
        )
        self.transaction_group.setVisible(
            (
                is_stock_out_mode
                and self.current_stock_out_section == "register"
            )
            or (
                is_stock_in_mode
                and self.current_stock_in_section == "register"
            )
        )
        self.transactions_title.setVisible(
            (
                is_stock_out_mode
                and self.current_stock_out_section == "list"
            )
            or (
                is_stock_in_mode
                and self.current_stock_in_section == "list"
            )
        )
        self.transactions_table.setVisible(
            (
                is_stock_out_mode
                and self.current_stock_out_section == "list"
            )
            or (
                is_stock_in_mode
                and self.current_stock_in_section == "list"
            )
        )

        self.register_stock_in_btn.setProperty(
            "active",
            self.current_stock_in_section == "register"
        )
        self.list_stock_in_btn.setProperty(
            "active",
            self.current_stock_in_section == "list"
        )
        self.register_stock_out_btn.setProperty(
            "active",
            self.current_stock_out_section == "register"
        )
        self.list_stock_out_btn.setProperty(
            "active",
            self.current_stock_out_section == "list"
        )
        for button in (
            self.register_stock_in_btn,
            self.list_stock_in_btn,
            self.register_stock_out_btn,
            self.list_stock_out_btn,
        ):
            button.style().unpolish(
                button
            )
            button.style().polish(
                button
            )

    def build_item_group(self):
        group = QGroupBox()
        group.setObjectName(
            "modalFormGroup"
        )
        form = QFormLayout(group)

        self.category_combo = configure_plain_combo(
            QComboBox()
        )
        self.category_combo.currentIndexChanged.connect(
            self.load_item_name_options
        )
        self.item_name_combo = create_searchable_combo(
            "جستجو یا انتخاب از لیست..."
        )
        self.item_name_combo.currentIndexChanged.connect(
            self.update_new_item_field
        )
        self.new_item_name_input = QLineEdit()
        self.new_item_name_input.setPlaceholderText(
            "نام عنوان جدید"
        )
        self.item_form_combo = configure_plain_combo(
            QComboBox()
        )
        self.item_form_combo.addItems([
            "بدون فرم",
            "قرص",
            "کپسول",
            "شربت",
            "آمپول",
            "ویال",
            "قطره",
            "پماد",
            "کرم",
            "محلول",
            "سرم",
            "اسپری",
            "ساشه",
            "شیاف",
            "ابزار مصرفی",
            "دستکش",
            "سرنگ",
        ])
        self.unit_combo = configure_plain_combo(
            QComboBox()
        )
        self.unit_combo.addItems([
            "عدد",
            "بسته",
            "جعبه",
            "کارتن",
            "شیشه",
            "ویال",
            "آمپول",
            "تیوب",
            "جفت",
            "متر",
            "رول",
        ])
        helper = QLabel(
            "نام قلم از منوی اقلام موجود انتخاب می‌شود. برای ثبت عنوان جدید، گزینه افزودن عنوان جدید را انتخاب کنید."
        )
        helper.setObjectName(
            "pageSubtitle"
        )
        helper.setWordWrap(
            True
        )
        self.minimum_stock_input = configure_quantity_input(
            QSpinBox()
        )
        self.minimum_stock_input.setMaximum(
            1000000
        )

        form.addRow(
            "دسته:",
            self.category_combo
        )
        form.addRow(
            "نام:",
            self.item_name_combo
        )
        form.addRow(
            "عنوان جدید:",
            self.new_item_name_input
        )
        form.addRow(
            "فرم:",
            self.item_form_combo
        )
        form.addRow(
            "واحد:",
            self.unit_combo
        )
        form.addRow(
            "حداقل:",
            self.minimum_stock_input
        )
        form.addRow(
            helper
        )

        return group

    def update_new_item_field(self):
        self.new_item_name_input.setVisible(
            self.item_name_combo.currentData() == "__new__"
        )

    def build_stock_group(self):
        group = QGroupBox(
            "موجودی اولیه"
        )
        form = QFormLayout(group)

        self.opening_item_combo = create_searchable_combo(
            "جستجو یا انتخاب از لیست..."
        )
        self.opening_quantity_input = create_quantity_input(
            decimals=2
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

        self.transaction_item_combo = create_searchable_combo(
            "جستجو یا انتخاب از لیست..."
        )
        self.transaction_type_combo = configure_plain_combo(
            QComboBox()
        )
        self.transaction_type_combo.addItem(
            "ورود",
            inventory_service.TRANSACTION_IN
        )
        self.transaction_type_combo.addItem(
            "خروج",
            inventory_service.TRANSACTION_OUT
        )
        self.transaction_quantity_input = create_quantity_input(
            decimals=2
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

        self.load_item_name_options()

    def load_item_name_options(self):
        if not hasattr(
            self,
            "item_name_combo"
        ):
            return

        category_id = self.category_combo.currentData()
        self.item_name_combo.clear()

        for item_name in inventory_service.get_item_names_by_category(
            category_id
        ):
            self.item_name_combo.addItem(
                item_name
            )

        self.item_name_combo.addItem(
            "➕ افزودن عنوان جدید",
            "__new__"
        )
        reset_combo_selection(
            self.item_name_combo
        )
        self.update_new_item_field()

    def refresh_data(self):
        user = self.main_window.current_user
        search_text = ""

        if hasattr(
            self,
            "search_input"
        ):
            search_text = self.search_input.text()

        self.inventory_rows = inventory_service.list_inventory(
            user,
            search_text
        )

        self.update_items_summary()
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
                    format_value(value)
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

    def _configure_inventory_table(
        self,
        table
    ):
        table.verticalHeader().setVisible(
            False
        )
        header = table.horizontalHeader()
        header.setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        header.setDefaultAlignment(
            Qt.AlignCenter
        )
        header.setStretchLastSection(
            True
        )

    def fill_item_combos(self):
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

        reset_combo_selection(
            self.opening_item_combo
        )
        reset_combo_selection(
            self.transaction_item_combo
        )

    def fill_transactions_table(self):
        transactions = inventory_service.list_recent_transactions(
            self.main_window.current_user
        )
        if self.current_mode == "stock_in":
            transactions = [
                transaction
                for transaction in transactions
                if transaction["transaction_type"] ==
                inventory_service.TRANSACTION_IN
            ]
        elif self.current_mode == "stock_out":
            transactions = [
                transaction
                for transaction in transactions
                if transaction["transaction_type"] ==
                inventory_service.TRANSACTION_OUT
            ]

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
                        format_value(value)
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
        item_name = (
            self.new_item_name_input.text().strip()
            if self.item_name_combo.currentData() == "__new__"
            else self.item_name_combo.currentText()
        )
        success, message = inventory_service.add_item(
            category_id=self.category_combo.currentData(),
            item_name=item_name,
            item_form=(
                ""
                if self.item_form_combo.currentText() == "بدون فرم"
                else self.item_form_combo.currentText()
            ),
            unit=self.unit_combo.currentText(),
            minimum_stock=self.minimum_stock_input.value()
        )

        self.show_result(
            success,
            message
        )

        if success:
            self.new_item_name_input.clear()
            self.minimum_stock_input.setValue(
                0
            )
            self.refresh_data()
            self.close_item_modal()

    def save_opening_stock(self):
        item_id = combo_value_by_text(
            self.opening_item_combo
        )
        if item_id is None:
            self.show_result(
                False,
                "کالای انتخاب‌شده معتبر نیست"
            )
            return

        success, message = inventory_service.set_opening_stock(
            user=self.main_window.current_user,
            item_id=item_id,
            quantity=self.opening_quantity_input.value()
        )

        self.show_result(
            success,
            message
        )

        if success:
            self.refresh_data()

    def save_transaction(self):
        item_id = combo_value_by_text(
            self.transaction_item_combo
        )
        if item_id is None:
            self.show_result(
                False,
                "کالای انتخاب‌شده معتبر نیست"
            )
            return

        success, message = inventory_service.create_transaction(
            user=self.main_window.current_user,
            item_id=item_id,
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
            reset_combo_selection(
                self.transaction_item_combo
            )
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
