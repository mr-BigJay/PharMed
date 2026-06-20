from pathlib import Path
import sys


def project_root():
    return Path(__file__).resolve().parent


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
