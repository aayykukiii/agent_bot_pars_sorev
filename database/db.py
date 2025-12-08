from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Use project root bron.db so Alembic and app point to the same file.
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DB_FILE = os.path.join(PROJECT_ROOT, "bron.db")


engine = create_engine(
    f"sqlite:///{DB_FILE}",
    echo=False,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)

Base = declarative_base()


def create_tables():
    """Create all tables from declarative models.

    This is provided as an explicit helper so you can call it when needed
    (for example, during development). When using Alembic for migrations,
    prefer running migrations instead of calling this in production.
    """
    Base.metadata.create_all(bind=engine)
