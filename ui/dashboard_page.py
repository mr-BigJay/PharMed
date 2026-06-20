from models.user import User
from ui.widgets.page_header import PageHeader
from ui.widgets.action_card import ActionCard

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QGridLayout,
    QFrame,
    QPushButton,
    QSizePolicy,
    QScrollArea
)

from PySide6.QtCore import Qt

from services.db_session import SessionLocal

from models.center import Center
from models.health_house import HealthHouse


class DashboardPage(QWidget):

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.db = SessionLocal()

        self.setup_ui()

    def setup_ui(self):

        user = self.main_window.current_user

        content = QWidget()

        main_layout = QVBoxLayout(content)

        main_layout.setContentsMargins(
            40,
            30,
            40,
            30
        )

        main_layout.setSpacing(25)

        header = PageHeader(
            "PharMed",
            "سامانه مدیریت دارو و تجهیزات پزشکی"
        )

        main_layout.addWidget(
            header,
            alignment=Qt.AlignHCenter
        )

        welcome_card = QFrame()

        welcome_card.setObjectName(
            "welcomeCard"
        )

        welcome_card.setMinimumHeight(
            130
        )

        welcome_layout = QVBoxLayout()

        welcome_layout.setContentsMargins(
            30,
            25,
            30,
            25
        )

        welcome_layout.setSpacing(8)

        if user:

            full_name = (
                f"{user.first_name} "
                f"{user.last_name}"
            )

            if user.role == "پرستار":

                welcome_text = (
                    f"پرستار گرامی {full_name}، خوش آمدید"
                )

            else:

                welcome_text = (
                    f"بهورز گرامی {full_name}، خوش آمدید"
                )

        else:

            welcome_text = (
                "به PharMed خوش آمدید"
            )

        welcome_title = QLabel(
            welcome_text
        )

        welcome_title.setObjectName(
            "welcomeTitle"
        )

        welcome_title.setAlignment(
            Qt.AlignCenter
        )

        welcome_title.setWordWrap(
            True
        )

        welcome_layout.addWidget(
            welcome_title
        )

        location_text = ""

        if user and user.health_house_id:

            house = (
                self.db.query(
                    HealthHouse
                )
                .filter(
                    HealthHouse.id ==
                    user.health_house_id
                )
                .first()
            )

            if house:

                location_text = (
                    f"خانه بهداشت: {house.name}"
                )

        elif user and user.center_id:

            center = (
                self.db.query(
                    Center
                )
                .filter(
                    Center.id ==
                    user.center_id
                )
                .first()
            )

            if center:

                location_text = (
                    f"مرکز درمانی: {center.name}"
                )

        if location_text:

            location_label = QLabel(
                location_text
            )

            location_label.setObjectName(
                "welcomeLocation"
            )

            location_label.setAlignment(
                Qt.AlignCenter
            )

            welcome_layout.addWidget(
                location_label
            )

        if user and user.is_manager:

            admin_label = QLabel(
                "مدیر سامانه"
            )

            admin_label.setObjectName(
                "welcomeInfo"
            )

            admin_label.setAlignment(
                Qt.AlignCenter
            )

            welcome_layout.addWidget(
                admin_label
            )

            max_users = 3
            registered_count = 0

            if user.health_house_id:

                registered_count = (
                    self.db.query(User)
                    .filter(
                        User.health_house_id ==
                        user.health_house_id
                    )
                    .count()
                )

            elif user.center_id:

                registered_count = (
                    self.db.query(User)
                    .filter(
                        User.center_id ==
                        user.center_id,
                        User.health_house_id.is_(None)
                    )
                    .count()
                )

            users_count_label = QLabel(
                f"{registered_count} از {max_users} مورد ثبت شده"
            )

            users_count_label.setObjectName(
                "usersCountLabel"
            )

            users_count_label.setAlignment(
                Qt.AlignCenter
            )

            welcome_layout.addWidget(
                users_count_label
            )
            

        welcome_card.setLayout(
            welcome_layout
        )

        main_layout.addWidget(
            welcome_card
        )

        cards_grid = QGridLayout()

        cards_grid.setHorizontalSpacing(
            20
        )

        cards_grid.setVerticalSpacing(
            20
        )

        cards_grid.setColumnStretch(
            0,
            1
        )

        cards_grid.setColumnStretch(
            1,
            1
        )

        inventory_card = ActionCard(
            "📦 مدیریت موجودی دارو"
        )
        inventory_card.callback = (
        self.main_window.show_inventory
        )

        equipment_card = ActionCard(
            "🏥 تجهیزات پزشکی"
        )

        requests_card = ActionCard(
            "📋 درخواست‌ها"
        )

        reports_card = ActionCard(
            "📊 گزارشات"
        )

        users_card = ActionCard(
            "👥 مدیریت کاربران"
        )

        cards_grid.addWidget(
            inventory_card,
            0,
            0
        )

        cards_grid.addWidget(
            equipment_card,
            0,
            1
        )

        cards_grid.addWidget(
            requests_card,
            1,
            0
        )

        cards_grid.addWidget(
            reports_card,
            1,
            1
        )

        if user and user.is_manager:

            cards_grid.addWidget(
                users_card,
                2,
                0,
                1,
                2
            )

        main_layout.addLayout(
            cards_grid
        )

        main_layout.addSpacing(
            15
        )

        logout_btn = QPushButton(
            "خروج از حساب کاربری"
        )

        logout_btn.setObjectName(
            "logoutButton"
        )

        logout_btn.setMinimumHeight(
            55
        )

        logout_btn.setMaximumWidth(
            400
        )

        logout_btn.clicked.connect(
            self.logout
        )

        main_layout.addWidget(
            logout_btn,
            alignment=Qt.AlignCenter
        )

        main_layout.addStretch()

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

    def logout(self):

        self.main_window.current_user = None

        self.main_window.show_login()