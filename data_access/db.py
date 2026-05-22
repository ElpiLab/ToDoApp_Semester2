import os
from sqlmodel import SQLModel, Session, create_engine

# Railway uses /tmp as writable space
DB_DIR = "/tmp" if os.environ.get("PORT") else "."
DATABASE_URL = f"sqlite:///{DB_DIR}/todo.db"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session