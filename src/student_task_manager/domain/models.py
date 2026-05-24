from datetime import date
from enum import Enum

from sqlmodel import Field, Relationship, SQLModel


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Status(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"


class Student(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    full_name: str = ""
    is_active: bool = True

    # Relationship to tasks
    tasks: list["Task"] = Relationship(back_populates="owner")


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    title: str
    description: str = ""
    priority: Priority = Priority.medium
    status: Status = Status.pending
    category: str = "Other"

    due_date: date | None = None
    completed: bool = False

    # Foreign key to link to user
    user_id: int = Field(foreign_key="student.id", index=True)

    # Relationship back to user
    owner: Student = Relationship(back_populates="tasks")
