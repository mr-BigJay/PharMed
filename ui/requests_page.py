from ui.widgets.placeholder_page import PlaceholderPage


class RequestsPage(PlaceholderPage):

    def __init__(self, main_window):
        super().__init__(
            main_window,
            "درخواست‌ها",
            "این بخش برای ثبت، پیگیری و تأیید درخواست‌های دارو و تجهیزات در نسخه‌های بعدی تکمیل می‌شود."
        )