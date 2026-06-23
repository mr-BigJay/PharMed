from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QWidget,
)

FORM_MAX_WIDTH = 520
FIELD_MAX_WIDTH = 360


def configure_compact_form(group: QGroupBox) -> QGroupBox:
    group.setObjectName(
        "compactForm"
    )
    group.setMaximumWidth(
        FORM_MAX_WIDTH
    )

    layout = group.layout()
    if isinstance(
        layout,
        QFormLayout
    ):
        layout.setFieldGrowthPolicy(
            QFormLayout.FieldsStayAtSizeHint
        )
        layout.setFormAlignment(
            Qt.AlignRight | Qt.AlignTop
        )
        layout.setLabelAlignment(
            Qt.AlignRight
        )

        for index in range(
            layout.rowCount()
        ):
            field_item = layout.itemAt(
                index,
                QFormLayout.FieldRole
            )
            if not field_item:
                continue

            field_widget = field_item.widget()
            if field_widget:
                field_widget.setMaximumWidth(
                    FIELD_MAX_WIDTH
                )

    return group


def wrap_centered_form(
    group: QGroupBox
) -> QWidget:
    configure_compact_form(
        group
    )

    row = QHBoxLayout()
    row.setContentsMargins(
        0,
        0,
        0,
        0
    )
    row.addStretch()
    row.addWidget(
        group
    )
    row.addStretch()

    wrapper = QWidget()
    wrapper.setLayout(
        row
    )
    return wrapper
