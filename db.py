from pathlib import Path

from sqlalchemy import create_engine, inspect, text


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

    _ensure_schema_updates()


def _ensure_schema_updates():
    inspector = inspect(
        engine
    )

    if "opening_stock" in inspector.get_table_names():
        _ensure_column(
            "opening_stock",
            "center_id",
            "INTEGER"
        )
        _ensure_column(
            "opening_stock",
            "health_house_id",
            "INTEGER"
        )

    if "stock_transactions" in inspector.get_table_names():
        _ensure_column(
            "stock_transactions",
            "center_id",
            "INTEGER"
        )
        _ensure_column(
            "stock_transactions",
            "health_house_id",
            "INTEGER"
        )
        _ensure_column(
            "stock_transactions",
            "transaction_date",
            "DATE"
        )


def _ensure_column(
    table_name,
    column_name,
    column_type
):
    inspector = inspect(
        engine
    )
    existing_columns = {
        column["name"]
        for column in inspector.get_columns(
            table_name
        )
    }

    if column_name in existing_columns:
        return

    with engine.begin() as connection:
        connection.execute(
            text(
                f"ALTER TABLE {table_name} "
                f"ADD COLUMN {column_name} {column_type}"
            )
        )
