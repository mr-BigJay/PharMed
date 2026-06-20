from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QColor,
    QPainter,
    QLinearGradient,
    QPen
)

from PySide6.QtWidgets import QWidget


class BackgroundWidget(QWidget):

    def __init__(self):
        super().__init__()

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        gradient = QLinearGradient(
            0,
            0,
            self.width(),
            self.height()
        )

        gradient.setColorAt(
            0,
            QColor("#071426")
        )

        gradient.setColorAt(
            1,
            QColor("#02101F")
        )

        painter.fillRect(
            self.rect(),
            gradient
        )

        pen = QPen(
            QColor(45, 212, 191, 25)
        )

        pen.setWidth(1)

        painter.setPen(pen)

        for x in range(50, self.width(), 140):

            for y in range(
                50,
                self.height(),
                120
            ):

                painter.drawEllipse(
                    x,
                    y,
                    60,
                    60
                )

        painter.setPen(
            QPen(
                QColor(45, 212, 191, 40),
                4
            )
        )

        painter.drawText(
            self.width() - 120,
            120,
            "+"
        )

        painter.drawText(
            60,
            self.height() - 80,
            "+"
        )