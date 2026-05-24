import shutil
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine

from student_task_manager.data_access.db import (
    LEGACY_RAILWAY_DATABASE_URL,
    RAILWAY_DATABASE_URL,
    database_url,
    engine_connect_args,
    get_engine,
    migrate_legacy_student_is_active,
    migrate_legacy_task_statuses,
    safe_database_url_for_logs,
)
from student_task_manager.domain.models import Student, Task


def test_database_url_defaults_to_local_sqlite_file() -> None:
    assert database_url({}) == "sqlite:///data/todo.db"


def test_database_url_can_be_overridden() -> None:
    assert database_url({"DATABASE_URL": "sqlite:////data/todo.db"}) == "sqlite:////data/todo.db"


def test_database_url_defaults_to_railway_volume_when_deployed() -> None:
    assert database_url({"RAILWAY_ENVIRONMENT": "production"}) == RAILWAY_DATABASE_URL


def test_database_url_corrects_legacy_railway_absolute_data_path() -> None:
    assert (
        database_url(
            {
                "RAILWAY_ENVIRONMENT": "production",
                "DATABASE_URL": LEGACY_RAILWAY_DATABASE_URL,
            }
        )
        == RAILWAY_DATABASE_URL
    )


def test_database_url_respects_explicit_non_legacy_railway_database_url() -> None:
    custom_url = "sqlite:////app/data/custom.db"

    assert (
        database_url(
            {
                "RAILWAY_ENVIRONMENT": "production",
                "DATABASE_URL": custom_url,
            }
        )
        == custom_url
    )


def test_engine_connect_args_are_sqlite_specific() -> None:
    assert engine_connect_args("sqlite:///data/todo.db") == {"check_same_thread": False}
    assert engine_connect_args("postgresql://example") == {}


def test_safe_database_url_for_logs_hides_password() -> None:
    logged_url = safe_database_url_for_logs("postgresql://user:secret@example.com/app")

    assert logged_url == "postgresql://user:***@example.com/app"
    assert "secret" not in logged_url


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


def test_migrate_legacy_student_is_active_drops_stale_not_null_column() -> None:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    with engine.begin() as connection:
        connection.execute(
            text(
                "CREATE TABLE student ("
                "id INTEGER PRIMARY KEY, "
                "email VARCHAR NOT NULL, "
                "password_hash VARCHAR NOT NULL, "
                "full_name VARCHAR NOT NULL, "
                "is_active BOOLEAN NOT NULL)"
            )
        )
        connection.execute(text("CREATE UNIQUE INDEX ix_student_email ON student (email)"))

    SQLModel.metadata.create_all(engine)
    migrate_legacy_student_is_active(engine)

    with engine.connect() as connection:
        columns = connection.execute(text("PRAGMA table_info(student)")).mappings().all()
    assert {column["name"] for column in columns} == {
        "id",
        "email",
        "password_hash",
        "full_name",
    }

    with Session(engine) as session:
        user = Student(
            email="new@example.com",
            password_hash="hash",
            full_name="New Student",
        )
        session.add(user)
        session.commit()

    with Session(engine) as session:
        assert session.get(Student, 1) is not None


def test_migrate_legacy_student_is_active_is_idempotent() -> None:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    migrate_legacy_student_is_active(engine)
    migrate_legacy_student_is_active(engine)

    with engine.connect() as connection:
        columns = connection.execute(text("PRAGMA table_info(student)")).mappings().all()
    assert "is_active" not in {column["name"] for column in columns}
