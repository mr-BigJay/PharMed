from ui.widgets.placeholder_page import PlaceholderPage


class InventoryPage(PlaceholderPage):

    def __init__(self, main_window):
        super().__init__(
            main_window,
            "مدیریت موجودی دارو",
            "این بخش برای ثبت موجودی اولیه، ورود و خروج داروها و کنترل حداقل موجودی در نسخه‌های بعدی تکمیل می‌شود."
        )