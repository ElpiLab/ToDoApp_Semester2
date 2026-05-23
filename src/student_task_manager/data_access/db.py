import os
from collections.abc import Mapping

from sqlalchemy import inspect, text
from sqlmodel import SQLModel, create_engine


def database_url(env: Mapping[str, str] = os.environ) -> str:
    return env.get("DATABASE_URL", "sqlite:///todo.db")


def engine_connect_args(url: str) -> dict[str, bool]:
    if url.startswith("sqlite:"):
        return {"check_same_thread": False}
    return {}


DATABASE_URL = database_url()

engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args=engine_connect_args(DATABASE_URL),
)


def _ensure_task_columns() -> None:
    inspector = inspect(engine)
    if not inspector.has_table("task"):
        return
    existing = {col["name"] for col in inspector.get_columns("task")}
    with engine.begin() as conn:
        if "category" not in existing:
            conn.execute(text("ALTER TABLE task ADD COLUMN category VARCHAR DEFAULT 'other'"))
        if "user_id" not in existing:
            conn.execute(text("ALTER TABLE task ADD COLUMN user_id INTEGER NOT NULL DEFAULT 1"))


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)
    _ensure_task_columns()
