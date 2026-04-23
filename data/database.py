from sqlmodel import SQLModel, create_engine, Session

# 🔹 Database URL (SQLite file)
DATABASE_URL = "sqlite:///todo.db"

# 🔹 Engine (connection to DB)
engine = create_engine(DATABASE_URL, echo=True)


# 🔹 Create tables (VERY IMPORTANT)
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# 🔹 Session (used for DB operations)
def get_session():
    with Session(engine) as session:
        yield session