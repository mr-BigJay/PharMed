import os
import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, ROOT)


class MockMainWindow:
    current_user = None

    def show_register(self):
        pass

    def show_dashboard(self):
        pass


def main():
    app = QApplication(sys.argv)

    with open(
        "assets/style.qss",
        "r",
        encoding="utf-8"
    ) as file:
        app.setStyleSheet(file.read())

    from ui.login_window import LoginWindow

    login = LoginWindow(MockMainWindow())
    login.resize(1280, 720)
    login.show()

    output_path = os.environ.get(
        "LOGIN_SCREENSHOT_PATH",
        "/opt/cursor/artifacts/login-split-screen-preview.png"
    )

    def capture():
        os.makedirs(
            os.path.dirname(output_path),
            exist_ok=True
        )
        login.grab().save(output_path)
        print(output_path)
        app.quit()

    QTimer.singleShot(400, capture)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
