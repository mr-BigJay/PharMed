import sys

from PySide6.QtWidgets import QApplication

from db import init_db

from ui.main_window import MainWindow


def main():

    init_db()

    app = QApplication(sys.argv)

    with open(
        "assets/style.qss",
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