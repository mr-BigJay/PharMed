from PySide6.QtCore import QThread, Signal

from services.update_service import (
    UpdateInfo,
    apply_update,
    check_for_updates,
)


class UpdateCheckWorker(QThread):

    finished = Signal(
        bool,
        str,
        object,
    )

    def run(self):
        success, message, update_info = (
            check_for_updates()
        )
        self.finished.emit(
            success,
            message,
            update_info,
        )


class UpdateApplyWorker(QThread):

    finished = Signal(
        bool,
        str,
    )

    def __init__(
        self,
        update_info: UpdateInfo
    ):
        super().__init__()
        self.update_info = update_info

    def run(self):
        success, message = apply_update(
            self.update_info
        )
        self.finished.emit(
            success,
            message,
        )
