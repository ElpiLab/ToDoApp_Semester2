from sqlmodel import Session, select
from data_access.db import engine
from domain.models import Task


def seed_tasks() -> None:
    with Session(engine) as session:
        existing_tasks = session.exec(select(Task)).all()

        if existing_tasks:
            return

        sample_tasks = [
            Task(title="Finish assignment"),
            Task(title="Review architecture"),
            Task(title="Test create and delete"),
        ]

        for task in sample_tasks:
            session.add(task)

        session.commit()