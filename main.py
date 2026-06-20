import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMessageBox

from db import init_db
from app_paths import resource_path
from services.bootstrap_service import bootstrap_reference_data

from ui.main_window import MainWindow


def main():

    init_db()

    app = QApplication(sys.argv)
    app.setLayoutDirection(
        Qt.RightToLeft
    )

    try:
        bootstrap_reference_data()
    except Exception as exc:
        QMessageBox.warning(
            None,
            "خطا در بارگذاری داده‌های اولیه",
            f"داده‌های مرجع به‌صورت کامل بارگذاری نشدند:\n{exc}"
        )

    with open(
        resource_path(
            "assets",
            "style.qss"
        ),
        "r",
        encoding="utf-8"
    ) as file:

        app.setStyleSheet(
            file.read()
        )

    window = MainWindow()

    window.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()
