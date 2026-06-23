from datetime import datetime
from zoneinfo import ZoneInfo

import jdatetime

from services.format_utils import format_value

TEHRAN_TZ = ZoneInfo(
    "Asia/Tehran"
)

WEEKDAY_NAMES = [
    "شنبه",
    "یکشنبه",
    "دوشنبه",
    "سه‌شنبه",
    "چهارشنبه",
    "پنجشنبه",
    "جمعه",
]


def get_tehran_now() -> datetime:
    return datetime.now(
        TEHRAN_TZ
    )


def format_tehran_time(
    now=None
) -> str:
    if now is None:
        now = get_tehran_now()

    return format_value(
        now.strftime(
            "%H:%M"
        )
    )


def format_tehran_jalali_label(
    now=None
) -> str:
    if now is None:
        now = get_tehran_now()

    jalali = jdatetime.datetime.fromgregorian(
        datetime=now
    )
    weekday = WEEKDAY_NAMES[
        jalali.weekday()
    ]
    date_text = format_value(
        jalali.strftime(
            "%Y/%m/%d"
        )
    )

    return (
        f"{weekday} ، {date_text}"
    )
