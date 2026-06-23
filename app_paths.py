from pathlib import Path
import os
import sys


def project_root():
    return Path(__file__).resolve().parent


def user_data_dir():
    if sys.platform == "win32":
        base = Path(
            os.environ.get(
                "LOCALAPPDATA",
                Path.home()
            )
        )
    else:
        base = Path.home()

    path = base / "PharMed"
    path.mkdir(
        parents=True,
        exist_ok=True
    )
    return path


def resource_path(*parts):
    base_dir = Path(
        getattr(
            sys,
            "_MEIPASS",
            project_root()
        )
    )

    return base_dir.joinpath(
        *parts
    )
