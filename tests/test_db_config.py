from student_task_manager.data_access.db import database_url, engine_connect_args


def test_database_url_defaults_to_local_sqlite_file() -> None:
    assert database_url({}) == "sqlite:///todo.db"


def test_database_url_can_be_overridden() -> None:
    assert database_url({"DATABASE_URL": "sqlite:////data/todo.db"}) == "sqlite:////data/todo.db"


def test_engine_connect_args_are_sqlite_specific() -> None:
    assert engine_connect_args("sqlite:///todo.db") == {"check_same_thread": False}
    assert engine_connect_args("postgresql://example") == {}
