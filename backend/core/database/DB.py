# psycopg2 : for PostgreSQL connections
# aioODBC : for MSSQL connections

from typing import Generator
from sqlmodel import Session, create_engine
from core.helperfunctions import get_env_var

databaseurl = get_env_var("DATABASE_URL")

# Create an SQLAlchemy engine with echo enabled for query logging
engine = create_engine(databaseurl, echo=True, future=True)

# Not required as Alembic handles DB migrations
# SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency generator for creating and closing a database session.

    Yields:
        Session: A SQLModel session object connected to the database.

    This function ensures proper resource management by:
    - Creating a new session for each request.
    - Yielding the session for database operations.
    - Automatically closing the session when done.

    Example:
        ```python
        from fastapi import Depends

        def get_items(session: Session = Depends(get_session)):
            return session.query(Item).all()
        ```
    """
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
