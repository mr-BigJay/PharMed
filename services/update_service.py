import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
import webbrowser
from dataclasses import dataclass
from pathlib import Path

from packaging.version import InvalidVersion, Version

from app_paths import project_root, user_data_dir
from version import (
    APP_VERSION,
    APP_VERSION_LABEL,
    GITHUB_DEFAULT_BRANCH,
    GITHUB_OWNER,
    GITHUB_REPO,
    WINDOWS_INSTALLER_SUFFIX,
)

GITHUB_API = (
    f"https://api.github.com/repos/"
    f"{GITHUB_OWNER}/{GITHUB_REPO}"
)


@dataclass
class UpdateInfo:
    current_version: str
    latest_version: str
    release_name: str
    release_notes: str
    download_url: str | None
    release_page_url: str
    source: str


def current_version_label() -> str:
    return APP_VERSION_LABEL


def is_frozen_app() -> bool:
    return bool(
        getattr(
            sys,
            "frozen",
            False
        )
    )


def _github_request(
    url
):
    request = urllib.request.Request(
        url,
        headers={
            "Accept": (
                "application/vnd.github+json"
            ),
            "User-Agent": (
                "PharMed-Updater"
            ),
        },
    )

    with urllib.request.urlopen(
        request,
        timeout=20
    ) as response:
        return json.loads(
            response.read().decode(
                "utf-8"
            )
        )


def _normalize_version(
    value
) -> Version:
    cleaned = value.strip()
    if cleaned.lower().startswith(
        "v"
    ):
        cleaned = cleaned[1:]

    return Version(
        cleaned
    )


def _release_page_url(
    tag_name=""
):
    if tag_name:
        return (
            f"https://github.com/"
            f"{GITHUB_OWNER}/{GITHUB_REPO}"
            f"/releases/tag/{tag_name}"
        )

    return (
        f"https://github.com/"
        f"{GITHUB_OWNER}/{GITHUB_REPO}"
        f"/releases/latest"
    )


def _pick_installer_asset(
    assets
):
    for asset in assets:
        name = asset.get(
            "name",
            ""
        )
        if name.endswith(
            WINDOWS_INSTALLER_SUFFIX
        ):
            return asset.get(
                "browser_download_url"
            )

    for asset in assets:
        download_url = asset.get(
            "browser_download_url"
        )
        if download_url:
            return download_url

    return None


def _fetch_latest_release():
    try:
        payload = _github_request(
            f"{GITHUB_API}/releases/latest"
        )
    except urllib.error.HTTPError as exc:
        if exc.code != 404:
            raise

        return None

    tag_name = payload.get(
        "tag_name",
        ""
    )
    return UpdateInfo(
        current_version=APP_VERSION,
        latest_version=tag_name.lstrip(
            "v"
        ),
        release_name=payload.get(
            "name",
            tag_name
        )
        or tag_name,
        release_notes=(
            payload.get(
                "body",
                ""
            )
            or ""
        ).strip(),
        download_url=_pick_installer_asset(
            payload.get(
                "assets",
                []
            )
        ),
        release_page_url=_release_page_url(
            tag_name
        ),
        source="release",
    )


def _fetch_latest_tag():
    payload = _github_request(
        f"{GITHUB_API}/tags"
    )

    if not payload:
        return None

    tag_name = payload[0].get(
        "name",
        ""
    )

    return UpdateInfo(
        current_version=APP_VERSION,
        latest_version=tag_name.lstrip(
            "v"
        ),
        release_name=tag_name,
        release_notes="",
        download_url=None,
        release_page_url=_release_page_url(
            tag_name
        ),
        source="tag",
    )


def check_for_updates():
    release = _fetch_latest_release()

    if release is None:
        release = _fetch_latest_tag()

    if release is None:
        return (
            False,
            "اطلاعات نسخه جدید در GitHub یافت نشد.",
            None,
        )

    try:
        latest = _normalize_version(
            release.latest_version
        )
        current = _normalize_version(
            APP_VERSION
        )
    except InvalidVersion as exc:
        return (
            False,
            f"نسخه دریافتی از GitHub نامعتبر است: {exc}",
            None,
        )

    if latest <= current:
        return (
            True,
            (
                "نسخه نصب‌شده شما به‌روز است "
                f"({current_version_label()})."
            ),
            None,
        )

    message = (
        f"نسخه جدید {release.latest_version} "
        f"منتشر شده است. نسخه فعلی شما "
        f"{current_version_label()} است."
    )
    return (
        True,
        message,
        release,
    )


def _download_file(
    url,
    destination
):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "PharMed-Updater"
            ),
        },
    )

    with urllib.request.urlopen(
        request,
        timeout=120
    ) as response:
        destination.write_bytes(
            response.read()
        )


def _find_git_root(
    start_path
):
    for path in [
        start_path,
        *start_path.parents,
    ]:
        if (
            path / ".git"
        ).exists():
            return path

    return None


def _apply_git_update():
    git_root = _find_git_root(
        project_root()
    )

    if git_root is None:
        return (
            False,
            "پوشه Git برای به‌روزرسانی سورس یافت نشد.",
        )

    if shutil.which(
        "git"
    ) is None:
        return (
            False,
            "Git روی سیستم نصب نیست.",
        )

    commands = [
        [
            "git",
            "fetch",
            "origin",
            GITHUB_DEFAULT_BRANCH,
        ],
        [
            "git",
            "pull",
            "origin",
            GITHUB_DEFAULT_BRANCH,
        ],
    ]

    for command in commands:
        result = subprocess.run(
            command,
            cwd=git_root,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            details = (
                result.stderr.strip()
                or result.stdout.strip()
                or "خطای نامشخص"
            )
            return (
                False,
                (
                    "به‌روزرسانی Git ناموفق بود:\n"
                    f"{details}"
                ),
            )

    return (
        True,
        (
            "کدهای جدید از GitHub دریافت شد. "
            "لطفاً برنامه را ببندید و دوباره اجرا کنید."
        ),
    )


def _apply_installer_update(
    update_info
):
    if not update_info.download_url:
        return (
            False,
            (
                "فایل نصب جدید در Release پیدا نشد. "
                "صفحه GitHub Releases را باز کنید."
            ),
        )

    if sys.platform != "win32":
        return (
            False,
            (
                "نصب خودکار فعلاً فقط در Windows "
                "پشتیبانی می‌شود."
            ),
        )

    updates_dir = user_data_dir() / "updates"
    updates_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    file_name = (
        update_info.download_url.rsplit(
            "/",
            1,
        )[-1]
    )
    safe_name = re.sub(
        r"[^\w.\-]+",
        "_",
        file_name,
    )
    installer_path = (
        updates_dir / safe_name
    )

    _download_file(
        update_info.download_url,
        installer_path
    )

    subprocess.Popen(
        [
            str(
                installer_path
            ),
        ],
        close_fds=True,
    )

    return (
        True,
        (
            "نصب‌کننده نسخه جدید اجرا شد. "
            "پس از پایان نصب، برنامه را دوباره باز کنید."
        ),
    )


def apply_update(
    update_info
):
    if is_frozen_app():
        return _apply_installer_update(
            update_info
        )

    return _apply_git_update()


def open_release_page(
    update_info=None
):
    url = (
        update_info.release_page_url
        if update_info
        else _release_page_url()
    )

    if sys.platform == "win32":
        os.startfile(
            url
        )
    else:
        webbrowser.open(
            url
        )

    return (
        True,
        "صفحه GitHub در مرورگر باز شد.",
    )
