from collections.abc import Callable

from sqlmodel import Session, select

from student_task_manager.data_access.db import get_session
from student_task_manager.domain.models import Task


class TaskDAO:
    def __init__(self, session_factory: Callable[[], Session] = get_session) -> None:
        self.session_factory = session_factory

    def create(self, task: Task) -> Task:
        with self.session_factory() as session:
            session.add(task)
            session.commit()
            session.refresh(task)
            return task

    def get_all_for_user(self, user_id: int) -> list[Task]:
        with self.session_factory() as session:
            statement = select(Task).where(Task.user_id == user_id)
            return list(session.exec(statement).all())

    def get_by_id_for_user(self, task_id: int, user_id: int) -> Task | None:
        with self.session_factory() as session:
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            return session.exec(statement).first()

    def update(self, task: Task) -> Task:
        with self.session_factory() as session:
            session.add(task)
            session.commit()
            session.refresh(task)
            return task

    def delete_for_user(self, task_id: int, user_id: int) -> bool:
        with self.session_factory() as session:
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            task = session.exec(statement).first()
            if task is None:
                return False
            session.delete(task)
            session.commit()
            return True

    def delete_all_for_user(self, user_id: int) -> int:
        with self.session_factory() as session:
            statement = select(Task).where(Task.user_id == user_id)
            tasks = list(session.exec(statement).all())
            for task in tasks:
                session.delete(task)
            session.commit()
            return len(tasks)
