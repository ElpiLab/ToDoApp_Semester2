from sqlmodel import Session, select

from data_access.db import engine
from domain.models import Task


class TaskDAO:
    def create(self, task: Task) -> Task:
        with Session(engine) as session:
            session.add(task)
            session.commit()
            session.refresh(task)
            return task

    def get_all(self) -> list[Task]:
        with Session(engine) as session:
            return list(session.exec(select(Task)).all())

    def get_by_id(self, task_id: int) -> Task | None:
        with Session(engine) as session:
            return session.get(Task, task_id)

    def update(self, task: Task) -> Task:
        with Session(engine) as session:
            session.add(task)
            session.commit()
            session.refresh(task)
            return task

    def delete(self, task_id: int) -> None:
        with Session(engine) as session:
            task = session.get(Task, task_id)
            if task:
                session.delete(task)
                session.commit()
