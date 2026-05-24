import shutil
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine

from student_task_manager.data_access.db import (
    database_url,
    engine_connect_args,
    get_engine,
    migrate_legacy_task_statuses,
)
from student_task_manager.domain.models import Task


def test_database_url_defaults_to_local_sqlite_file() -> None:
    assert database_url({}) == "sqlite:///data/todo.db"


def test_database_url_can_be_overridden() -> None:
    assert database_url({"DATABASE_URL": "sqlite:////data/todo.db"}) == "sqlite:////data/todo.db"


def test_engine_connect_args_are_sqlite_specific() -> None:
    assert engine_connect_args("sqlite:///data/todo.db") == {"check_same_thread": False}
    assert engine_connect_args("postgresql://example") == {}


def test_get_engine_creates_sqlite_parent_directory() -> None:
    db_dir = Path("build/test-db-config-lazy")
    shutil.rmtree(db_dir, ignore_errors=True)
    db_path = db_dir / "todo.db"

    get_engine.cache_clear()
    engine = get_engine(f"sqlite:///{db_path}")
    get_engine.cache_clear()

    assert engine.url.database == str(db_path)
    assert db_path.parent.exists()
    shutil.rmtree(db_dir, ignore_errors=True)


def test_migrate_legacy_task_statuses_collapses_created_rows_to_pending() -> None:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    with engine.begin() as connection:
        connection.execute(
            text(
                "INSERT INTO task "
                "(title, description, priority, status, category, completed, user_id) "
                "VALUES ('Legacy task', '', 'medium', 'created', 'Other', 0, 1)"
            )
        )

    migrate_legacy_task_statuses(engine)

    with Session(engine) as session:
        stored_task = session.get(Task, 1)

    assert stored_task is not None
    assert stored_task.status.value == "pending"
