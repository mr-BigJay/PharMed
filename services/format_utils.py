from datetime import date, datetime

WESTERN_TO_PERSIAN = str.maketrans(
    "0123456789",
    "۰۱۲۳۴۵۶۷۸۹"
)


def to_persian_digits(value) -> str:
    return str(value).translate(
        WESTERN_TO_PERSIAN
    )


def format_value(value) -> str:
    if value is None:
        return ""

    if isinstance(value, datetime):
        return to_persian_digits(
            value.strftime("%Y/%m/%d")
        )

    if isinstance(value, date):
        return to_persian_digits(
            value.strftime("%Y/%m/%d")
        )

    if isinstance(value, float):
        if value.is_integer():
            return to_persian_digits(
                int(value)
            )
        return to_persian_digits(
            f"{value:.2f}"
        )

    if isinstance(value, int):
        return to_persian_digits(value)

    return to_persian_digits(str(value))
