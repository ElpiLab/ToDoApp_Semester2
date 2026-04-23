from sqlmodel import SQLModel, Field
from enum import Enum
from datetime import date
from typing import Optional


# 🔹 ENUMS (controlled values)

class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Status(str, Enum):
    created = "created"
    pending = "pending"
    in_progress = "in_progress"
    done = "done"


# 🔹 MAIN ENTITY

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    title: str
    description: str

    priority: Priority
    status: Status = Status.created

    due_date: Optional[date] = None
    completed: bool = False