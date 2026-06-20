from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///database/pharmed.db"

engine = create_engine(
    DATABASE_URL,
    echo=False
)