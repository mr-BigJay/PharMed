from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractSpinBox,
    QComboBox,
    QCompleter,
    QDoubleSpinBox,
    QSpinBox,
)


def create_searchable_combo(
    placeholder=""
):
    combo = QComboBox()
    combo.setEditable(
        True
    )
    combo.setInsertPolicy(
        QComboBox.InsertPolicy.NoInsert
    )
    combo.setObjectName(
        "searchCombo"
    )

    line_edit = combo.lineEdit()
    line_edit.setPlaceholderText(
        placeholder
        or "جستجو و انتخاب کالا..."
    )
    line_edit.setClearButtonEnabled(
        True
    )

    completer = QCompleter(
        combo.model(),
        combo
    )
    completer.setCaseSensitivity(
        Qt.CaseInsensitive
    )
    completer.setFilterMode(
        Qt.MatchFlag.MatchContains
    )
    completer.setCompletionMode(
        QCompleter.CompletionMode.PopupCompletion
    )
    combo.setCompleter(
        completer
    )

    return combo


def configure_plain_combo(
    combo
):
    combo.setObjectName(
        "plainCombo"
    )
    return combo


def configure_quantity_input(
    spinbox
):
    spinbox.setButtonSymbols(
        QAbstractSpinBox.ButtonSymbols.NoButtons
    )
    spinbox.setAlignment(
        Qt.AlignRight | Qt.AlignVCenter
    )
    spinbox.setObjectName(
        "plainQuantity"
    )
    return spinbox


def create_quantity_input(
    decimals=2,
    maximum=100000000
):
    if decimals == 0:
        spinbox = QSpinBox()
        spinbox.setMaximum(
            maximum
        )
    else:
        spinbox = QDoubleSpinBox()
        spinbox.setMaximum(
            maximum
        )
        spinbox.setDecimals(
            decimals
        )

    return configure_quantity_input(
        spinbox
    )


def combo_value_by_text(
    combo
):
    data = combo.currentData()
    if data is not None:
        return data

    text = combo.currentText().strip()
    index = combo.findText(
        text
    )
    if index >= 0:
        return combo.itemData(
            index
        )

    return None
