from sqlalchemy import inspect, text
from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = "sqlite:///todo.db"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False},
)


def _ensure_task_columns() -> None:
    inspector = inspect(engine)
    if not inspector.has_table("task"):
        return
    existing = {col["name"] for col in inspector.get_columns("task")}
    with engine.begin() as conn:
        if "category" not in existing:
            conn.execute(
                text(
                    "ALTER TABLE task "
                    "ADD COLUMN category VARCHAR DEFAULT 'other'"
                )
            )


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)
    _ensure_task_columns()


def get_session():
    with Session(engine) as session:
        yield session
