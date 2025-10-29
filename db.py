from os import getenv
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import cast

Base = declarative_base()
load_dotenv()

SQLALCHEMY_DATABASE_URL = cast(str, getenv("DATABASE_URL"))

engine = create_engine(SQLALCHEMY_DATABASE_URL)
if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("Database url not set in the env")

# session creation
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_table():
    Base.metadata.create_all(bind=engine)
