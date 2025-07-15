# psycopg2 : for postgresql
# aioODBC : for mssql
from typing import Generator
from sqlmodel import Session, create_engine
from utils.helperfunctions import GetEnvVar


databaseurl = GetEnvVar("DATABASE_URL")
engine = create_engine(databaseurl, echo=True, future=True)

# no necessary as we are using alembic for DB migrations
# SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
