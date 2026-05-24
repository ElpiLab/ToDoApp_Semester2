import os
from collections.abc import Mapping
from functools import lru_cache
import logging
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.engine import make_url
from sqlmodel import Session
from sqlmodel import SQLModel, create_engine

DEFAULT_DATABASE_URL = "sqlite:///data/todo.db"
RAILWAY_DATABASE_URL = "sqlite:////app/data/todo.db"
LEGACY_RAILWAY_DATABASE_URL = "sqlite:////data/todo.db"
logger = logging.getLogger(__name__)


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


def safe_database_url_for_logs(url: str) -> str:
    return make_url(url).render_as_string(hide_password=True)


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


def migrate_legacy_student_is_active(engine: Engine) -> None:
    if engine.dialect.name != "sqlite":
        return
    with engine.begin() as connection:
        columns = connection.execute(text("PRAGMA table_info(student)")).mappings().all()
        if not any(column["name"] == "is_active" for column in columns):
            return
        logger.warning("Dropping legacy student.is_active column")
        connection.execute(text("ALTER TABLE student DROP COLUMN is_active"))


def create_db_and_tables() -> None:
    engine = get_engine()
    SQLModel.metadata.create_all(engine)
    migrate_legacy_student_is_active(engine)
    migrate_legacy_task_statuses(engine)
