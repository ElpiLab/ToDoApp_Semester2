from datetime import date
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Status(str, Enum):
    created = "created"
    pending = "pending"
    in_progress = "in_progress"
    done = "done"


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    title: str
    description: str = ""
    priority: Priority = Priority.medium
    status: Status = Status.created

    due_date: Optional[date] = None
    completed: bool = False