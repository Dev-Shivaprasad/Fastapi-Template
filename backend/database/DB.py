# psycopg2 : for postgresql
# aioODBC : for mssql
# import aioodbc
from typing import Generator

from sqlmodel import Session, SQLModel, create_engine


DATABASE_URL = (
    "mssql+pyodbc://@SHIVAPRASAD\\SQLEXPRESS/test"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
    "&Encrypt=no"
)

engine = create_engine(DATABASE_URL, echo=True, future=True)

SQLModel.metadata.create_all(engine)


# ✅ Correct FastAPI-compatible session dependency
def get_session() -> Generator[Session, None, None]:
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
