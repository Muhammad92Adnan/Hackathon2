from sqlmodel import create_engine
from sqlalchemy.pool import QueuePool
from .config import settings
from typing import Generator


# Create the database engine
engine = create_engine(
    settings.database_url,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=300,
)


def get_session() -> Generator:
    """Get a database session."""
    from sqlmodel import Session
    with Session(engine) as session:
        yield session