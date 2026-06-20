from sqlalchemy.orm import sessionmaker

from db import engine

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)