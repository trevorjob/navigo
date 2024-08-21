""" The database module
"""

import os
from pathlib import Path

from api.utils.settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

BASE_DIR = Path(__file__).resolve().parent
DB_HOST = settings.DB_HOST
DB_PORT = settings.DB_PORT
DB_USER = settings.DB_USER
DB_PASSWORD = settings.DB_PASSWORD
DB_NAME = settings.DB_NAME
DB_TYPE = settings.DB_TYPE


def get_db_engine(test_mode: bool = False):
    if DB_TYPE == "sqlite" or test_mode:
        if test_mode:
            db_path = os.path.join(BASE_DIR, "test.db")
        else:
            db_path = os.path.join(BASE_DIR, DB_NAME)

        # Create the database file if it doesn't exist
        if not os.path.exists(db_path):
            open(db_path, "a").close()  # This creates an empty file

        DATABASE_URL = f"sqlite:///{db_path}"

        return create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

    elif DB_TYPE == "postgresql":
        DATABASE_URL = (
            f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

    return create_engine(DATABASE_URL)


engine = get_db_engine()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db_session = scoped_session(SessionLocal)

Base = declarative_base()


def create_database():
    """Creates the database tables if they do not exist"""
    Base.metadata.create_all(bind=engine)


def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()
