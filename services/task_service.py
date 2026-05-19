from sqlmodel import Session, select
from data_access.db import engine
from domain.models import Task, Priority, Status
from datetime import date
from typing import Optional, List


class TaskService:
    
    def create_task(self, user_id: int, title: str, description: str = "", 
                    priority: Priority = Priority.medium, 
                    due_date: Optional[date] = None) -> Task:
        """Create a task for a specific user"""
        with Session(engine) as session:
            task = Task(
                user_id=user_id,
                title=title,
                description=description,
                priority=priority,
                due_date=due_date,
                status=Status.created,
                completed=False
            )
            session.add(task)
            session.commit()
            session.refresh(task)
            return task
    
    def get_user_tasks(self, user_id: int) -> List[Task]:
        """Get all tasks for a specific user"""
        with Session(engine) as session:
            tasks = session.exec(
                select(Task).where(Task.user_id == user_id)
            ).all()
            return tasks
    
    def get_all_tasks(self) -> List[Task]:
        """Get ALL tasks (admin only - careful!)"""
        with Session(engine) as session:
            tasks = session.exec(select(Task)).all()
            return tasks
    
    def update_task(self, task_id: int, user_id: int, **kwargs) -> Optional[Task]:
        """Update a task only if it belongs to the user"""
        with Session(engine) as session:
            task = session.exec(
                select(Task).where(Task.id == task_id, Task.user_id == user_id)
            ).first()
            
            if task:
                for key, value in kwargs.items():
                    if hasattr(task, key) and value is not None:
                        setattr(task, key, value)
                session.commit()
                session.refresh(task)
                return task
            return None
    
    def delete_task(self, task_id: int, user_id: int) -> bool:
        """Delete a task only if it belongs to the user"""
        with Session(engine) as session:
            task = session.exec(
                select(Task).where(Task.id == task_id, Task.user_id == user_id)
            ).first()
            
            if task:
                session.delete(task)
                session.commit()
                return True
            return False
    
    def mark_complete(self, task_id: int, user_id: int) -> bool:
        """Mark task as complete only if it belongs to user"""
        with Session(engine) as session:
            task = session.exec(
                select(Task).where(Task.id == task_id, Task.user_id == user_id)
            ).first()
            
            if task:
                task.completed = True
                task.status = Status.done
                session.commit()
                return True
            return False
    
    def mark_pending(self, task_id: int, user_id: int) -> bool:
        """Mark task as pending only if it belongs to user"""
        with Session(engine) as session:
            task = session.exec(
                select(Task).where(Task.id == task_id, Task.user_id == user_id)
            ).first()
            
            if task:
                task.completed = False
                task.status = Status.pending
                session.commit()
                return True
            return False