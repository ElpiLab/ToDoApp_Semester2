from sqlmodel import Session, select

from student_task_manager.data_access.db import engine
from student_task_manager.domain.models import Task


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

    def get_all_for_user(self, user_id: int) -> list[Task]:
        with Session(engine) as session:
            statement = select(Task).where(Task.user_id == user_id)
            return list(session.exec(statement).all())

    def get_by_id(self, task_id: int) -> Task | None:
        with Session(engine) as session:
            return session.get(Task, task_id)

    def get_by_id_for_user(self, task_id: int, user_id: int) -> Task | None:
        with Session(engine) as session:
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            return session.exec(statement).first()

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
