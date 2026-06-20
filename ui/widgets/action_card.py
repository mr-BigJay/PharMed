from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QSizePolicy
)


class ActionCard(QFrame):

    def __init__(self, title):
        super().__init__()

        self.setObjectName(
            "actionCard"
        )

        self.setFixedSize(
            320,
            75
        )

        self.setSizePolicy(
            QSizePolicy.Fixed,
            QSizePolicy.Fixed
        )

        layout = QVBoxLayout()

        layout.setContentsMargins(
            10,
            10,
            10,
            10
        )

        layout.setSpacing(0)

        label = QLabel(title)

        label.setAlignment(
            Qt.AlignCenter
        )

        label.setObjectName(
            "actionCardLabel"
        )

        layout.addWidget(
            label
        )

        self.setLayout(
            layout
        )
        
        self.setCursor(
        Qt.PointingHandCursor
        )
        def mousePressEvent(
            self,
            event
        ):

            if hasattr(
                self,
                "callback"
            ):
        
                self.callback()

            super().mousePressEvent(
                event
            )