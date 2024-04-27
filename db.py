from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import get_settings

settings = get_settings()

# DB_URL = f"mysql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

DB_URL = f"mysql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

# print(f"DB_URL: {DB_URL}")

# print(f"DB_HOST: {settings.DB_HOST}")
# print(f"DB_PORT: {settings.DB_PORT}")
# print(f"DB_NAME: {settings.DB_NAME}")
# print(f"DB_USERNAME: {settings.DB_USERNAME}")
# print(f"DB_PASSWORD: {settings.DB_PASSWORD}")

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
