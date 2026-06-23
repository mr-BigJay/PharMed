from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractSpinBox,
    QComboBox,
    QCompleter,
    QDoubleSpinBox,
    QSpinBox,
)


class SearchableComboBox(QComboBox):

    def __init__(
        self,
        placeholder="",
        parent=None
    ):
        super().__init__(
            parent
        )
        self.setEditable(
            True
        )
        self.setInsertPolicy(
            QComboBox.InsertPolicy.NoInsert
        )
        self.setObjectName(
            "searchCombo"
        )

        line_edit = self.lineEdit()
        line_edit.setPlaceholderText(
            placeholder
            or "جستجو یا انتخاب از لیست..."
        )
        line_edit.setClearButtonEnabled(
            True
        )

        completer = QCompleter(
            self.model(),
            self
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
        self.setCompleter(
            completer
        )

        line_edit.textEdited.connect(
            self._on_text_edited
        )

    def _on_text_edited(
        self,
        text
    ):
        self._apply_filter(
            text.strip()
        )

    def _apply_filter(
        self,
        text=""
    ):
        needle = text.lower()

        for index in range(
            self.count()
        ):
            if not needle:
                hidden = False
            else:
                hidden = (
                    needle
                    not in self.itemText(
                        index
                    ).lower()
                )

            self.view().setRowHidden(
                index,
                hidden
            )

    def showPopup(self):
        self._apply_filter(
            self.currentText().strip()
        )
        super().showPopup()

    def clear(self):
        super().clear()
        self._apply_filter(
            ""
        )

    def hidePopup(self):
        super().hidePopup()
        self._apply_filter(
            self.currentText().strip()
        )


def create_searchable_combo(
    placeholder=""
):
    return SearchableComboBox(
        placeholder
    )


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


def reset_combo_selection(
    combo
):
    combo.blockSignals(
        True
    )
    combo.setCurrentIndex(
        -1
    )

    line_edit = combo.lineEdit()
    if line_edit:
        line_edit.clear()

    combo.blockSignals(
        False
    )

    if isinstance(
        combo,
        SearchableComboBox
    ):
        combo._apply_filter(
            ""
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
