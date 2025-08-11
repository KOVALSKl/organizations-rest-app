import os

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker, Session

DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=DB_USER,
    password=DB_PASS,
    # host="secunda-rest-app-db",
    host="localhost",
    port=32700,
    database=DB_NAME,
)

print(DATABASE_URL.render_as_string(hide_password=False))


engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
)

def get_session() -> Session:
    with SessionLocal() as session:
        yield session