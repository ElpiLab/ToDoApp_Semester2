from collections.abc import Iterator

import pytest
from sqlalchemy.engine import Engine
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from student_task_manager.data_access import db as db_module
from student_task_manager.domain.models import Student


@pytest.fixture
def seeded_test_engine(monkeypatch: pytest.MonkeyPatch) -> Iterator[Engine]:
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        session.add(
            Student(
                id=1,
                email="student@example.com",
                password_hash="not-used",
                full_name="Test Student",
            )
        )
        session.add(
            Student(
                id=2,
                email="other@example.com",
                password_hash="not-used",
                full_name="Other Student",
            )
        )
        session.commit()

    def get_test_engine(url: str | None = None) -> Engine:
        _ = url
        return test_engine

    monkeypatch.setattr(db_module, "get_engine", get_test_engine)
    yield test_engine
