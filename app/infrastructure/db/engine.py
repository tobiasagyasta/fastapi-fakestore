import os

from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine

load_dotenv()

database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL environment variable is not set")
db_echo_raw = os.getenv("DB_ECHO", "false")

db_echo = db_echo_raw.strip().lower() in {"1", "true", "yes", "on"}

engine = create_engine(
    database_url,
    echo=db_echo,
    pool_pre_ping=True,
)


def init_db() -> None:
    from app.infrastructure.db.models import ProductModel  # noqa: F401

    SQLModel.metadata.create_all(engine)
