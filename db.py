from pathlib import Path

from sqlalchemy import create_engine


BASE_DIR = Path(__file__).resolve().parent
DATABASE_DIR = BASE_DIR / "database"
DATABASE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

DATABASE_PATH = DATABASE_DIR / "pharmed.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(
    DATABASE_URL,
    echo=False
)


def init_db():
    import models  # noqa: F401
    from models.base import Base

    Base.metadata.create_all(
        bind=engine
    )