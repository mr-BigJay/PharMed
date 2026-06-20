import sys

from PySide6.QtWidgets import QApplication

from db import engine

from models.base import Base

from models.user import User
from models.center import Center
from models.health_house import HealthHouse
from models.category import Category
from models.item import Item

from ui.main_window import MainWindow


def main():

    Base.metadata.create_all(
        bind=engine
    )

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