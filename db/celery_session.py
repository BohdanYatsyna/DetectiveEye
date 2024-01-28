from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.settings import settings


DATABASE_URL = settings.DATABASE_URL.replace("asyncpg", "psycopg2")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_sync_session():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
