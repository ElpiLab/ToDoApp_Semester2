from sqlmodel import Session, select
from domain.models import Task
from data.database import engine


class TaskDAO:

    # 🔹 CREATE
    def create(self, task: Task) -> Task:
        with Session(engine) as session:
            session.add(task)
            session.commit()
            session.refresh(task)
            return task

    # 🔹 READ ALL
    def get_all(self) -> list[Task]:
        with Session(engine) as session:
            return session.exec(select(Task)).all()

    # 🔹 READ BY ID
    def get_by_id(self, task_id: int) -> Task | None:
        with Session(engine) as session:
            return session.get(Task, task_id)

    # 🔹 UPDATE
    def update(self, task: Task) -> Task:
        with Session(engine) as session:
            session.add(task)
            session.commit()
            session.refresh(task)
            return task

    # 🔹 DELETE
    def delete(self, task_id: int) -> None:
        with Session(engine) as session:
            task = session.get(Task, task_id)
            if task:
                session.delete(task)
                session.commit()