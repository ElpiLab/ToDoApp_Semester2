import os
from sqlmodel import SQLModel, Session, create_engine

# Detect if running on Railway (has PORT env var) or locally
is_railway = os.environ.get("PORT") is not None

if is_railway:
    # On Railway – use writable /tmp directory
    DB_DIR = os.environ.get("RAILWAY_VOLUME_MOUNT_PATH", "/tmp")
else:
    # On your local Windows – use current directory
    DB_DIR = "."

DATABASE_URL = f"sqlite:///{DB_DIR}/todo.db"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
)

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session