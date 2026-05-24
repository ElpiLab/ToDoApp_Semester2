import os
from collections.abc import Mapping
from functools import lru_cache
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.engine import make_url
from sqlmodel import Session
from sqlmodel import SQLModel, create_engine

DEFAULT_DATABASE_URL = "sqlite:///data/todo.db"
RAILWAY_DATABASE_URL = "sqlite:////app/data/todo.db"
LEGACY_RAILWAY_DATABASE_URL = "sqlite:////data/todo.db"


def _is_railway(env: Mapping[str, str]) -> bool:
    return any(key.startswith("RAILWAY_") for key in env)


def database_url(env: Mapping[str, str] = os.environ) -> str:
    configured_url = env.get("DATABASE_URL")
    if configured_url:
        if _is_railway(env) and configured_url == LEGACY_RAILWAY_DATABASE_URL:
            return RAILWAY_DATABASE_URL
        return configured_url
    if _is_railway(env):
        return RAILWAY_DATABASE_URL
    return DEFAULT_DATABASE_URL


def engine_connect_args(url: str) -> dict[str, bool]:
    if url.startswith("sqlite:"):
        return {"check_same_thread": False}
    return {}


def _ensure_sqlite_parent_dir(url: str) -> None:
    parsed = make_url(url)
    if parsed.drivername != "sqlite" or not parsed.database or parsed.database == ":memory:":
        return
    Path(parsed.database).parent.mkdir(parents=True, exist_ok=True)


@lru_cache(maxsize=1)
def get_engine(url: str | None = None) -> Engine:
    database_url_value = url or database_url()
    _ensure_sqlite_parent_dir(database_url_value)
    return create_engine(
        database_url_value,
        echo=False,
        connect_args=engine_connect_args(database_url_value),
    )


def get_session() -> Session:
    return Session(get_engine())


def migrate_legacy_task_statuses(engine: Engine) -> None:
    with engine.begin() as connection:
        connection.execute(text("UPDATE task SET status = 'pending' WHERE status = 'created'"))


def create_db_and_tables() -> None:
    engine = get_engine()
    SQLModel.metadata.create_all(engine)
    migrate_legacy_task_statuses(engine)
